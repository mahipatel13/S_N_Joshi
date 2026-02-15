import requests

urls = ['/menu_dashboard','/add_menu','/submit']
for u in urls:
    try:
        r = requests.get('http://localhost:8080'+u, timeout=10)
        print('\nURL:', u, 'Status:', r.status_code)
        text = r.text
        print(text[:2000])
    except Exception as e:
        print('\nURL:', u, 'ERROR:', e)
