#!/usr/bin/env python3
"""
ISODROP - Vercel Serverless Deployment
Optimized for Vercel with limitations
"""

import os
import socket
import uuid
import json
import qrcode
import io
import base64
from datetime import datetime
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from functools import wraps

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'isodrop-vercel-' + str(uuid.uuid4())
CORS(app, origins="*")

# Store client data (in-memory, will reset on serverless function restart)
connected_devices = {}
shared_files = {}
messages = []

# ============================================================================
# Utility Functions
# ============================================================================

def get_local_ip():
    """Get local IP or use Vercel provided domain"""
    try:
        # Try to get actual IP for local development
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        # For Vercel, return a placeholder
        return os.environ.get('VERCEL_URL', 'localhost:3000')

def generate_qr_code(url):
    """Generate QR code as base64"""
    try:
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        return f"data:image/png;base64,{img_base64}"
    except:
        return None

def validate_mime_type(mime_type):
    """Validate MIME type"""
    allowed = {
        'text/plain', 'text/html', 'image/jpeg', 'image/png', 
        'image/gif', 'image/webp', 'application/pdf', 'video/mp4',
        'video/x-matroska', 'audio/mpeg', 'audio/wav'
    }
    main_type = mime_type.split('/')[0] if mime_type else ''
    return mime_type in allowed or main_type in ['image', 'audio', 'video', 'text']

# ============================================================================
# API Routes
# ============================================================================

@app.route('/', methods=['GET'])
def index():
    """Serve frontend HTML"""
    return get_frontend_html()

@app.route('/api/server-info', methods=['GET'])
def server_info():
    """Get server connection info"""
    url = os.environ.get('VERCEL_URL')
    if url and not url.startswith('http'):
        url = f"https://{url}"
    else:
        url = "http://localhost:3000"
    
    try:
        qr_code = generate_qr_code(url)
    except:
        qr_code = None
    
    return jsonify({
        'server_url': url,
        'local_ip': get_local_ip(),
        'qr_code': qr_code,
        'port': '443' if 'https' in url else '80',
        'deployment': 'vercel'
    })

@app.route('/api/devices', methods=['GET'])
def get_devices():
    """Get connected devices"""
    devices_list = [
        {
            'id': device_id,
            'name': device_data['name'],
            'joined_at': device_data['joined_at'],
            'is_online': True
        }
        for device_id, device_data in connected_devices.items()
    ]
    return jsonify({
        'devices': devices_list,
        'total': len(devices_list)
    })

@app.route('/api/devices', methods=['POST'])
def register_device():
    """Register new device"""
    data = request.json
    device_id = str(uuid.uuid4())[:8]
    device_name = data.get('name', f"Device {device_id}")
    
    connected_devices[device_id] = {
        'id': device_id,
        'name': device_name,
        'joined_at': datetime.now().isoformat(),
        'is_online': True
    }
    
    return jsonify({
        'device_id': device_id,
        'success': True
    }), 201

@app.route('/api/devices/<device_id>', methods=['DELETE'])
def unregister_device(device_id):
    """Unregister device"""
    if device_id in connected_devices:
        del connected_devices[device_id]
        return jsonify({'success': True})
    return jsonify({'error': 'Device not found'}), 404

@app.route('/api/messages', methods=['GET'])
def get_messages():
    """Get shared messages"""
    return jsonify({
        'messages': messages[-50:]  # Last 50 messages
    })

@app.route('/api/messages', methods=['POST'])
def add_message():
    """Add new message"""
    data = request.json
    sender_id = data.get('sender_id')
    sender_name = data.get('sender_name', 'Unknown')
    text = data.get('text', '').strip()[:5000]
    
    if not sender_id or not text:
        return jsonify({'error': 'Invalid message'}), 400
    
    message = {
        'id': str(uuid.uuid4()),
        'sender_id': sender_id,
        'sender_name': sender_name,
        'text': text,
        'timestamp': datetime.now().isoformat(),
        'type': 'text'
    }
    
    messages.append(message)
    return jsonify(message), 201

