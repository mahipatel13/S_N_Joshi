import requests

LOGIN = {'phone_no':'8511895498','password':'SNJoshi@123'}
BASE = 'http://localhost:8080'

s = requests.Session()
try:
    s.post(BASE + '/adminlogin', data=LOGIN, timeout=10)
    r = s.get(BASE + '/g_v_report', timeout=10)
    print('status', r.status_code)
    text = r.text
    marker = 'name="id" value="'
    idx = text.find(marker)
    if idx == -1:
        print('No id inputs found in report HTML')
    else:
        start = idx + len(marker)
        end = text.find('"', start)
        print('Found id sample:', text[start:end])
except Exception as e:
    print('Error:', e)
