# ISODROP - VISUAL GUIDE & FEATURE WALKTHROUGH

## 🎨 UI Layout

```
┌─────────────────────────────────────────────────────────────────┐
│                         ISODROP 🚀                             │
├──────────────────┬───────────────────────────────────────────────┤
│                  │                                               │
│   SIDEBAR        │              MAIN AREA                        │
│   (320px)        │          (Flexible Width)                     │
│                  │                                               │
│ ┌──────────────┐ │ ┌─────────────────────────────────────────┐  │
│ │ Header Card  │ │ │     💬 Shared Content                   │  │
│ │  🚀 ISODROP  │ │ │                                         │  │
│ └──────────────┘ │ │  ┌──────────────────────────────────┐  │  │
│                  │ │  │ 📨 Alice                         │  │  │
│ ┌──────────────┐ │ │  │ Hello everyone!                  │  │  │
│ │ Device Count │ │ │  │ 2:30 PM                          │  │  │
│ │   • 4        │ │ │  └──────────────────────────────────┘  │  │
│ │   Connected  │ │ │                                         │  │
│ └──────────────┘ │ │  ┌──────────────────────────────────┐  │  │
│                  │ │  │ 🎬 Bob                           │  │  │
│ ┌──────────────┐ │ │  │ ┌─────────────────────────────┐  │  │  │
│ │ QR Section   │ │ │  │ │ 🎬 movie.mp4               │  │  │  │
│ │ ┌──────────┐ │ │ │  │ │ 500MB • Bob               │  │  │  │
│ │ │  [QR]    │ │ │ │  │ │ █████████████ 100%      │  │  │  │
│ │ └──────────┘ │ │ │  │ │ [Download] [Play]        │  │  │  │
│ │ http://...   │ │ │  │ └─────────────────────────────┘  │  │  │
│ └──────────────┘ │ │  └──────────────────────────────────┘  │  │
│                  │ │                                         │  │
│ ┌──────────────┐ │ │  [Input] Share a message... [Send]     │  │
│ │  👥 Active   │ │ └─────────────────────────────────────────┘  │
│ │ Devices      │ │                                               │
│ │              │ │                                               │
│ │ ┌──────────┐ │ │                                               │
│ │ │ 👤 Alice │ │ │                                               │
│ │ │ 🟢 Online│ │ │                                               │
│ │ └──────────┘ │ │                                               │
│ │              │ │                                               │
│ │ ┌──────────┐ │ │                                               │
│ │ │ 👥 Bob   │ │ │                                               │
│ │ │ 🟢 Online│ │ │                                               │
│ │ └──────────┘ │ │                                               │
│ └──────────────┘ │                                               │
│                  │                                               │
│ ┌──────────────┐ │                                               │
│ │ Upload Zone  │ │                                               │
│ │              │ │                                               │
│ │   📤         │ │                                               │
│ │ Drag files   │ │                                               │
│ │ here or click │ │                                               │
│ └──────────────┘ │                                               │
└──────────────────┴───────────────────────────────────────────────┘
```

## 🎯 Feature Flow Diagram

```
USER JOINS ISODROP
    ↓
┌─────────────────────────────────────────┐
│ 1. Enter URL or Scan QR Code           │
│    http://192.168.1.100:5000           │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ 2. Page Loads with Beautiful UI        │
│    - Dark theme                         │
│    - Live device counter (1)            │
│    - Upload zone ready                  │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ 3. Connect to Server                    │
│    - Device ID generated                │
│    - Device registered in room          │
│    - Broadcast: "New device joined!"    │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ 4. Now You Can:                         │
│    - See live device list               │
│    - Send messages instantly            │
│    - Upload files                       │
│    - Watch progress in real-time        │
│    - Download files from others         │
└─────────────────────────────────────────┘
```

## 📊 Message Flow

```
USER A (Device 1)          Server              USER B (Device 2)
───────────────────────────────────────────────────────────────

Type "Hello!"
    │
    ├─ emit('message') ──────→ Receive message
    │                         Validate input
    │                         Broadcast to all
    │                                        ← broadcast('new_message')
    │                                        Display in UI
    │                                        Play sound/toast

```

## 📁 File Upload/Download Flow

```
USER A                     Server                 USER B
──────────────────────────────────────────────────────────

Select file
    │
    ├─ emit('file_upload_start') ──→ Generate file_id
    │                                Create transfer object
    │                                Return chunk_size ───→
    │
    ├─ Split into 1MB chunks
    ├─ emit('file_chunk', data) ──→ Write chunk to disk
    │  emit('file_chunk', data) ──→ Write chunk to disk
    │  emit('file_chunk', data) ──→ Write chunk to disk
    │                                [Progress: 25%, 50%, 75%]
    │                                                     ← broadcast progress
    │                                                     Update progress bar
    │
    ├─ emit('file_upload_complete') ──→ Finalize file
    │                                    Emit to all
    │                                             ← broadcast('new_file')
    │                                             File appears in list
    │                                             [Download] button active
    │
    │                                    USER B CLICKS DOWNLOAD
    │                                    GET /download/file_id ───→
    │                                    File streamed from disk
    │                                    Saved to device ✅
```

## 🎨 Color Palette

```
Primary:   #00d9ff (Cyan) - Main accent, borders, highlights
Secondary: #ff006e (Pink) - Hover effects, alternative accent
Accent:    #8338ec (Purple) - Gradients, shadows
Dark BG:   #0a0e27 (Dark Blue) - Main background
Card BG:   rgba(15,20,45,0.7) - Card backgrounds
Border:    rgba(0,217,255,0.3) - Subtle borders
Text:      #ffffff (White) - Primary text
Secondary: #b0b7c0 (Gray) - Smaller text
Success:   #06ffa5 (Green) - Success notifications
Error:     #ff006e (Pink) - Error notifications
```

