# ISODROP Configuration Guide

## Environment Variables

Create a `.env` file in the project root to customize settings:

```env
# Server Settings
FLASK_ENV=production
FLASK_DEBUG=False
SERVER_HOST=0.0.0.0
SERVER_PORT=5000

# File Transfer Settings
MAX_FILE_SIZE_GB=5
CHUNK_SIZE_MB=1
FILE_EXPIRY_HOURS=24
UPLOAD_TEMP_DIR=/tmp/isodrop

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60

# Security
PIN_ENABLED=False
PIN_LENGTH=4
MAX_PIN_ATTEMPTS=5
REQUIRE_AUTH=False

# UI Settings
APP_NAME=ISODROP
THEME=dark
ACCENT_COLOR=#00d9ff
```

## Configuration Options

### File Transfer
- `MAX_FILE_SIZE_GB`: Maximum file size in GB (default: 5)
- `CHUNK_SIZE_MB`: Upload chunk size in MB (default: 1)
- `FILE_EXPIRY_HOURS`: How long to keep temp files (default: 24)
- `UPLOAD_TEMP_DIR`: Directory for temporary files

### Rate Limiting
- `RATE_LIMIT_REQUESTS`: Requests per window (default: 100)
- `RATE_LIMIT_WINDOW`: Time window in seconds (default: 60)

### Security
- `PIN_ENABLED`: Enable PIN protection (True/False)
- `PIN_LENGTH`: PIN digit length (default: 4)
- `MAX_PIN_ATTEMPTS`: Failed attempts before lockout
- `REQUIRE_AUTH`: Require login (future feature)

### UI/UX
- `THEME`: dark or light
- `ACCENT_COLOR`: Primary color (hex)

## Recommended Production Settings

```env
FLASK_ENV=production
FLASK_DEBUG=False
SERVER_HOST=0.0.0.0
SERVER_PORT=5000
MAX_FILE_SIZE_GB=10
FILE_EXPIRY_HOURS=48
RATE_LIMIT_REQUESTS=50
RATE_LIMIT_WINDOW=60
PIN_ENABLED=True
```

## Deployment on Different Platforms

### AWS EC2
```bash
# Install Python 3.11
sudo yum update -y
sudo yum install python3.11 -y

# Clone repo
git clone https://github.com/yourusername/isodrop.git
cd isodrop

# Install dependencies
pip3 install -r requirements.txt

# Run with systemd
sudo systemctl start isodrop
```

### Heroku
```bash
# Create Procfile
echo "web: python app.py" > Procfile

# Deploy
git push heroku main
```

### Docker Compose
```yaml
version: '3.8'
services:
  isodrop:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - SERVER_PORT=5000
    volumes:
      - ./uploads:/tmp/isodrop
```

## Performance Tuning

### For High Device Count (50+)
```env
RATE_LIMIT_REQUESTS=200
CHUNK_SIZE_MB=2
FILE_EXPIRY_HOURS=12
```

### For Slow Networks
```env
CHUNK_SIZE_MB=512k
RATE_LIMIT_WINDOW=120
```

### For High Throughput (LAN)
```env
CHUNK_SIZE_MB=5
RATE_LIMIT_REQUESTS=500
```

## Security Hardening

### Enable PIN Protection
Edit `app.py` to add PIN validation:

```python
PIN_CODE = "1234"  # Change this

@socketio.on('connect')
def on_connect(auth):
    if PIN_ENABLED and auth.get('pin') != PIN_CODE:
        return False  # Reject connection
```

### Add Rate Limiting Per Device
```python
MAX_MESSAGES_PER_MINUTE = 30
MAX_FILES_PER_DAY = 100
```

### HTTPS Setup (Nginx Reverse Proxy)
```nginx
server {
    listen 443 ssl http2;
    server_name isodrop.example.com;

    ssl_certificate /etc/ssl/certs/isodrop.crt;
    ssl_certificate_key /etc/ssl/private/isodrop.key;

    location / {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

## Monitoring

### Check Active Connections
```bash
# Linux
netstat -an | grep 5000

# macOS
lsof -i :5000
```

### View Logs
```bash
# Enable debug logging in app.py
app.logger.setLevel(logging.DEBUG)
```

### Monitor Temp Files
```bash
# Check disk usage
du -sh /tmp/isodrop

# Remove old files manually
find /tmp/isodrop -mtime +1 -delete
```

## Troubleshooting Configuration

### Port Already in Use
```bash
# Find process using port 5000
lsof -i :5000

# Kill it
kill -9 <PID>

# Or change port in .env
SERVER_PORT=8000
```

### Memory Issues with Large Files
- Reduce `CHUNK_SIZE_MB` for streaming
- Increase server RAM
- Implement disk buffering instead of memory

### Slow Uploads
- Check network bandwidth
- Increase `CHUNK_SIZE_MB` if network is stable
- Use wired connection for large files

---

**For more info, see README.md**
