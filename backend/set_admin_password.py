import pymysql

NEW_PW = 'SNJoshi@123'
PHONE = '8511895498'

conn = pymysql.connect(host='localhost', port=3306, user='root', password='', db='track_serve')
cur = conn.cursor()
cur.execute("UPDATE admin SET password=%s WHERE phone_no=%s", (NEW_PW, PHONE))
conn.commit()
print('Updated admin password for', PHONE)
cur.execute('SELECT id, fullname, phone_no, password FROM admin WHERE phone_no=%s', (PHONE,))
print(cur.fetchone())
conn.close()
