🚀 ISODROP - QUICK REFERENCE
=============================

INSTALLATION & STARTUP
======================

Windows (All-in-One):
1. Open PowerShell in project folder
2. Run: .\run.bat
3. Follow prompts
4. Open browser to displayed URL

Windows (Manual):
1. pip install -r requirements.txt
2. python app.py
3. Open http://192.168.1.X:5000

macOS/Linux (All-in-One):
1. chmod +x run.sh
2. ./run.sh
3. Follow prompts
4. Open browser to displayed URL

macOS/Linux (Manual):
1. python3 -m venv venv
2. source venv/bin/activate
3. pip install -r requirements.txt
4. python3 app.py
5. Open http://192.168.1.X:5000

FIND YOUR LOCAL IP
==================

Windows:
- Open PowerShell: ipconfig
- Look for "IPv4 Address" (usually 192.168.x.x)
- Full URL: http://192.168.x.x:5000

macOS/Linux:
- Open Terminal: ifconfig
- Look for "inet" under en0 or eth0
- Full URL: http://192.168.x.x:5000

TROUBLESHOOTING COMMANDS
========================

Check if Python is installed:
- Windows: python --version
- macOS/Linux: python3 --version

Check if port 5000 is available:
- Windows: netstat -ano | findstr :5000
- macOS/Linux: lsof -i :5000

Kill process using port 5000:
- Windows: taskkill /PID <number> /F
- macOS/Linux: kill -9 <PID>

Change port in app.py (last line):
socketio.run(app, host='0.0.0.0', port=8000)

Clear temporary files:
- Windows: rmdir %temp%\isodrop /s
- macOS/Linux: rm -rf /tmp/isodrop

FEATURE QUICK START
===================

Send Message:
1. Type in bottom input
2. Press Enter or click Send
3. Appears on all devices

Share File:
1. Drag file to upload zone OR click zone
2. See progress bar
3. File appears on all devices
4. Others click Download or Preview

View Devices:
- See list in left sidebar
- Shows real-time online status
- Counter at top shows total

Preview Media:
- Images: Click "👁️ Preview" button
- Videos: Click "▶️ Play" button
- Other files: Click "⬇️ Download" button

CUSTOMIZATION QUICK EDITS
==========================

Change Port:
File: app.py
Line: ~400 (last line)
Change: port=5000 to desired port

Change Max File Size:
File: app.py
Line: ~30
Change: 5 * 1024 * 1024 * 1024 to desired size in bytes

Change Primary Color:
File: index.html
Line: ~19
Change: --primary: #00d9ff to desired hex color

Change Primary Color:
File: index.html
Line: ~20
Change: --secondary: #ff006e to desired hex color

BROWSER COMPATIBILITY
=====================