@app.route('/api/files', methods=['GET'])
def get_files():
    """Get shared files"""
    return jsonify({
        'files': list(shared_files.values())
    })

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file upload (REST endpoint - limited to 50MB on Vercel)"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    sender_id = request.form.get('sender_id')
    sender_name = request.form.get('sender_name', 'Unknown')
    
    if not file or not sender_id:
        return jsonify({'error': 'Invalid request'}), 400
    
    if file.size > 52428800:  # 50MB limit on Vercel
        return jsonify({'error': 'File too large (max 50MB on Vercel)'}), 413
    
    file_id = str(uuid.uuid4())
    file_data = file.read()
    
    shared_files[file_id] = {
        'file_id': file_id,
        'filename': file.filename,
        'file_size': len(file_data),
        'mime_type': file.content_type or 'application/octet-stream',
        'sender_id': sender_id,
        'sender_name': sender_name,
        'timestamp': datetime.now().isoformat(),
        'type': 'file',
        'data': base64.b64encode(file_data).decode()[:1000000]  # Store limited base64
    }
    
    return jsonify({
        'file_id': file_id,
        'success': True,
        'message': 'Note: File stored in memory, will be cleared on function restart'
    }), 201

@app.route('/download/<file_id>', methods=['GET'])
def download_file(file_id):
    """Download shared file"""
    if file_id not in shared_files:
        return jsonify({'error': 'File not found'}), 404
    
    file_data = shared_files[file_id]
    
    try:
        file_bytes = base64.b64decode(file_data['data'])
        return send_file(
            io.BytesIO(file_bytes),
            mimetype=file_data['mime_type'],
            as_attachment=True,
            download_name=file_data['filename']
        )
    except:
        return jsonify({'error': 'Cannot download file'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'devices': len(connected_devices),
        'messages': len(messages),
        'files': len(shared_files)
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Server error'}), 500

# ============================================================================
# Frontend HTML
# ============================================================================

def get_frontend_html():
    """Return frontend HTML"""
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ISODROP - Real-time Local Data Sharing</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            --primary: #00d9ff;
            --secondary: #ff006e;
            --accent: #8338ec;
            --dark-bg: #0a0e27;
            --card-bg: rgba(15, 20, 45, 0.7);
            --border-color: rgba(0, 217, 255, 0.3);
            --text-primary: #ffffff;
            --text-secondary: #b0b7c0;
        }

        html, body {
            height: 100%;
            width: 100%;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0a0e27 0%, #1a1f4b 50%, #0f1425 100%);
            color: var(--text-primary);
        }

        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                radial-gradient(circle at 20% 50%, rgba(0, 217, 255, 0.05) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(131, 56, 236, 0.05) 0%, transparent 50%);
            pointer-events: none;
            z-index: -1;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }

        .card {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 2rem;
            backdrop-filter: blur(20px);
            margin-bottom: 2rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }

        .header {
            text-align: center;
            margin-bottom: 3rem;
        }

        .title {
            font-size: 48px;
            font-weight: 700;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 1rem;
        }

        .subtitle {
            font-size: 18px;
            color: var(--text-secondary);
        }

        .deployment-notice {
            background: rgba(255, 165, 0, 0.1);
            border: 1px solid #ffa500;
            border-radius: 8px;
            padding: 1.5rem;
            margin-bottom: 2rem;
            color: #ffa500;
        }

        .deployment-notice strong {
            color: #ffb700;
        }

        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }

        .feature-card {
            background: linear-gradient(135deg, rgba(0, 217, 255, 0.1), rgba(131, 56, 236, 0.1));
            border: 1px solid rgba(0, 217, 255, 0.3);
            border-radius: 10px;
            padding: 1.5rem;
            text-align: center;
        }

        .feature-icon {
            font-size: 32px;
            margin-bottom: 0.5rem;
        }

        .feature-title {
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: var(--primary);
        }

        .feature-desc {
            font-size: 14px;
            color: var(--text-secondary);
            line-height: 1.5;
        }

        .info-section {
            margin: 2rem 0;
        }

        .info-title {
            font-size: 20px;
            font-weight: 700;
            color: var(--primary);
            margin-bottom: 1rem;
        }

        .info-text {
            font-size: 14px;
            color: var(--text-secondary);
            line-height: 1.8;
            margin-bottom: 1rem;
        }

        .code-block {
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 1rem;
            font-family: 'Courier New', monospace;
            font-size: 12px;
            overflow-x: auto;
            margin: 1rem 0;
        }

        .qr-section {
            text-align: center;
            margin: 2rem 0;
        }

        .qr-container {
            width: 200px;
            height: 200px;
            background: white;
            border-radius: 12px;
            padding: 1rem;
            margin: 0 auto;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .qr-container img {
            width: 100%;
            height: 100%;
            object-fit: contain;
        }

        .button-group {
            display: flex;
            gap: 1rem;
            justify-content: center;
            flex-wrap: wrap;
            margin: 2rem 0;
        }

        .btn {
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
        }

        .btn-primary {
            background: linear-gradient(135deg, var(--primary), var(--accent));
            color: var(--text-primary);
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(0, 217, 255, 0.4);
        }

        .btn-secondary {
            background: rgba(0, 217, 255, 0.2);
            color: var(--primary);
            border: 1px solid var(--primary);
        }

        .btn-secondary:hover {
            background: rgba(0, 217, 255, 0.3);
        }

        .status {
            display: inline-block;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            background: rgba(6, 255, 165, 0.1);
            color: #06ffa5;
            border: 1px solid #06ffa5;
        }

        .warning {
            display: inline-block;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            background: rgba(255, 165, 0, 0.1);
            color: #ffa500;
            border: 1px solid #ffa500;
        }

        .footer {
            text-align: center;
            color: var(--text-secondary);
            font-size: 12px;
            margin-top: 3rem;
            padding-top: 2rem;
            border-top: 1px solid var(--border-color);
        }

        @media (max-width: 768px) {
            .container {
                padding: 1rem;
            }

            .title {
                font-size: 32px;
            }

            .feature-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="title">🚀 ISODROP</div>
            <div class="subtitle">Real-time Data Sharing on Vercel</div>
        </div>

        <div class="card deployment-notice">
            <strong>⚠️ Vercel Deployment Notice:</strong><br>
            This is a REST-based version of ISODROP optimized for Vercel's serverless environment.
            For the full real-time WebSocket experience, deploy on Render, Railway, or Heroku (see alternatives below).
        </div>

        <div class="card">
            <div class="info-title">About ISODROP on Vercel</div>
            <div class="info-text">
                ISODROP is a premium real-time data sharing application. This Vercel version uses REST APIs
                for compatibility with serverless functions. The full SocketIO version is recommended for
                production use with real-time features.
            </div>
            <div class="button-group">
                <span class="status">✅ REST API Version</span>
                <span class="warning">⚠️ Limited WebSocket Support</span>
            </div>
        </div>

        <div class="card">
            <div class="info-title">📊 Features in This Version</div>
            <div class="feature-grid">
                <div class="feature-card">
                    <div class="feature-icon">💬</div>
                    <div class="feature-title">Messages</div>
                    <div class="feature-desc">Send and receive text messages via REST API</div>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">📁</div>
                    <div class="feature-title">File Sharing</div>
                    <div class="feature-desc">Share files up to 50MB (Vercel limit)</div>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">👥</div>
                    <div class="feature-title">Device Tracking</div>
                    <div class="feature-desc">Register and track connected devices</div>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">📊</div>
                    <div class="feature-title">Server Info</div>
                    <div class="feature-desc">Get deployment and server information</div>
                </div>
            </div>
        </div>

        <div class="card">
            <div class="info-title">🔌 REST API Endpoints</div>
            <div class="info-text">Access the following endpoints:</div>
            <div class="code-block">
GET  /health                 - Health check<br>
GET  /api/server-info        - Server info & QR code<br>
GET  /api/devices            - List connected devices<br>
POST /api/devices            - Register new device<br>
DEL  /api/devices/{id}       - Unregister device<br>
GET  /api/messages           - Get messages<br>
POST /api/messages           - Send message<br>
GET  /api/files              - List shared files<br>
POST /api/upload             - Upload file<br>
GET  /download/{id}          - Download file
            </div>
        </div>

        <div class="card">
            <div class="info-title">⚡ Better Alternatives for Full Experience</div>
            <div class="info-text">For the complete real-time WebSocket experience, deploy ISODROP on:</div>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin: 1.5rem 0;">
                <div style="padding: 1rem; background: rgba(0, 217, 255, 0.1); border: 1px solid var(--border-color); border-radius: 8px;">
                    <div style="font-weight: 600; color: var(--primary); margin-bottom: 0.5rem;">Render</div>
                    <div style="font-size: 12px; color: var(--text-secondary);">Best for Flask + SocketIO</div>
                    <div style="font-size: 11px; color: #06ffa5; margin-top: 0.5rem;">Free tier available ✓</div>
                </div>
                <div style="padding: 1rem; background: rgba(0, 217, 255, 0.1); border: 1px solid var(--border-color); border-radius: 8px;">
                    <div style="font-weight: 600; color: var(--primary); margin-bottom: 0.5rem;">Railway</div>
                    <div style="font-size: 12px; color: var(--text-secondary);">Easy deployment, great docs</div>
                    <div style="font-size: 11px; color: #06ffa5; margin-top: 0.5rem;">Free credits included ✓</div>
                </div>
                <div style="padding: 1rem; background: rgba(0, 217, 255, 0.1); border: 1px solid var(--border-color); border-radius: 8px;">
                    <div style="font-weight: 600; color: var(--primary); margin-bottom: 0.5rem;">Heroku</div>
                    <div style="font-size: 12px; color: var(--text-secondary);">Reliable, full WebSocket support</div>
                    <div style="font-size: 11px; color: #06ffa5; margin-top: 0.5rem;">Paid plans starting at $5</div>
                </div>
            </div>
        </div>

        <div class="card">
            <div class="info-title">📚 Documentation</div>
            <div class="info-text">
                For complete documentation, deployment guides, and customization options,
                check the included markdown files in the project:
            </div>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin: 1.5rem 0;">
                <div>📖 README.md</div>
                <div>⚡ QUICKSTART.md</div>
                <div>🚀 DEPLOYMENT.md</div>
                <div>🔧 CONFIG.md</div>
            </div>
        </div>

        <div class="card">
            <div class="info-title">🎯 Next Steps</div>
            <div class="button-group">
                <a href="/health" class="btn btn-primary">Check Health</a>
                <a href="/api/server-info" class="btn btn-secondary">Server Info</a>
            </div>
            <div class="info-text" style="text-align: center; margin-top: 1.5rem;">
                For the full ISODROP experience with real-time WebSocket communication,<br>
                deploy on Render, Railway, or a traditional server.
            </div>
        </div>

        <div class="footer">
            <p>ISODROP v1.0.0 | Vercel Deployment | Made with ❤️ for the community</p>
        </div>
    </div>

    <script>
        // Simple client-side functionality
        async function getServerInfo() {
            try {
                const response = await fetch('/api/server-info');
                const data = await response.json();
                console.log('Server Info:', data);
                alert(JSON.stringify(data, null, 2));
            } catch (error) {
                console.error('Error:', error);
                alert('Error fetching server info');
            }
        }

        async function checkHealth() {
            try {
                const response = await fetch('/health');
                const data = await response.json();
                console.log('Health:', data);
                alert('Status: ' + data.status + '\\nDevices: ' + data.devices);
            } catch (error) {
                console.error('Error:', error);
                alert('Error checking health');
            }
        }
    </script>
</body>
</html>
'''

# ============================================================================
# Main
# ============================================================================

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))
