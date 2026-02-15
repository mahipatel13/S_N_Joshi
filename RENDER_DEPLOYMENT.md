# S. N. Joshi. Mess - Deployment Guide (Render.com)

## Pre-Deployment Checklist

- [x] Admin-only refactored (menu, timetable, grocery tracker)
- [x] Single-session login enforcement (UUID-based)
- [x] Local Bootstrap CSS (avoids CDN Tracking Prevention blocking)
- [x] Database connection configuration (supports environment variables)
- [x] Delete row functionality (fixed with primary key support)
- [x] Production-ready app settings (debug disabled in production)
- [x] Gunicorn WSGI server configured (Procfile)
- [x] Requirements.txt with pinned versions

## Environment Variables Required on Render

Set these in your Render dashboard under **Environment Variables**:

```
DB_HOST=<your-mysql-host>
DB_PORT=3306
DB_USER=<your-mysql-username>
DB_PASSWORD=<your-mysql-password>
DB_NAME=track_serve
SECRET_KEY=<strong-random-string>
ENVIRONMENT=production
PORT=10000
```

### Example values:
- `DB_HOST`: Your MySQL server address (e.g., `db.example.com`, or AWS RDS endpoint)
- `SECRET_KEY`: Generate with: `python -c "import secrets; print(secrets.token_hex(32))"`
- `PORT`: Render assigns a port automatically; use this if you need to override it

## Steps to Deploy on Render

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "S.N. Joshi Mess - Admin System"
   git remote add origin https://github.com/YOUR_USERNAME/sns-mess.git
   git push -u origin main
   ```

2. **Create a Render Web Service**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Select your GitHub repository
   - Set:
     - **Name**: `sns-mess-admin` (or your choice)
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn main:app`
     - **Instance Type**: Free tier or Paid (Starter/Standard)

3. **Configure Environment Variables**
   - In Render dashboard, go to your service → **Environment**
   - Add all the environment variables listed above

4. **Deploy**
   - Click "Create Web Service"
   - Render will automatically deploy when you push to GitHub

## Post-Deployment Issues (Common FAQs)

### 1. **"Database connection refused" error**
   **Cause**: MySQL credentials incorrect or host unreachable from Render.
   
   **Solution**:
   - Verify `DB_HOST`, `DB_USER`, `DB_PASSWORD` are correct.
   - If using local MySQL, it won't be accessible from Render. Use a cloud MySQL service:
     - AWS RDS (Amazon Relational Database Service)
     - Google Cloud SQL
     - DigitalOcean Managed Databases
     - PlanetScale (MySQL-compatible, serverless)

### 2. **"Static files (CSS, JS) not loading" (404 errors)**
   **Cause**: Render doesn't automatically serve static files in certain configurations.
   
   **Solution**:
     - Static files are already local (`/static` folder), so this is pre-configured.
     - If needed, use Render's static file support or a CDN (Cloudflare, AWS S3).

### 3. **"Login session expires too quickly"**
   **Cause**: Render restarts the app periodically; in-memory sessions (`ACTIVE_SESSIONS`) are lost.
   
   **Solution**:
   - For persistent sessions, implement Redis:
     ```bash
     # In Render, add Redis service and set REDIS_URL env var
     # Then update main.py to use Flask-Session with Redis
     ```
   - Or accept that users need to re-login after 24+ hours when the free tier restarts.

### 4. **"File uploads or reports not saving"**
   **Cause**: Render has ephemeral file system (deleted on restart).
   
   **Solution**:
   - Generated PDFs are served directly; no persistent storage needed.
   - If you need to save uploads, use AWS S3, Google Cloud Storage, or similar.

### 5. **"Slow initial load / timeout on first request"**
   **Cause**: Free tier Render instances sleep after 15 minutes of inactivity.
   
   **Solution**:
   - Upgrade to Paid tier (Starter: $7/month) for always-on.
   - Or accept a 10–30 second delay on the first request after sleeep.

### 6. **"Port binding error: 'Port 8080 already in use'"**
   **Cause**: Render assigns a dynamic port; this should be handled automatically.
   
   **Solution**:
   - The app is already set to read `PORT` from environment; no action needed.

### 7. **"Tracking Prevention still blocks Bootstrap CSS"**
   **Cause**: CSS is served locally, but user's browser still blocks external resources.
   
   **Solution**:
   - Bootstrap is now local (`/static/css/bootstrap.min.css`), so this is resolved.
   - If CDN issues persist, ensure all external scripts are removed (already done).

### 8. **"Delete grocery/vegetable entries fails"**
   **Cause**: Database transaction issues or session expired.
   
   **Solution**:
   - Delete now works by primary key (`id`), which is more reliable.
   - If failing, check DB logs and ensure session is valid.

### 9. **"Can't log in: 'Unexpected token in JSON at position 0'"**
   **Cause**: Server returned HTML (error page) instead of JSON.
   
   **Solution**:
   - Check Flask logs on Render (`View Logs` in dashboard).
   - Ensure `DB_*` environment variables are set correctly.

### 10. **"Need to generate a new admin password for production"**
   **To set a new admin password after deployment**:
   - Use Render's SSH option (if available) or a helper route.
   - Or, connect to your cloud MySQL instance directly and run:
     ```sql
     UPDATE admin SET password = 'NewPassword@123' WHERE phone_no = '7862017545';
     ```

---

## Monitoring & Debugging

- **View Logs**: Render dashboard → Service → "Logs" tab
- **Check Status**: Monitor CPU, Memory, Network usage
- **Restart Service**: Click "Restart Instance" if needed
- **View Events**: Check deployment history and error messages

## Summary

✅ **Your app is production-ready:**
- Environment-aware configuration
- Database connection flexible (local or cloud)
- Static files served locally
- Gunicorn WSGI server set up
- Session management integrated
- Delete functionality fixed

🚀 **Next step**: Push to GitHub and create a Render Web Service. Deploy takes 2–5 minutes!

---

**Questions during/after deployment?** Check the log output in the Render dashboard for specific error messages.
