#!/usr/bin/env python
"""Test script to verify Flask app works on port 8080"""
import sys
import time
import subprocess
import requests

# Start Flask server
print("Starting S. N. Joshi. Mess Admin System on port 8080...")
proc = subprocess.Popen(
    [sys.executable, "main.py"],
    cwd=r"c:\Users\Mahi Patel\Desktop\Mahi\HS",
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

time.sleep(3)

# Test connection
try:
    response = requests.get("http://localhost:8080/adminlogin")
    if response.status_code == 200:
        print("✓ Server is running successfully on http://localhost:8080")
        print("✓ Admin login page is accessible")
        print("\n=== Admin Credentials ===")
        print("Phone: 7862017545")
        print("Password: (Check your existing admin password)")
        print("\nServer is now running. Press Ctrl+C to stop.")
        
        # Keep server running
        proc.wait()
    else:
        print(f"✗ Unexpected response code: {response.status_code}")
        proc.terminate()
except Exception as e:
    print(f"✗ Connection error: {e}")
    print("Make sure MySQL is running and the database is accessible")
    proc.terminate()
    sys.exit(1)
