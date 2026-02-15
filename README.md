# S. N. Joshi. Mess - Admin System
## Refactored & Customized Version

### What's New ✨

1. **Single Session Login** - Only one admin can login at a time. Previous session auto-logs out
2. **Three Core Features**:
3. **Menu Management** - Add, Update, Delete breakfast, lunch, dinner menus
4. **Grocery & Vegetable Tracker** - Track purchases and usage
5. **Raw Material Management** - Manage groceries and vegetables efficiently

### How to Run

1. **Open Terminal/Command Prompt** in the project directory
2. **Run the Flask app:**

   python main.py
   

3. **Access the application:**
   - Open your browser and go to: `http://localhost:8080`
   - You'll be redirected to the admin login page automatically

### Features Overview

#### 1. Menu Management (`/menu_dashboard`)
- **Add Menu** - Create new breakfast/lunch/dinner menus for weekly cycles
- **Update Menu** - Modify existing menus
- **Delete Menu** - Remove outdated menus
- **View Weekly Menu** - See complete week's menu
- **Download PDF/Excel** - Export menus as PDF/Excel

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

### Troubleshooting

**Problem:** "Port 8080 already in use"
- **Solution:** Close other applications using port 8080 or change port in `main.py` line (last line)

**Problem:** "Connection refused"
- **Solution:** Ensure MySQL is running: `mysql -u root -p` (should work)

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

**Version:** 1.0  
**Last Updated:** February 2026  
**Customized for:** S. N. Joshi. Mess
=======
# S_N_Joshi
