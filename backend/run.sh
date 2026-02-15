#!/bin/bash
# S. N. Joshi. Mess - Admin System Launcher (for Linux/Mac)

echo "====================================================="
echo "  S. N. JOSHI. MESS - ADMIN MANAGEMENT SYSTEM"
echo "====================================================="
echo ""

# Verify database connection first
echo "Verifying database connection..."
python3 verify_setup.py > /dev/null 2>&1

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Database connection failed!"
    echo "Please ensure:"
    echo "  1. MySQL is running"
    echo "  2. track_serve database exists"
    echo "  3. Admin user is configured"
    echo ""
    exit 1
fi

echo ""
echo "Starting Flask application on port 8080..."
echo ""
echo "Access the application at: http://localhost:8080"
echo ""
echo "Login Credentials:"
echo "  Phone: 7862017545"
echo "  Password: (Your admin password)"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 main.py
