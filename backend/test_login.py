import requests
from bs4 import BeautifulSoup

s = requests.Session()
login_url = 'http://localhost:8080/adminlogin'
cred = {'username':'SNJoshi_admin','password':'SNJoshi@123'}

r = s.post(login_url, data=cred, allow_redirects=True, timeout=10)
print('Login POST status:', r.status_code)
# After login, request menu_dashboard
r2 = s.get('http://localhost:8080/admin_dashboard', timeout=10)
print('Admin dashboard GET status:', r2.status_code)
if 'Welcome to' in r2.text:
    print('Login appears successful — dashboard accessible')
else:
    print('Login failed — dashboard shows login or other content')
    print(r2.text[:800])
