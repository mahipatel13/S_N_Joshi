import pymysql

conn = pymysql.connect(host='localhost', port=3306, user='root', password='', db='track_serve')
cur = conn.cursor()
cur.execute('SELECT id, fullname, phone_no, email_id, password FROM admin')
rows = cur.fetchall()
if not rows:
    print('No admin rows found')
else:
    for r in rows:
        print('ID:', r[0])
        print('Name:', r[1])
        print('Phone:', r[2])
        print('Email:', r[3])
        print('Password:', r[4])
        print('-'*40)
conn.close()
