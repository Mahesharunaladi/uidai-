# 🔐 Authentication System - UIDAI Dashboard

## Overview
The UIDAI Dashboard now includes a secure authentication system with user registration and login functionality.

## Features

### ✅ User Authentication
- **Secure Login**: SHA-256 encrypted password hashing
- **User Registration**: Create new accounts with role assignment
- **Session Management**: Persistent login sessions
- **Role-Based Access**: Support for different user roles (admin, analyst, user)

### 🔒 Security Features
- Password encryption using SHA-256
- Secure session state management
- Password confirmation during registration
- Minimum password length requirement (6 characters)

## Default Login Credentials

### Admin Account
```
Username: admin
Password: admin123
Role: admin
```

### Demo Account
```
Username: demo
Password: demo123
Role: user
```

⚠️ **Important**: Change these default passwords after first login!

## User Roles

1. **Admin** - Full access to all features and system administration
2. **Analyst** - Access to analytical tools and reports
3. **User** - Standard access to dashboard features

## How to Use

### First Time Setup

1. Run the application:
   ```bash
   streamlit run app.py
   ```

2. You'll see the login/registration page
3. Use the default credentials above to login, or create a new account

### Login

1. Click on the "🔐 Login" tab
2. Enter your username and password
3. Click "🔓 Login"

### Registration

1. Click on the "📝 Register" tab
2. Fill in all required fields:
   - Username (unique)
   - Email address
   - Password (minimum 6 characters)
   - Confirm password
   - Select role
3. Click "📝 Register"
4. After successful registration, switch to Login tab to access the dashboard

### Logout

- Click the "🚪 Logout" button in the sidebar to end your session

## User Database

User credentials are stored in `user_database.json` in the project root directory.

### Creating Additional Admin Users

Run the `create_admin.py` script:
```bash
python3 create_admin.py
```

This will create/reset the default admin and demo accounts.

## File Structure

```
uidai--1/
├── app.py                    # Main application with authentication
├── create_admin.py          # Script to create default users
├── user_database.json       # User credentials database (auto-generated)
└── AUTH_README.md          # This file
```

## Security Notes

1. **Password Storage**: All passwords are hashed using SHA-256 before storage
2. **Session Security**: Session state is managed by Streamlit's secure session management
3. **Data Protection**: User database is stored locally in JSON format
4. **Production Deployment**: For production use, consider:
   - Using a proper database (PostgreSQL, MySQL)
   - Implementing OAuth/LDAP integration
   - Adding two-factor authentication
   - Using environment variables for sensitive data
   - Implementing password reset functionality

## Troubleshooting

### Can't Login?
- Verify username and password are correct
- Check that `user_database.json` exists
- Run `create_admin.py` to reset default accounts

### Forgot Password?
- Contact your administrator to reset your password
- Administrators can manually edit `user_database.json`

### Registration Issues?
- Ensure username is unique
- Password must be at least 6 characters
- Both password fields must match

## Future Enhancements

- [ ] Password reset via email
- [ ] Two-factor authentication
- [ ] User profile management
- [ ] Activity logging and audit trail
- [ ] Password strength meter
- [ ] Account lockout after failed attempts
- [ ] OAuth integration (Google, Microsoft)
- [ ] LDAP/Active Directory integration

## Support

For issues or questions, contact the UIDAI dashboard administrator.

---

**Last Updated**: January 2026
**Version**: 1.0.0
