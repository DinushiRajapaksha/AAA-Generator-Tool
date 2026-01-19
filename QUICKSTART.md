# Quick Start Guide - AAA Generator Web Interface

## 🚀 Getting Started

### 1. Install Dependencies

Open PowerShell in the project directory and run:

```powershell
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- Jinja2 (templating engine)

### 2. Start the Web Server

Run the Flask application:

```powershell
python app.py
```

You should see:
```
======================================================================
AAA Generator Tool - Web Interface
======================================================================
Starting server at http://localhost:5000
Press Ctrl+C to stop
======================================================================
```

### 3. Open in Browser

Open your web browser and navigate to:
```
http://localhost:5000
```

## 📖 Using the Web Interface

### Step 1: Fill in the Form
1. **Activity Diagram ID**: Enter the ID (e.g., "2.11.1.1")
2. **Activity Name**: Enter the activity name
3. **IFS Documentation Text**: Paste the documentation including:
   - Explanation section
   - Prerequisites section
   - System Effects section

### Step 2: Generate
Click the **"Generate AAA Block"** button

### Step 3: Copy Results
- View the generated AAA block on the right panel
- Click **"Copy to Clipboard"** to copy the markdown

## 🎯 Features

✨ **Load Examples**: Click "Load Example" to see sample documentation
🎨 **Modern UI**: Clean, responsive design
📋 **Copy to Clipboard**: One-click copy functionality
⌨️ **Keyboard Shortcuts**: 
- `Ctrl/Cmd + Enter` to generate
- `Escape` to close modal

## 🔧 Troubleshooting

### Server won't start
- Make sure port 5000 is not in use
- Check that Flask is installed: `pip list | findstr Flask`

### Can't connect to server
- Make sure the server is running
- Try accessing http://127.0.0.1:5000 instead

### Form validation errors
- All three fields are required
- Make sure documentation includes sections with headers

## 🌐 Network Access

To access from other devices on your network:
1. Find your IP address: `ipconfig`
2. Access using: `http://YOUR_IP:5000`

## 🛑 Stopping the Server

Press `Ctrl+C` in the terminal to stop the server.

---

**Enjoy using the AAA Generator Tool!** 🎉
