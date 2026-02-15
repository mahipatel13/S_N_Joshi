from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_file
import pymysql.cursors
from pymysql.cursors import DictCursor
import random
from datetime import date, datetime
import mysql.connector
import qrcode
import io
import subprocess
import pandas as pd
from fpdf import FPDF
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from collections import defaultdict, OrderedDict
import uuid

app = Flask(__name__)
app.secret_key = 'sn_joshi_mess_secret_key_2024'

# Store active sessions
ACTIVE_SESSIONS = {}

# Mess Name
MESS_NAME = "S. N. Joshi. Mess"

# Function to connect to MySQL
def get_db_connection():
    try:
        connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='',
            db='track_serve',
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except pymysql.MySQLError as e:
        print(f"Error connecting to MySQL: {e}")
        return None

@app.route('/')
def home():
    return redirect(url_for('adminlogin'))

@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        phone_no = request.form['phone_no']
        password = request.form['password']

        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query = "SELECT * FROM admin WHERE phone_no = %s AND password = %s"
                cursor.execute(query, (phone_no, password))
                user = cursor.fetchone()

                if user:
                    # Check if this admin is already logged in elsewhere
                    admin_id = user['id'] if 'id' in user else phone_no
                    
                    # If already logged in, logout the previous session
                    if admin_id in ACTIVE_SESSIONS:
                        old_session_id = ACTIVE_SESSIONS[admin_id]
                        # Clear old session (if needed)
                        print(f"Logging out previous session for admin {admin_id}")
                    
                    # Create new session
                    session_id = str(uuid.uuid4())
                    ACTIVE_SESSIONS[admin_id] = session_id
                    
                    session['admin_id'] = admin_id
                    session['phone_no'] = phone_no
                    session['session_id'] = session_id
                    session['logged_in'] = True
                    
                    flash("Login successful! Welcome to S. N. Joshi. Mess", "success")
                    return redirect(url_for('admin_dashboard'))
                else:
                    return render_template('admin_login.html', error="Invalid phone number or password")

            except pymysql.MySQLError as e:
                print(f"Database error: {e}")
                return render_template('admin_login.html', error="Error while checking credentials")
            finally:
                cursor.close()
                connection.close()
        else:
            return render_template('admin_login.html', error="Failed to connect to the database")

    return render_template('admin_login.html', mess_name=MESS_NAME)

@app.before_request
def check_session():
    """Check if user session is valid"""
    if 'logged_in' in session:
        admin_id = session.get('admin_id')
        session_id = session.get('session_id')
        
        # Verify session is still active
        if admin_id not in ACTIVE_SESSIONS or ACTIVE_SESSIONS[admin_id] != session_id:
            session.clear()
            flash("Your session has been terminated. Please login again.", "warning")

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('adminlogin'))
    return render_template("admin_dashboard.html", mess_name=MESS_NAME)

@app.route('/logout')
def logout():
    if 'admin_id' in session:
        admin_id = session['admin_id']
        if admin_id in ACTIVE_SESSIONS:
            del ACTIVE_SESSIONS[admin_id]
    
    session.clear()
    flash("You have been logged out successfully.", "success")
    return redirect(url_for('adminlogin'))

# Menu Management Routes
@app.route('/menu_dashboard')
def menu_dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('adminlogin'))
    return render_template('menu_dashboard.html', mess_name=MESS_NAME)

@app.route('/add_menu')
def add_menu():
    if 'logged_in' not in session:
        return redirect(url_for('adminlogin'))
    return render_template('add_menu_dashboard.html', mess_name=MESS_NAME)

