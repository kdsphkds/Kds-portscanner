# PyPortScanner 🔍

A professional-grade educational port scanner built in Python. Perfect for learning cybersecurity fundamentals in restricted environments like Replit.

## ⚠️ **SECURITY & ETHICAL WARNING**
**THIS IS AN EDUCATIONAL TOOL FOR LEARNING PURPOSES ONLY.**
- Only scan systems you own or have explicit written permission to test
- Unauthorized port scanning is illegal in many jurisdictions
- You are solely responsible for your actions

## 🚀 Quick Start (Replit)

1. **Click the "Run" button** in Replit
2. **Try these examples** in the console:
   ```bash
   python main.py scanme.nmap.org
   python main.py 192.168.1.1 -p 80,443
   python main.py example.com -p 1-100 -o json
   python main.py test.local --top-ports 50 -o csv

## Sample output
PORT    STATE   SERVICE         BANNER
22      open    ssh             SSH-2.0-OpenSSH_8.9p1 Ubuntu...
80      open    http            HTTP/1.1 200 OK\r\nServer: ngin...
443     open    https           HTTP/1.1 200 OK\r\nServer: Apac...