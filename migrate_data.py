import json
import re
import requests
from datetime import datetime

# Source Google Apps Script URL
GAS_URL = 'https://script.google.com/macros/s/AKfycbzdN_JoCmrwDbM_9Bi7XU84kKIdGz2sMCK8gDIPev4jR58WDZvn0PddRDIkZ13LNQQW0w/exec'

# Target Supabase Credentials
SUPABASE_URL = 'https://oijgqcmdofvicworgeir.supabase.co/rest/v1'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9pamdxY21kb2Z2aWN3b3JnZWlyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODQ3NzYyMDAsImV4cCI6MjEwMDM1MjIwMH0.FnLH_PrbjEUvaPTC8hr-jtUeaAol31ReUKH6k-SQgdU'

headers = {
    'apikey': SUPABASE_KEY,
    'Authorization': f'Bearer {SUPABASE_KEY}',
    'Content-Type': 'application/json'
}

def parse_date_string(dt_str, context_date=None):
    if not dt_str:
        return None
    dt_str = dt_str.strip()
    
    # Check for empty string representation or nulls
    if dt_str.lower() in ('null', 'undefined', ''):
        return None
        
    # Extract time part from "Sat Dec 30 1899 16:06:01 (India Standard Time)" or similar
    if "1899" in dt_str or "1900" in dt_str:
        time_match = re.search(r'(\d{2}:\d{2}:\d{2})', dt_str)
        if time_match and context_date:
            return f"{context_date}T{time_match.group(1)}Z"
        elif time_match:
            # Fallback to current date if context_date is missing
            today_str = datetime.now().strftime("%Y-%m-%d")
            return f"{today_str}T{time_match.group(1)}Z"
            
    # Check if timezone is appended (e.g., "gmt+0521" or "gmt+0530") and clean it
    dt_str = re.sub(r'\s+gmt\+\d+', '', dt_str, flags=re.IGNORECASE)
    dt_str = re.sub(r'\s+gmt\-\d+', '', dt_str, flags=re.IGNORECASE)
    dt_str = re.sub(r'\s+gmt', '', dt_str, flags=re.IGNORECASE)
    dt_str = dt_str.strip()

    # Format 1: "HH:MM:SS YYYY-MM-DD"
    match1 = re.match(r'^(\d{2}:\d{2}:\d{2})\s+(\d{4}-\d{2}-\d{2})$', dt_str)
    if match1:
        time_part, date_part = match1.groups()
        return f"{date_part}T{time_part}Z"
        
    # Format 2: "YYYY-MM-DD HH:MM:SS"
    match2 = re.match(r'^(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2})$', dt_str)
    if match2:
        date_part, time_part = match2.groups()
        return f"{date_part}T{time_part}Z"

    # Standard formats parsing
    for fmt in ("%Y-%m-%d %H:%M:%S", "%H:%M:%S %Y-%m-%d", "%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(dt_str, fmt)
            return dt.isoformat() + "Z"
        except ValueError:
            continue
            
    # Try parsing generic date format
    try:
        dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        return dt.isoformat()
    except Exception:
        pass
        
    return dt_str

def format_month_cell(month_val):
    if not month_val:
        return ""
    month_val = str(month_val).strip()
    if re.match(r'^\d{4}-\d{2}$', month_val):
        return month_val
    months_map = {
        'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04', 'may': '05', 'jun': '06',
        'jul': '07', 'aug': '08', 'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'
    }
    month_val_lower = month_val.lower()
    found_month = None
    for m_name, m_num in months_map.items():
        if m_name in month_val_lower:
            found_month = m_num
            break
    year_match = re.search(r'\b(20\d{2})\b', month_val)
    if found_month and year_match:
        return f"{year_match.group(1)}-{found_month}"
        
    for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y-%m"):
        try:
            dt = datetime.strptime(month_val, fmt)
            return dt.strftime("%Y-%m")
        except ValueError:
            continue
    return month_val[:7]


def fetch_gas(action, payload=None):
    if payload is None:
        payload = {}
    payload['action'] = action
    print(f"[+] Fetching '{action}' from Google Sheets backend...")
    res = requests.post(GAS_URL, json=payload, headers={'Content-Type': 'text/plain;charset=utf-8'})
    res.raise_for_status()
    return res.json()

def insert_supabase(endpoint, data):
    url = f"{SUPABASE_URL}{endpoint}"
    print(f"[+] Inserting {len(data)} records into Supabase {endpoint}...")
    res = requests.post(url, json=data, headers=headers)
    if not res.ok:
        print(f"[!] Error inserting into {endpoint}: {res.text}")
    else:
        print(f"[OK] Successfully populated {endpoint}")

def main():
    print("=" * 60)
    print("        PERIFERRY DATABASE MIGRATION SYSTEM (GAS -> SQL)       ")
    print("=" * 60)
    
    # 1. Fetch Users
    users_res = fetch_gas('get_all_users')
    users = users_res.get('users', [])
    
    # 2. Fetch Manager Data (TimeLogs, Tasks, Summaries, Leaves, Requests)
    manager_res = fetch_gas('get_manager_data')
    time_logs = manager_res.get('time_logs', [])
    tasks = manager_res.get('tasks', [])
    summaries = manager_res.get('summaries', [])
    leaves = manager_res.get('leaves', [])
    leave_requests = manager_res.get('leave_requests', [])
    
    print(f"\n[OK] Retrieved data from Google Sheets:")
    print(f"    - Users: {len(users)}")
    print(f"    - Time Logs: {len(time_logs)}")
    print(f"    - Tasks: {len(tasks)}")
    print(f"    - Daily Work Summaries: {len(summaries)}")
    print(f"    - Leave Balances: {len(leaves)}")
    print(f"    - Leave Requests: {len(leave_requests)}")
    print("-" * 60)

    # Clean existing Supabase transactional tables to avoid duplicates/integrity errors
    print("[+] Cleaning transactional records in Supabase tables...")
    endpoints_to_clean = [
        ('/leave_requests?username=neq.null', '/leave_requests'),
        ('/leaves?id=gt.0', '/leaves'),
        ('/daily_summaries?id=gt.0', '/daily_summaries'),
        ('/tasks?username=neq.null', '/tasks'),
        ('/time_logs?id=gt.0', '/time_logs'),
        ('/users?username=neq.null', '/users')
    ]
    for clean_url, name in endpoints_to_clean:
        res = requests.delete(f"{SUPABASE_URL}{clean_url}", headers=headers)
        if not res.ok:
            print(f"[!] Notice: Failed cleaning {name} (could be empty or RLS constraint): {res.text}")
            
    # Ensure all usernames referenced in transactions exist in the users array
    known_users = {u['username'].strip().lower() for u in users}
    all_usernames = set()
    for l in time_logs:
      if l.get('username'):
        all_usernames.add(l['username'].strip().lower())
    for t in tasks:
      if t.get('username'):
        all_usernames.add(t['username'].strip().lower())
    for s in summaries:
      if s.get('username'):
        all_usernames.add(s['username'].strip().lower())
    for lv in leaves:
      if lv.get('username'):
        all_usernames.add(lv['username'].strip().lower())
    for r in leave_requests:
      if r.get('username'):
        all_usernames.add(r['username'].strip().lower())
        
    for uname in all_usernames:
      if uname not in known_users:
        print(f"[!] Warning: Username '{uname}' has transactional logs but is missing from Users table. Adding automatically.")
        users.append({
          'username': uname,
          'password': f"{uname}@pf",
          'role': 'employee'
        })
        known_users.add(uname)

    # 3. Populate Users
    if users:
      formatted_users = []
      for u in users:
        formatted_users.append({
          'username': u['username'].strip().lower(),
          'password': u['password'],
          'role': u['role']
        })
      insert_supabase('/users', formatted_users)
        
    # 4. Populate Time Logs
    if time_logs:
      formatted_logs = []
      for l in time_logs:
        log_date = l['date'] if l['date'] else datetime.now().strftime("%Y-%m-%d")
        parsed_log_date = parse_date_string(log_date)
        if parsed_log_date:
          log_date = parsed_log_date[:10]
          
        logout = parse_date_string(l['logout_time'], context_date=log_date) if l['logout_time'] else None
        formatted_logs.append({
          'username': l['username'].strip().lower(),
          'date': log_date,
          'login_time': parse_date_string(l['login_time'], context_date=log_date),
          'logout_time': logout,
          'total_hours': float(l['total_hours']) if l['total_hours'] else 0
        })
      insert_supabase('/time_logs', formatted_logs)

    # 5. Populate Tasks
    if tasks:
      formatted_tasks = []
      for t in tasks:
        task_date = t['date'] if t['date'] else datetime.now().strftime("%Y-%m-%d")
        parsed_task_date = parse_date_string(task_date)
        if parsed_task_date:
          task_date = parsed_task_date[:10]
          
        formatted_tasks.append({
          'task_id': t['task_id'],
          'username': t['username'].strip().lower(),
          'date': task_date,
          'title': t['title'],
          'status': t['status'],
          'created_at': parse_date_string(t['created_at'], context_date=task_date),
          'updated_at': parse_date_string(t['updated_at'], context_date=task_date)
        })
      insert_supabase('/tasks', formatted_tasks)

    # 6. Populate Daily Summaries
    if summaries:
      formatted_summaries = []
      for s in summaries:
        sum_date = s['date'] if s['date'] else None
        if not sum_date and s['created_at']:
          parsed_sum_created = parse_date_string(s['created_at'])
          if parsed_sum_created:
            sum_date = parsed_sum_created[:10]
        if not sum_date:
          sum_date = datetime.now().strftime("%Y-%m-%d")
          
        formatted_summaries.append({
          'username': s['username'].strip().lower(),
          'date': sum_date,
          'summary': s['summary'],
          'created_at': parse_date_string(s['created_at'], context_date=sum_date)
        })
      insert_supabase('/daily_summaries', formatted_summaries)

    # 7. Populate Leave Balances
    if leaves:
      grouped_leaves = {}
      for lv in leaves:
        uname = lv['username'].strip().lower()
        mth = format_month_cell(lv['month'])
        if not mth:
          continue
        key = (uname, mth)
        cl = float(lv['casual_leaves']) if lv['casual_leaves'] else 0.0
        ml = float(lv['medical_leaves']) if lv['medical_leaves'] else 0.0
        
        if key in grouped_leaves:
          grouped_leaves[key]['casual_leaves'] += cl
          grouped_leaves[key]['medical_leaves'] += ml
        else:
          grouped_leaves[key] = {
            'username': uname,
            'month': mth,
            'casual_leaves': cl,
            'medical_leaves': ml
          }
      insert_supabase('/leaves', list(grouped_leaves.values()))

    # 8. Populate Leave Requests
    if leave_requests:
      formatted_reqs = []
      for r in leave_requests:
        formatted_reqs.append({
          'request_id': r['request_id'],
          'username': r['username'].strip().lower(),
          'start_date': r['start_date'],
          'end_date': r['end_date'],
          'leave_type': r['leave_type'],
          'reason': r['reason'],
          'status': r['status'],
          'created_at': parse_date_string(r['created_at'])
        })
      insert_supabase('/leave_requests', formatted_reqs)

    print("\n" + "=" * 60)
    print("             MIGRATION COMPLETED SUCCESSFULLY!            ")
    print("=" * 60)

if __name__ == '__main__':
    main()
