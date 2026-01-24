"""
Create initial admin user for UIDAI Dashboard
"""

import json
import hashlib
from datetime import datetime

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

# Create initial admin user
users = {
    "admin": {
        "password": hash_password("admin123"),
        "email": "admin@uidai.gov.in",
        "role": "admin",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    },
    "demo": {
        "password": hash_password("demo123"),
        "email": "demo@uidai.gov.in",
        "role": "user",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
}

# Save to file
with open("user_database.json", "w") as f:
    json.dump(users, f, indent=4)

print("✅ Initial users created successfully!")
print("\n📋 Login Credentials:")
print("-" * 50)
print("Admin User:")
print("  Username: admin")
print("  Password: admin123")
print("  Role: admin")
print("\nDemo User:")
print("  Username: demo")
print("  Password: demo123")
print("  Role: user")
print("-" * 50)
print("\n⚠️  Please change these passwords after first login!")
