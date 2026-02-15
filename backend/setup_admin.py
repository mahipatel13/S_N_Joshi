import pymysql
import sys

try:
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='',
        db='track_serve',
        cursorclass=pymysql.cursors.DictCursor
    )

    cursor = conn.cursor()

    # Check if admin table exists
    cursor.execute("SHOW TABLES LIKE 'admin'")
    if not cursor.fetchone():
        print("ERROR: Admin table does not exist in database")
        conn.close()
        sys.exit(1)

    # Check existing admins
    cursor.execute("SELECT * FROM admin")
    admins = cursor.fetchall()
    
    if admins:
        print("Existing admin users:")
        for admin in admins:
            print(f"  - Phone: {admin.get('phone_no')}, Name: {admin.get('fullname', 'N/A')}")
    else:
        print("No admins found. Creating default admin...")
        cursor.execute(
            "INSERT INTO admin (fullname, phone_no, email_id, password) VALUES (%s, %s, %s, %s)",
            ('S. N. Joshi Admin', '9876543210', 'admin@snjoshi.com', 'admin@123')
        )
        conn.commit()
        print("✓ Default admin created successfully!")
        print("  Phone: 9876543210")
        print("  Password: admin@123")

    conn.close()
    print("\n✓ Admin setup complete!")

except Exception as e:
    print(f"ERROR: {str(e)}")
    sys.exit(1)
