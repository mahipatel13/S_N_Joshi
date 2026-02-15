<<<<<<< HEAD
# S. N. Joshi. Mess - Admin System
## Refactored & Customized Version

### What's New ✨

1. **Admin-Only Functionality** - Removed all student, faculty, and non-hostel user interfaces
2. **Single Session Login** - Only one admin can login at a time. Previous session auto-logs out
3. **Custom Branding** - All pages display "S. N. Joshi. Mess"
4. **Port Changed to 8080** - Changed from port 5000 to 8080 for better compatibility
5. **Three Core Features**:
   - **Menu Management** - Add, Update, Delete breakfast, lunch, dinner menus
   - **Grocery & Vegetable Tracker** - Track purchases and usage
   - **Raw Material Management** - Manage groceries and vegetables efficiently

### Admin Credentials

**Phone:** `7862017545`  
**Password:** (Your existing password)

### How to Run

1. **Open Terminal/Command Prompt** in the project directory
2. **Run the Flask app:**
   ```bash
   python main.py
   ```

3. **Access the application:**
   - Open your browser and go to: `http://localhost:8080`
   - You'll be redirected to the admin login page automatically

### Features Overview

#### 1. Menu Management (`/menu_dashboard`)
- **Add Menu** - Create new breakfast/lunch/dinner menus for weekly cycles
- **Update Menu** - Modify existing menus
- **Delete Menu** - Remove outdated menus
- **View Weekly Menu** - See complete week's menu
- **Download PDF** - Export menus as PDF

#### 2. Grocery & Vegetable Management (`/g_v`)
- **Add Entry** - Record grocery and vegetable purchases
- **Track by Meal** - Organize by breakfast, lunch, dinner
- **View Reports** - Generate detailed reports
- **Delete Entries** - Remove incorrect entries

#### 3. Raw Material Tracker
- Monitor all grocery items used
- Track vegetables and other raw materials
- Generate reports by date and meal type

### Security Features

✓ Single session per admin (prevents multiple logins)  
✓ Session-based authentication  
✓ Auto-logout on duplicate login attempts  
✓ Secure database connection  

### Important Notes

1. **Database**: Ensure MySQL is running with `track_serve` database
2. **Port 8080**: Make sure port 8080 is not being used by another application
3. **Environment**: Works with Python 3.7+ with virtual environment
4. **Browser**: Works on all modern browsers (Chrome, Firefox, Safari, Edge)

### Troubleshooting

**Problem:** "Port 8080 already in use"
- **Solution:** Close other applications using port 8080 or change port in `main.py` line (last line)

**Problem:** "Connection refused"
- **Solution:** Ensure MySQL is running: `mysql -u root -p` (should work)

**Problem:** "Admin login shows error"
- **Solution:** Verify admin exists in database with credentials: Phone `7862017545`

### Database Setup

If you need to add another admin:

```sql
INSERT INTO admin (fullname, phone_no, email_id, password) 
VALUES ('Admin Name', '9876543210', 'email@example.com', 'password123');
```

### File Structure

```
HS/
├── main.py                  (Flask application - PORT 8080)
├── requirements.txt         (Dependencies)
├── setup_admin.py          (Admin setup script)
├── templates/              (HTML templates)
│   ├── admin_login.html
│   ├── admin_dashboard.html
│   ├── menu_dashboard.html
│   ├── add_menu_dashboard.html
│   ├── g_v.html
│   └── ... (other templates)
├── static/                 (CSS, JS, Images)
│   ├── css/
│   ├── js/
│   └── images/
└── .venv/                  (Virtual environment)
```

### Contact & Support

For issues or questions, check:
1. MySQL connection settings
2. Database tables exist
3. Admin credentials are correct
4. Port 8080 is available

---

**Version:** 2.0 (Refactored for Admin Only)  
**Last Updated:** February 2026  
**Customized for:** S. N. Joshi. Mess
=======
# S_N_Joshi
>>>>>>> 5a3a1b19325f174d40f9a584d4e56117772f7348