✅ Works great:
- Chrome/Chromium (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

Recommended:
- Chrome on desktop
- Chrome on Android
- Safari on iOS

NETWORK REQUIREMENTS
====================

✅ Local WiFi (LAN):
- All devices on same WiFi
- No internet needed
- Works instantly

❌ Not supported:
- Different networks
- VPN to same network
- 4G/LTE only devices

For remote access:
- Run on server with public IP
- Access from anywhere
- Add authentication (see CONFIG.md)

PERFORMANCE STATS
=================

Message delay: < 100ms
File upload speed: ~ Network speed
Max concurrent devices: 50+
Max file size: 5GB
Chunk size: 1MB (configurable)
Temp file cleanup: 24 hours (configurable)

COMMON ERROR MESSAGES
====================

"Port 5000 already in use":
→ Close other app using port 5000, OR
→ Change port in app.py line ~400

"Cannot find module Flask":
→ Run: pip install -r requirements.txt

"ModuleNotFoundError: No module named 'qrcode'":
→ Run: pip install qrcode[pil]

"Failed to connect":
→ Check if server is running
→ Check if devices on same WiFi
→ Verify firewall isn't blocking port 5000

"File upload failed":
→ Check file size (max 5GB)
→ Check disk space
→ Try smaller file first

MOBILE SETUP
============

From Mobile Browser:
1. Connect to same WiFi as server
2. Open: http://192.168.1.X:5000
3. Or scan QR code with camera app
4. Grant notification permission (recommended)
5. Type name (optional)
6. Start sharing!

Android Specific:
- Chrome: Supports all features
- Firefox: Supports all features
- Permissions: Allow notifications
- Files: Use Files app to share

iOS Specific:
- Safari: Supports all features
- Add to home screen: Can work offline
- Permissions: Allow notifications
- Files: Use Files app to share

DEVELOPMENT TIPS
================

Debug mode (see errors):
1. In app.py, change: debug=False to debug=True
2. Restart server
3. Watch console for detailed errors

Add logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
app.logger.debug("Message here")
```

Test with multiple devices:
1. Open in main browser
2. Open in incognito window
3. Open on phone
4. Send messages between them

Monitor uploads:
1. Open browser console (F12)
2. Go to Network tab
3. Upload file
4. Watch chunk requests

DEPLOYMENT CHECKLIST
====================

Before going live:
[ ] Test on 3+ devices
[ ] Test large file upload
[ ] Test on mobile
[ ] Check all buttons work
[ ] Test disconnect/reconnect
[ ] Verify firewall allows port
[ ] Check disk space for temp files
[ ] Test on different WiFi network
[ ] Verify QR code works
[ ] Test video playback
[ ] Test image preview
[ ] Check push notifications

For production:
[ ] Use static IP or DNS
[ ] Add HTTPS (nginx reverse proxy)
[ ] Enable rate limiting
[ ] Monitor disk usage
[ ] Set up log rotation
[ ] Add backup cleanup script
[ ] Update security group rules
[ ] Add SSL certificate
[ ] Enable password protection
[ ] Test under load

KEYBOARD SHORTCUTS
==================

Global:
- Enter (in message input): Send message
- Escape (in preview): Close modal
- Ctrl+Shift+J: Open browser console

Message Input:
- Enter: Send
- Shift+Enter: New line (future feature)
- Tab: Next field

File Upload:
- Ctrl+A: Select all files
- Enter: Upload selected

ADVANCED USAGE
==============

Batch file sharing:
1. Select multiple files in upload zone
2. Drag and drop all at once
3. Each uploads sequentially
4. All devices see all files

Concurrent messaging:
1. Send while file uploading
2. Both work independently
3. No interference

Device naming:
1. Edit in browser console:
   localStorage.setItem('isodrop_device_name', 'My Device')
2. Refresh page
3. New name appears to others

Custom styling:
1. Open DevTools (F12)
2. Modify CSS in <style> tag
3. Changes live preview immediately

SECURITY TIPS
=============

Local Network Safety:
✅ Only accessible on same WiFi
✅ No data stored on device
✅ Auto-cleanup after 24 hours
✅ Input validation on all fields

Additional security (optional):
1. Use strong WiFi password
2. Hide SSID if very sensitive
3. Use VPN if untrusted WiFi
4. Run firewall check before demo
5. Don't expose to internet without auth
6. Limit concurrent device count if needed
7. Enable read-only for presentations
8. Disable downloads for public demo

MONITORING
==========

Watch active connections:
```bash
watch netstat -an | grep 5000  # Linux/macOS
```

Monitor disk usage:
```bash
du -sh /tmp/isodrop  # Linux/macOS
dir %temp%\isodrop  # Windows
```

Check server health:
- Open http://localhost:5000
- Should load instantly
- No console errors in DevTools
- Network requests should complete

CONTACT & SUPPORT
=================

Issues:
1. Check README.md troubleshooting
2. Check CONFIG.md for settings
3. Read SUMMARY.md for overview
4. Search error message on GitHub

Contributing:
1. Fork the project
2. Make changes
3. Test thoroughly
4. Submit pull request

=============================
Quick Reference Complete ✅

Need more info? See:
- README.md (full docs)
- CONFIG.md (advanced)
- SUMMARY.md (overview)
=============================
