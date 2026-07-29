import requests

SUPABASE_URL = 'https://oijgqcmdofvicworgeir.supabase.co/rest/v1'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9pamdxY21kb2Z2aWN3b3JnZWlyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODQ3NzYyMDAsImV4cCI6MjEwMDM1MjIwMH0.FnLH_PrbjEUvaPTC8hr-jtUeaAol31ReUKH6k-SQgdU'

headers = {
    'apikey': SUPABASE_KEY,
    'Authorization': f'Bearer {SUPABASE_KEY}',
    'Content-Type': 'application/json'
}

def main():
    print("[+] Clearing transaction tables...")
    for endpoint in ['/leave_requests?username=neq.null', '/leaves?id=gt.0', '/daily_summaries?id=gt.0', '/tasks?username=neq.null', '/time_logs?id=gt.0']:
        res = requests.delete(f"{SUPABASE_URL}{endpoint}", headers=headers)
        print(f"    - Cleaned {endpoint}: {res.status_code}")

    print("[+] Wiping users...")
    requests.delete(f"{SUPABASE_URL}/users?username=neq.null", headers=headers)

    print("[+] Seeding fresh default users...")
    users = [
        {'username': 'anurag', 'password': 'anurag@pf', 'role': 'employee,manager', 'status': 'offline'},
        {'username': 'hana', 'password': '8376ti.ger3110', 'role': 'employee,manager,developer', 'status': 'offline'},
        {'username': 'soumita', 'password': 'soumita@pf', 'role': 'employee', 'status': 'offline'},
        {'username': 'nishant', 'password': 'nishant@pf', 'role': 'employee,manager,developer', 'status': 'offline'},
        {'username': 'sai', 'password': 'sai@PF', 'role': 'employee', 'status': 'offline'},
        {'username': 'edyn', 'password': 'edyn@pf', 'role': 'employee', 'status': 'offline'},
        {'username': 'mohama', 'password': 'mohama@pf', 'role': 'employee,manager,developer', 'status': 'offline'}
    ]
    res = requests.post(f"{SUPABASE_URL}/users", json=users, headers=headers)
    if res.ok:
        print("[OK] Database reset complete! Start fresh!")
    else:
        print(f"[!] Error seeding users: {res.text}")

if __name__ == '__main__':
    main()
