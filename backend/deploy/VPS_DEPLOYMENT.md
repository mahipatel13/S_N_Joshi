# KVM 1 VPS Deployment (Ubuntu)

This app is prepared to run on a KVM 1 VPS using:
- Nginx (public web server)
- Gunicorn (Flask app server on `127.0.0.1:8080`)
- MySQL (local or external)

## 1) Upload project
Place project at:
`/var/www/hs/backend`

## 2) Configure environment
Create `.env` from template:
```bash
cd /var/www/hs/backend
cp .env.example .env
```

Edit `.env` with real values.

## 3) Database setup
If MySQL is local, create DB/user:
```sql
CREATE DATABASE track_serve;
CREATE USER 'trackserve_user'@'localhost' IDENTIFIED BY 'strong_password_here';
GRANT ALL PRIVILEGES ON track_serve.* TO 'trackserve_user'@'localhost';
FLUSH PRIVILEGES;
```

Import schema/data:
```bash
mysql -u trackserve_user -p track_serve < /var/www/hs/backend/track_serve.sql
```

## 4) Run setup script
```bash
cd /var/www/hs/backend
sudo bash deploy/setup_vps.sh
```

## 5) DNS and SSL
- Point your domain A record to VPS public IP.
- Update `server_name` in `deploy/nginx.conf`, then copy it again.
- Install SSL:
```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

## 6) Verify
```bash
curl http://127.0.0.1:8080/health
sudo systemctl status hs
sudo systemctl status nginx
```
