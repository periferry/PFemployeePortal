import requests
import random

SUPABASE_URL = 'https://oijgqcmdofvicworgeir.supabase.co/rest/v1'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9pamdxY21kb2Z2aWN3b3JnZWlyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODQ3NzYyMDAsImV4cCI6MjEwMDM1MjIwMH0.FnLH_PrbjEUvaPTC8hr-jtUeaAol31ReUKH6k-SQgdU'

headers = {
    'apikey': SUPABASE_KEY,
    'Authorization': f'Bearer {SUPABASE_KEY}',
    'Content-Type': 'application/json'
}

def main():
    print("[+] Wiping transactional database tables...")
    for endpoint in ['/leave_requests?username=neq.null', '/leaves?id=gt.0', '/daily_summaries?id=gt.0', '/tasks?username=neq.null', '/time_logs?id=gt.0']:
        requests.delete(f"{SUPABASE_URL}{endpoint}", headers=headers)

    print("[+] Wiping and re-seeding Users list (including 'edyn')...")
    requests.delete(f"{SUPABASE_URL}/users?username=neq.null", headers=headers)
    users = [
        {'username': 'anurag', 'password': 'anurag@pf', 'role': 'employee,manager'},
        {'username': 'hana', 'password': '8376ti.ger3110', 'role': 'employee,manager,developer'},
        {'username': 'soumita', 'password': 'soumita@pf', 'role': 'employee'},
        {'username': 'nishant', 'password': 'nishant@pf', 'role': 'employee,manager'},
        {'username': 'sai', 'password': 'sai@PF', 'role': 'employee'},
        {'username': 'edyn', 'password': 'edyn@pf', 'role': 'employee'}
    ]
    requests.post(f"{SUPABASE_URL}/users", json=users, headers=headers)

    print("[+] Seeding Leave Balances for July 2026...")
    leaves = []
    for u in users:
        uname = u['username']
        cl = 1.0
        ml = 0.0 if uname == 'hana' else 1.0
        leaves.append({
            'username': uname,
            'month': '2026-07',
            'casual_leaves': cl,
            'medical_leaves': ml
        })
    requests.post(f"{SUPABASE_URL}/leaves", json=leaves, headers=headers)

    print("[+] Seeding Login Times for 2026-07-23...")
    time_logs = [
        {'username': 'anurag', 'date': '2026-07-23', 'login_time': '2026-07-23T09:00:26Z', 'logout_time': None, 'total_hours': 0},
        {'username': 'edyn', 'date': '2026-07-23', 'login_time': '2026-07-23T09:34:43Z', 'logout_time': None, 'total_hours': 0},
        {'username': 'hana', 'date': '2026-07-23', 'login_time': '2026-07-23T09:27:11Z', 'logout_time': None, 'total_hours': 0},
        {'username': 'soumita', 'date': '2026-07-23', 'login_time': '2026-07-23T09:30:11Z', 'logout_time': None, 'total_hours': 0}
    ]
    requests.post(f"{SUPABASE_URL}/time_logs", json=time_logs, headers=headers)

    print("[+] Seeding Tasks for 2026-07-23...")
    # Deduplicated task status resolution
    raw_tasks = [
        ('anurag', 'Respond on mail and clear Inbox', 'todo'),
        ('anurag', 'Respond on mail and clear Inbox', 'todo'),
        ('anurag', 'Respond on mail and clear Inbox', 'todo'),
        ('anurag', 'Respond on mail and clear Inbox', 'completed'),
        ('anurag', 'Work on Job Fair Sheet', 'inprogress'),
        ('hana', 'mails', 'completed'),
        ('hana', 'Kiosk proposal', 'todo'),
        ('hana', 'wall mosaic proposal/ printables for corporates', 'todo'),
        ('hana', 'update details in team page', 'todo'),
        ('anurag', 'Internal Meeting', 'todo'),
        ('anurag', 'Schedule Second Round for Internal Hiring', 'todo'),
        ('anurag', 'Prepare offer letter for new a joinee and issued', 'inprogress'),
        ('anurag', 'Profile share with McKinsey', 'todo'),
        ('anurag', 'Work on My Inbox', 'inprogress'),
        ('hana', 'fix the employee portal', 'inprogress'),
        ('anurag', 'Work on Revive Sheet', 'todo')
    ]

    # Process tasks following the resolution rules:
    # 1. Ignore repeat tasks with same status
    # 2. Update status of repeated tasks if different (using latest status)
    task_dict = {}
    for user, title, status in raw_tasks:
        key = (user, title)
        # Always overwrite with latest occurrence
        task_dict[key] = status

    tasks_payload = []
    for (user, title), status in task_dict.items():
        task_id = f"TSK-{random.randint(100000, 999999)}"
        tasks_payload.append({
            'task_id': task_id,
            'username': user,
            'date': '2026-07-23',
            'title': title,
            'status': status,
            'created_at': '2026-07-23T09:00:00Z',
            'updated_at': '2026-07-23T09:00:00Z'
        })
    
    requests.post(f"{SUPABASE_URL}/tasks", json=tasks_payload, headers=headers)
    print("[OK] Database successfully initialized for today!")

if __name__ == '__main__':
    main()
