import os
import sys
import json
import requests
import webview

class Api:
    def __init__(self):
        # If compiled, use sys.executable dir; else use script dir
        if getattr(sys, 'frozen', False):
            app_dir = os.path.dirname(sys.executable)
        else:
            app_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_file = os.path.join(app_dir, 'config.json')
        self.session = requests.Session()

    def get_config(self):
        """Read the Google Apps Script URL from the local config file."""
        default_url = "https://script.google.com/macros/s/AKfycbzdN_JoCmrwDbM_9Bi7XU84kKIdGz2sMCK8gDIPev4jR58WDZvn0PddRDIkZ13LNQQW0w/exec"
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return {"success": True, "url": data.get("url", default_url) or default_url}
            return {"success": True, "url": default_url}
        except Exception as e:
            return {"success": True, "url": default_url}

    def save_config(self, url):
        """Save the Google Apps Script URL to the local config file."""
        try:
            data = {"url": url}
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def api_request(self, payload):
        """
        Proxy requests to the Google Apps Script API.
        Handles CORS automatically since request is made from Python environment.
        """
        try:
            # First, fetch the URL from config
            config = self.get_config()
            if not config.get("success") or not config.get("url"):
                return {"success": False, "error": "Google Apps Script URL is not configured."}
            
            url = config.get("url")
            
            # Apps Script Web Apps require POST requests for operations modifying/reading data safely
            # We send payload as JSON and allow redirects since Google redirects the request
            headers = {
                'Content-Type': 'application/json'
            }
            
            # Make the request and follow redirects using the session object
            response = self.session.post(url, data=json.dumps(payload), headers=headers, allow_redirects=True, timeout=30)
            
            if response.status_code == 200:
                try:
                    return response.json()
                except Exception:
                    return {"success": False, "error": "Invalid response format from script: " + response.text[:200]}
            else:
                return {
                    "success": False, 
                    "error": f"HTTP request failed with status code: {response.status_code}. Response: {response.text[:200]}"
                }
        except Exception as e:
            return {"success": False, "error": str(e)}


def get_asset_path(relative_path):
    """Get the absolute path to resource, works for dev and for PyInstaller."""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    return os.path.join(base_path, relative_path)


def main():
    api = Api()
    
    # Locate index.html
    html_path = get_asset_path('index.html')
    
    if not os.path.exists(html_path):
        # Fallback to local file in current working directory if not found in bundle path
        html_path = os.path.abspath('index.html')
    
    # Create webview window
    window = webview.create_window(
        title='PeriFerry Employee Portal',
        url=html_path,
        js_api=api,
        width=1280,
        height=800,
        min_size=(1000, 700),
        background_color='#ffffff'
    )
    
    # Start webview loop
    webview.start(debug=False)

if __name__ == '__main__':
    main()
