import os, sys
sys.stdout.reconfigure(encoding='utf-8')
from dotenv import load_dotenv
load_dotenv()

url = os.getenv('DATABASE_URL')
print('DATABASE_URL loaded:', url[:80] + '...' if url and len(url) > 80 else url)

if not url or 'postgresql' not in url:
    print('ERROR: DATABASE_URL is not set to PostgreSQL!')
    sys.exit(1)

import psycopg2

try:
    print('\nConnecting to Supabase...')
    conn = psycopg2.connect(url, sslmode='require')
    cur = conn.cursor()

    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
    tables = [t[0] for t in cur.fetchall()]
    print('[OK] CONNECTED TO SUPABASE SUCCESSFULLY!')
    print('Tables found:', tables)

    if 'users' in tables:
        cur.execute('SELECT email, name FROM users LIMIT 5')
        users = cur.fetchall()
        print('Users in DB:', users)
    else:
        print('No users table found!')

    conn.close()
    print('\nSupabase is fully working as the database.')

except Exception as e:
    print(f'[FAILED] Connection error: {e}')
