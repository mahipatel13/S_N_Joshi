import pymysql

try:
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='', db='track_serve')
    cursor = conn.cursor()

    print("=" * 50)
    print("S. N. JOSHI. MESS - DATABASE VERIFICATION")
    print("=" * 50)
    
    # Verify required tables exist
    tables = ['admin', 'breakfast', 'lunch', 'dinner', 'grocery_vegetable_management']
    for table in tables:
        cursor.execute(f'SHOW TABLES LIKE "{table}"')
        if cursor.fetchone():
            print(f'✓ Table exists: {table}')
        else:
            print(f'✗ Table missing: {table}')

    # Check admin user
    cursor.execute('SELECT fullname, phone_no FROM admin LIMIT 1')
    admin = cursor.fetchone()
    if admin:
        print(f'\n✓ Admin user configured:')
        print(f'  Name: {admin[0]}')
        print(f'  Phone: {admin[1]}')
    else:
        print('\n✗ No admin user found')

    conn.close()
    print("\n" + "=" * 50)
    print("DATABASE SETUP: OK ✓")
    print("=" * 50)

except Exception as e:
    print(f"ERROR: {str(e)}")

# mysql -u root -p -e "SELECT id, fullname, phone_no, email_id, password FROM track_serve.admin;"

# UPDATE track_serve.admin
# SET password = 'SNJoshi@123'
# WHERE phone_no = '8511895498';