@app.route('/submit', methods=['POST'])
def submit():
    if 'logged_in' not in session:
        return redirect(url_for('adminlogin'))
        
    meal_type = request.form.get('meal_type')
    from_date = request.form.get("fromDate")
    to_date = request.form.get("toDate")

    print("From Date:", from_date)
    print("To Date:", to_date)

    # Fetch meal data for all days
    data = {
        'Monday': request.form.get('Monday'),
        'Tuesday': request.form.get('Tuesday'),
        'Wednesday': request.form.get('Wednesday'),
        'Thursday': request.form.get('Thursday'),
        'Friday': request.form.get('Friday'),
        'Saturday': request.form.get('Saturday'),
        'Sunday': request.form.get('Sunday')
    }

    # Identify the table to store meal data
    table_name = ""
    if meal_type == 'breakfast':
        table_name = "breakfast"
    elif meal_type == 'lunch':
        table_name = "lunch"
    elif meal_type == 'dinner':
        table_name = "dinner"

    if table_name:
        connection = get_db_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    sql = f"""
                        INSERT INTO {table_name}
                        (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, from_date, to_date)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(sql, tuple(data.values()) + (from_date, to_date))
                    connection.commit()
                    print(f"Data successfully inserted into {table_name}")
                    flash(f"Menu for {meal_type.upper()} added successfully!", "success")
                    return render_template("add_menu_dashboard.html", mess_name=MESS_NAME)
            except Exception as e:
                print("Database Error:", e)
                flash(f"Error: {str(e)}", "danger")
            finally:
                connection.close()

    return redirect(url_for('add_menu'))

def get_today_menu():
    try:
        conn = get_db_connection()
        if conn is None:
            return [{"Meal_Type": "Error", "Today_Menu": "MySQL Connection not available"}]

        cursor = conn.cursor()

        today = date.today().strftime('%Y-%m-%d')
        print(f"Today's Date: {today}")

        # Fetch the Weekday Name
        cursor.execute("SELECT DAYNAME(%s) AS weekday", (today,))
        result = cursor.fetchone()

        if not result or "weekday" not in result:
            print("Error: Could not retrieve weekday from MySQL")
            return [{"Meal_Type": "Error", "Today_Menu": "Could not retrieve weekday"}]

        weekday = result["weekday"]

        # Check if weekday column exists
        cursor.execute("SHOW COLUMNS FROM breakfast")
        breakfast_columns = [col["Field"] for col in cursor.fetchall()]

        if weekday not in breakfast_columns:
            print(f"Error: Column `{weekday}` does not exist in table.")
            return [{"Meal_Type": "Error", "Today_Menu": f"Column `{weekday}` not found"}]

        # Fetch Today's Menu
        query = f"""
        SELECT `{weekday}` AS Today_Menu, 'Breakfast' AS Meal_Type FROM breakfast 
        WHERE %s BETWEEN FROM_DATE AND TO_DATE
        UNION
        SELECT `{weekday}` AS Today_Menu, 'Lunch' AS Meal_Type FROM lunch 
        WHERE %s BETWEEN FROM_DATE AND TO_DATE
        UNION
        SELECT `{weekday}` AS Today_Menu, 'Dinner' AS Meal_Type FROM dinner 
        WHERE %s BETWEEN FROM_DATE AND TO_DATE;
        """
        cursor.execute(query, (today, today, today))
        result = cursor.fetchall()

        cursor.close()
        conn.close()

        return result if result else [{"Meal_Type": "No Data", "Today_Menu": "No menu available"}]
    
    except pymysql.MySQLError as e:
        print("SQL Error:", e)
        return [{"Meal_Type": "Error", "Today_Menu": str(e)}]

@app.route('/menu_show', methods=['GET', 'POST'])
def menu_show():
    if 'logged_in' not in session:
        return redirect(url_for('adminlogin'))
        
    today_menu = get_today_menu()
    return render_template("menu.html", menu=today_menu, mess_name=MESS_NAME)

# Function to Fetch Weekly Data
def fetch_weekly_data():
    today_date = datetime.today().strftime('%Y-%m-%d')
    connection = get_db_connection()
    
    if not connection:
        return None, [], [], []

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT FROM_DATE, TO_DATE FROM breakfast WHERE %s BETWEEN FROM_DATE AND TO_DATE LIMIT 1",
                (today_date,)
            )
            date_range = cursor.fetchone()

            cursor.execute("SELECT * FROM breakfast WHERE %s BETWEEN FROM_DATE AND TO_DATE", (today_date,))
            breakfast_data = cursor.fetchall()

            cursor.execute("SELECT * FROM lunch WHERE %s BETWEEN FROM_DATE AND TO_DATE", (today_date,))
            lunch_data = cursor.fetchall()

            cursor.execute("SELECT * FROM dinner WHERE %s BETWEEN FROM_DATE AND TO_DATE", (today_date,))
            dinner_data = cursor.fetchall()

        return date_range, breakfast_data, lunch_data, dinner_data
    except Exception as e:
        print("Database Error:", e)
        return None, [], [], []
    finally:
        connection.close()

@app.route('/weekly_data', methods=['GET'])
def weekly_data():
    if 'logged_in' not in session:
        return redirect(url_for('adminlogin'))
        
    date_range, breakfast, lunch, dinner = fetch_weekly_data()
    return render_template('weakly_menu.html', date_range=date_range, breakfast=breakfast, lunch=lunch, dinner=dinner, mess_name=MESS_NAME)

# PDF Generation Class
class CustomPDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, f"{MESS_NAME} - Weekly Menu", ln=True, align="C")
        self.ln(5)

# Function to Generate PDF
def generate_pdf_menu(from_date, meals):
    file_name = f"{from_date}_Menu.pdf"
    
    pdf = CustomPDF(orientation="L", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.add_page()

    # Set Title
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"Weekly Menu ({from_date})", ln=True, align="C")
    pdf.ln(5)

    # Column headers
    column_headers = ["Meal Type", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    column_widths = [40] + [35] * 7

    # Header Row
    pdf.set_font("Arial", "B", 11)
    for i, header in enumerate(column_headers):
        pdf.cell(column_widths[i], 10, header, border=1, align="C")
    pdf.ln()

    # Function to add meal rows dynamically
    def add_meal_row(meal_name, meal_data):
        pdf.set_font("Arial", size=10)
        pdf.cell(column_widths[0], 10, meal_name, border=1, align="C")

        for day in column_headers[1:]:
            pdf.cell(column_widths[column_headers.index(day)], 10, meal_data.get(day, ""), border=1, align="C")
        pdf.ln()

    for meal_type, meal_data in meals.items():
        if not isinstance(meal_data, dict):
            print(f"Error: Expected dict for {meal_type}, but got {type(meal_data)}")
            continue
        add_meal_row(meal_type, meal_data)

    pdf.output(file_name)
    return file_name

# Function to Extract Meal Data
def extract_meal_data(meal_data):
    if not meal_data:
        return {day: "" for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}

    if isinstance(meal_data[0], dict):
        meal_dict = meal_data[0]
    elif isinstance(meal_data[0], tuple):
        column_names = ["id", "from_date", "to_date", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        meal_dict = dict(zip(column_names, meal_data[0]))
    else:
        print(f"Unexpected meal_data format: {meal_data[0]}")
        return {day: "" for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}

    return {day: meal_dict.get(day, "") for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}

# Route to Download Weekly Menu as PDF
@app.route('/download_menu_pdf', methods=['GET'])
def download_menu_pdf():
    if 'logged_in' not in session:
        return redirect(url_for('adminlogin'))
        
    date_range, breakfast, lunch, dinner = fetch_weekly_data()

    if not date_range:
        return jsonify({"error": "No data found for the current week"}), 404

    from_date = str(date_range["FROM_DATE"])

    print(f"Generating PDF for: {from_date}")

    meals = {
        "Breakfast": extract_meal_data(breakfast),
        "Lunch": extract_meal_data(lunch),
        "Dinner": extract_meal_data(dinner),
    }

    pdf_file = generate_pdf_menu(from_date, meals)
    return send_file(pdf_file, as_attachment=True)

# Fetch all menu data for deletion
@app.route('/delete_menu', methods=['GET'])
def delete_menu():
    if 'logged_in' not in session:
        return redirect(url_for('adminlogin'))
        
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            breakfast_query = "SELECT * FROM breakfast"
            lunch_query = "SELECT * FROM lunch"
            dinner_query = "SELECT * FROM dinner"

            cursor.execute(breakfast_query)
            breakfast_data = cursor.fetchall()

            cursor.execute(lunch_query)
            lunch_data = cursor.fetchall()

            cursor.execute(dinner_query)
            dinner_data = cursor.fetchall()

        return render_template('delete_menu.html', breakfast=breakfast_data, lunch=lunch_data, dinner=dinner_data, mess_name=MESS_NAME)
    except Exception as e:
        print("Database Error:", e)
        return "Error fetching data"
    finally:
        if connection:
            connection.close()

# Handle menu deletion
@app.route('/delete_menu/<meal>/<int:menu_id>', methods=['POST'])
def delete_menu_item(meal, menu_id):
    if 'logged_in' not in session:
        return redirect(url_for('adminlogin'))
        
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = f"DELETE FROM {meal} WHERE id = %s"
            cursor.execute(query, (menu_id,))
            connection.commit()
        
        flash(f"Menu item deleted successfully", "success")
        return jsonify({"message": "Menu item deleted successfully"}), 200
    except Exception as e:
        print("Error deleting menu item:", e)
        return jsonify({"error": "Failed to delete"}), 500
    finally:
        if connection:
            connection.close()

# Grocery & Vegetable Management Routes
@app.route("/g_v_list", methods=["GET", "POST"])
def g_v_list():
    if 'logged_in' not in session:
        return redirect(url_for('adminlogin'))
        
    if request.method == "GET":
        meal_type = request.args.get("meal_type")
        menu_items = []
        if meal_type in ["breakfast", "lunch", "dinner"]:
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                today = datetime.now().date()
                weekday = today.strftime('%A')

                query = f"""
                    SELECT `{weekday}` AS day_value
                    FROM `{meal_type}`
                    WHERE `{weekday}` IS NOT NULL AND `{weekday}` != ''
                    AND from_date <= %s AND to_date >= %s
                """

                cursor.execute(query, (today, today))
                results = cursor.fetchall()

                for row in results:
                    if row['day_value']:
                        items = row['day_value'].split('\n')
                        menu_items.extend([item.strip() for item in items if item.strip()])

                cursor.close()
                conn.close()

            except pymysql.MySQLError as e:
                return f"Database error while fetching: {str(e)}", 500

        return render_template("g_v_list.html", meal_type=meal_type, menu_items=menu_items, mess_name=MESS_NAME)

    # POST processing
    meal_type = request.form.get("meal_type")
    persons = request.form.get("person")
    menu_items = request.form.getlist("menu_item[]")
    groceries = request.form.getlist("grocery[]")
    vegetables = request.form.getlist("vegetable[]")
    khanabchas = request.form.getlist("khanabcha[]")
    khanaghatas = request.form.getlist("khanaghata[]")
    remarks = request.form.getlist("remark[]")

    def format_readable_list(data_list):
        return "\n".join([f"{i+1}. {item.strip()}" for i, item in enumerate(data_list) if item.strip()])

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO grocery_vegetable_management
            (date_day, meal_type, menu_item, person, grocery, vegetable, khanabcha, khanaghata, remark)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            datetime.now(),
            meal_type,
            format_readable_list(menu_items),
            persons,
            format_readable_list(groceries),
            format_readable_list(vegetables),
            format_readable_list(khanabchas),
            format_readable_list(khanaghatas),
            format_readable_list(remarks)
        ))

        conn.commit()
        cursor.close()
        conn.close()
        flash("Grocery and Vegetable data saved successfully!", "success")
    except pymysql.MySQLError as e:
        flash(f"Database error while inserting: {str(e)}", "danger")
        return redirect("/g_v_list")

    return redirect("/g_v_list")

@app.route("/g_v_report")
def g_v_report():
    if 'logged_in' not in session:
        return redirect(url_for('adminlogin'))
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM grocery_vegetable_management")
    rows = cursor.fetchall()
    conn.close()

    grouped_data = defaultdict(list)

    for row in rows:
        date = row['date_day']
        meal_type = row['meal_type']
        key = (date, meal_type)
        grouped_data[key].append({
            'menu_item': row['menu_item'],
            'person': row['person'],
            'grocery': row['grocery'],
            'vegetable': row['vegetable'],
            'khanabcha': row['khanabcha'],
            'khanaghata': row['khanaghata'],
            'remark': row['remark'],
            'day': date.strftime("%A"),
            'date_str': date.strftime("%d-%m-%Y")
        })

    sorted_grouped_data = OrderedDict(sorted(grouped_data.items(), key=lambda x: x[0][0], reverse=True))

    return render_template("g_v_report.html", grouped_data=sorted_grouped_data, mess_name=MESS_NAME)


@app.route("/delete_gv_row", methods=["POST"])
def delete_gv_row():
    if 'logged_in' not in session:
        return redirect(url_for('adminlogin'))
        
    date = request.form.get("date")
    meal_type = request.form.get("meal_type")
    menu_item = request.form.get("menu_item")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        table_name = "grocery_vegetable_management"
        query = f"DELETE FROM `{table_name}` WHERE menu_item LIKE %s LIMIT 1"
        cursor.execute(query, (f"%{menu_item}%",))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Row deleted successfully!", "success")
    except Exception as e:
        print("Deletion error:", e)
        flash(f"Error deleting row: {str(e)}", "danger")
    
    return redirect(url_for("g_v_report"))


@app.route('/g_v')
def g_v():
    if 'logged_in' not in session:
        return redirect(url_for('adminlogin'))
    return render_template('g_v.html', mess_name=MESS_NAME)


if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')

