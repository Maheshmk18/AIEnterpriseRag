# Supabase Database Setup Guide

## Issue
The application cannot connect to Supabase database. Error: "No such host is known"

## Root Cause
The database connection string in `.env` file is either:
1. Incorrect or has a typo
2. Using an old/deprecated Supabase URL format
3. Project is paused or deleted

## Solution

### Step 1: Get Correct Connection String

1. **Login to Supabase Dashboard**
   - Go to https://supabase.com/dashboard
   - Select your project

2. **Navigate to Database Settings**
   - Click Settings (gear icon) → Database
   - Scroll to "Connection string" section

3. **Copy Connection Pooling URI**
   - Select "Connection Pooling" tab
   - Choose "Transaction" mode
   - Copy the URI (should look like):
     ```
     postgresql://postgres.[PROJECT-REF]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres
     ```

### Step 2: Update .env File

1. **URL Encode Special Characters in Password**
   
   If your password contains special characters, encode them:
   - `#` → `%23`
   - `@` → `%40`
   - `$` → `%24`
   - `%` → `%25`
   - `&` → `%26`
   - `+` → `%2B`
   - ` ` (space) → `%20`

2. **Update DATABASE_URL in .env**
   ```
   DATABASE_URL=postgresql://postgres.[PROJECT-REF]:[ENCODED-PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres
   ```

### Step 3: Initialize Database

After updating the connection string:

```bash
# Test connection
python test_db_connection.py

# Initialize database (create tables)
python init_database.py

# Restart backend server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Step 4: Verify Tables Created

1. Go to Supabase Dashboard
2. Click "Table Editor"
3. You should see these tables:
   - users
   - documents
   - chat_sessions
   - chat_messages

## Common Issues

### Issue: "No such host is known"
**Solution**: Connection string is wrong. Get new one from Supabase dashboard.

### Issue: "password authentication failed"
**Solution**: Password has special characters. URL encode them.

### Issue: "SSL connection required"
**Solution**: Add `?sslmode=require` to end of connection string.

### Issue: Tables not showing in Supabase
**Solution**: Run `python init_database.py` after fixing connection.

## Default Admin Credentials

After successful initialization:
- **Username**: admin
- **Email**: admin@enterprise.com
- **Password**: admin123

## Need Help?

If you're still having issues:
1. Check if Supabase project is active (not paused)
2. Verify you're using the correct project reference
3. Try using Direct Connection instead of Pooler
4. Check firewall/antivirus settings