## 📱 Responsive Breakpoints

```
Desktop (> 1024px):
┌─────────────────────────────────┐
│ Sidebar (320px)  │  Main (flex)  │
│ [Fixed]          │  [Grows]      │
└─────────────────────────────────┘

Tablet (768-1024px):
┌─────────────────────────────────┐
│ Sidebar (horizontal scroll)      │
└─────────────────────────────────┘
┌─────────────────────────────────┐
│ Main area (takes full width)     │
└─────────────────────────────────┘

Mobile (< 768px):
┌─────────────────────────────────┐
│ Sidebar (horizontal, compact)    │
└─────────────────────────────────┘
┌─────────────────────────────────┐
│ Messages + Input (full width)    │
└─────────────────────────────────┘
```

## 🔄 Real-time Sync Timeline

```
Time: 0ms
└─ Device A connects

Time: 50ms
└─ Device B connects
└─ Both receive updated device list (2 devices)

Time: 100ms
└─ Device A sends message "Hello"

Time: 110ms (WebSocket latency)
└─ All devices (A, B) receive message
└─ Message appears instantly in UI

Time: 500ms
└─ Device B sends file (1MB)

Time: 510ms
└─ Server receives chunk
└─ Device A receives progress event (progress: 25%)
└─ Progress bar updates

Time: 1500ms
└─ File upload complete
└─ All devices receive file info
└─ File appears in content area

```

## 🎭 Animation Keyframes

```
Float Animation (upload icon):
0%    ↑ y = 0
50%   ↓ y = -10px
100%  ↑ y = 0

Pulse Animation (device counter):
0%    ● scale=1, opacity=1
50%   ◎ scale=1.2, opacity=0.5
100%  ● scale=1, opacity=1

Slide In Animation (messages):
0%    ┌─────┐
      │···· │  opacity: 0, y: +10px
      └─────┘

100%  ┌─────┐
      │Text │  opacity: 1, y: 0
      └─────┘

Hover Effect (cards):
Before: Normal appearance
After:  Border glow + slight lift
```

## 🚀 Performance Metrics

```
Page Load:
├─ HTML parse: 50ms
├─ CSS render: 100ms
├─ JS execute: 150ms
├─ Socket.IO init: 200ms
└─ Total: ~500ms

Message Send:
├─ Client emit: 1ms
├─ Network: 30-100ms
├─ Server process: 5ms
├─ Broadcast: 10ms
├─ UI render: 50ms
└─ Total: 96-156ms

File Upload (1GB):
├─ Chunking: ~200ms
├─ First chunk: 100ms
├─ Chunks 2-1000: ~100ms per chunk
└─ Total: ~100s (depends on network)

```

## 📊 Data Structure

```
Device Object:
{
  id: "abc12345",
  session_id: "xyz789",
  name: "Alice's Phone",
  joined_at: "2024-01-28T10:30:00",
  is_online: true
}

Message Object:
{
  id: "msg-123",
  sender_id: "abc12345",
  sender_name: "Alice",
  text: "Hello everyone!",
  timestamp: "2024-01-28T10:31:00",
  type: "text"
}

File Object:
{
  file_id: "file-xyz",
  filename: "vacation.mp4",
  file_size: 500000000,
  mime_type: "video/mp4",
  sender_id: "abc12345",
  sender_name: "Bob",
  timestamp: "2024-01-28T10:32:00",
  type: "file"
}
```

## 🔌 Socket.IO Events Reference

```
CLIENT → SERVER:
├─ 'connect' - Device connects
├─ 'disconnect' - Device leaves
├─ 'message' - Send text message
├─ 'file_upload_start' - Initiate file upload
├─ 'file_chunk' - Send file chunk
├─ 'file_upload_complete' - Upload finished
├─ 'get_devices' - Request device list
├─ 'set_device_name' - Change device name
├─ 'ping' - Heartbeat

SERVER → CLIENT (broadcast):
├─ 'device_connected' - New device joined
├─ 'device_disconnected' - Device left
├─ 'device_updated' - Device info changed
├─ 'new_message' - New text message
├─ 'new_file' - New file available
├─ 'file_upload_progress' - Upload progress
├─ 'error' - Error notification
├─ 'pong' - Heartbeat response
```

## 💾 Storage Locations

```
Windows:
C:\Users\<username>\isodrop_temp\

macOS/Linux:
/tmp/isodrop/

File structure:
isodrop_temp/
├─ <file-id-1> (raw binary data)
├─ <file-id-2> (raw binary data)
├─ <file-id-3> (raw binary data)
└─ Auto-cleaned after 24 hours

```

## 🎯 User Journey Map

```
AWARENESS          ONBOARDING         USAGE              ENGAGEMENT
───────────────────────────────────────────────────────────────────

Sees QR code    →   Scans or    →   Sees devices  →   Keeps sending
                    types URL        and counter        files/messages

Reads URL       →   Page loads  →   Sends message →   Shares with
                    beautifully      to all others      others

Clicks link     →   Interface  →    Uploads file  →   Recommends
                    appears         instantly         to friends

```

## 🎊 Toast Notification Types

```
SUCCESS (Green border, green text):
┌─────────────────────────────────┐
│ ✓ File uploaded successfully!  │
└─────────────────────────────────┘

ERROR (Pink border, pink text):
┌─────────────────────────────────┐
│ ✗ Failed to connect to server  │
└─────────────────────────────────┘

INFO (Cyan border, white text):
┌─────────────────────────────────┐
│ ℹ New device joined: Bob's PC  │
└─────────────────────────────────┘
```

---

**This visual guide helps understand ISODROP's structure, flow, and UI at a glance!**
