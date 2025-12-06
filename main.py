#!/usr/bin/env python3
"""
PyPortScanner - Educational Cybersecurity Tool
Simulates port scanning to teach networking fundamentals.
"""

import argparse
import json
import csv
import time
import random
import sys
from datetime import datetime
from typing import List, Dict

# ==================== CORE SCANNER CLASS ====================
class EducationalPortScanner:
    """Simulates port scanning for educational purposes."""
    
    COMMON_PORTS = {
        21: 'ftp', 22: 'ssh', 23: 'telnet', 25: 'smtp',
        53: 'dns', 80: 'http', 110: 'pop3', 143: 'imap',
        443: 'https', 445: 'samba', 3389: 'rdp',
        5900: 'vnc', 8080: 'http-proxy', 8443: 'https-alt'
    }
    
    def __init__(self, timeout: float = 1.0):
        self.timeout = timeout
        self.scan_results = []
        self.scan_duration = 0
        self.start_time = None
        
    def simulate_scan(self, target: str, ports: List[int]) -> List[Dict]:
        """
        Simulate scanning ports with realistic delays and results.
        Perfect for learning in restricted environments like Replit.
        """
        self.start_time = time.time()
        self.scan_results = []
        
        print(f"[*] Starting simulated scan of {target}")
        print(f"[*] Scanning {len(ports)} ports in educational mode")
        print("-" * 50)
        
        for i, port in enumerate(ports, 1):
            # Realistic scan delay simulation
            time.sleep(random.uniform(0.05, 0.15))
            
            # Progress indicator
            if i % 10 == 0:
                sys.stdout.write(f"\r[*] Progress: {i}/{len(ports)} ports")
                sys.stdout.flush()
            
            # Simulate finding open ports
            is_open = self._should_port_be_open(port)
            result = self._create_port_result(target, port, is_open)
            
            if is_open:
                self.scan_results.append(result)
                
        self.scan_duration = time.time() - self.start_time
        print(f"\n\n[*] Scan completed in {self.scan_duration:.2f} seconds")
        return self.scan_results
    
    def _should_port_be_open(self, port: int) -> bool:
        """Realistic logic for determining if a port should appear open."""
        # Common ports are more likely to be "open" in simulation
        if port in self.COMMON_PORTS:
            return random.random() < 0.4  # 40% chance for common ports
        return random.random() < 0.1  # 10% chance for others
    
    def _create_port_result(self, target: str, port: int, is_open: bool) -> Dict:
        """Create a detailed result dictionary for a port."""
        result = {
            'target': target,
            'port': port,
            'state': 'open' if is_open else 'closed',
            'service': self.COMMON_PORTS.get(port, 'unknown'),
            'timestamp': datetime.now().isoformat(),
            'protocol': 'tcp'
        }
        
        if is_open:
            result['banner'] = self._generate_banner(port)
            result['version'] = self._generate_version_info(port)
            
        return result
    
    def _generate_banner(self, port: int) -> str:
        """Generate realistic service banners."""
        banners = {
            22: 'SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.4',
            80: 'HTTP/1.1 200 OK\r\nServer: nginx/1.18.0\r\n',
            443: 'HTTP/1.1 200 OK\r\nServer: Apache/2.4.41\r\n',
            21: '220 ProFTPD Server (Debian)',
            25: '220 mail.example.com ESMTP Postfix',
            3389: '\x03\x00\x00\x13\x0e\xd0\x00\x00\x12\x34\x00\x02\x0f\x08\x00\x02\x00\x00\x00'
        }
        return banners.get(port, 'Generic Service Ready')
    
    def _generate_version_info(self, port: int) -> str:
        """Generate version information for open services."""
        versions = {
            22: 'OpenSSH 8.9',
            80: 'nginx 1.18',
            443: 'Apache 2.4.41',
            21: 'ProFTPD 1.3.7',
        }
        return versions.get(port, 'Unknown')
    
    def export_results(self, format_type: str = 'table') -> str:
        """Export results in various formats."""
        if not self.scan_results:
            return "No open ports found."
        
        if format_type == 'json':
            return json.dumps(self.scan_results, indent=2)
        
        elif format_type == 'csv':
            output = ['port,state,service,banner,protocol']
            for result in self.scan_results:
                banner = result.get('banner', '').replace('"', '""').replace('\n', '\\n')
                output.append(f'{result["port"]},{result["state"]},{result["service"]},"{banner}",{result["protocol"]}')
            return '\n'.join(output)
        
        else:  # table format
            output = ["PORT    STATE   SERVICE         BANNER"]
            output.append("-" * 60)
            for result in self.scan_results:
                banner_preview = result.get('banner', 'No banner')[0:30] + "..." if len(result.get('banner', '')) > 30 else result.get('banner', 'No banner')
                output.append(f'{result["port"]:<7} {result["state"]:<7} {result["service"]:<15} {banner_preview}')
            return '\n'.join(output)

# ==================== COMMAND LINE INTERFACE ====================
def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Educational Port Scanner - Learn networking fundamentals',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s scanme.nmap.org                     # Scan common ports
  %(prog)s 192.168.1.1 -p 80,443,8080         # Scan specific ports
  %(prog)s example.com -p 1-100 -o json       # Output in JSON format
  %(prog)s test.local --top-ports 50          # Scan top 50 ports
        """
    )
    
    parser.add_argument('target', help='Target hostname or IP address')
    parser.add_argument('-p', '--ports', default='top',
                       help='Ports to scan: "top", "all", "common", or range like "1-100" or list like "22,80,443"')
    parser.add_argument('-o', '--output', choices=['table', 'json', 'csv'], 
                       default='table', help='Output format')
    parser.add_argument('--top-ports', type=int, default=20,
                       help='Number of top ports to scan when using "top"')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Show detailed information')
    
    return parser.parse_args()

def get_ports_to_scan(ports_arg: str, top_count: int = 20) -> List[int]:
    """Convert ports argument to list of port numbers."""
    # Top ports list (based on real-world frequency)
    TOP_PORTS = [80, 443, 22, 21, 25, 110, 143, 53, 3389, 23, 
                 445, 139, 135, 8080, 8443, 3306, 5432, 5900, 
                 161, 162]
    
    if ports_arg == 'top':
        return TOP_PORTS[:top_count]
    elif ports_arg == 'common':
        return list(EducationalPortScanner.COMMON_PORTS.keys())
    elif ports_arg == 'all':
        return list(range(1, 1025))  # Well-known ports
    elif '-' in ports_arg:
        start, end = map(int, ports_arg.split('-'))
        return list(range(start, end + 1))
    elif ',' in ports_arg:
        return [int(p) for p in ports_arg.split(',')]
    else:
        return [int(ports_arg)]

def display_educational_info(target: str, ports: List[int]):
    """Show educational information about the scan."""
    print("\n" + "="*60)
    print("EDUCATIONAL PORT SCANNER - CYBERSECURITY LEARNING TOOL")
    print("="*60)
    print(f"\nTarget: {target}")
    print(f"Ports to scan: {len(ports)}")
    print(f"Mode: Simulation (Replit-friendly)")
    print("\n🔍 What this teaches you:")
    print("  • How port scanners enumerate services")
    print("  • Common port/service mappings")
    print("  • Network protocol fundamentals")
    print("  • Security assessment methodology")
    print("\n⚠️  Important Notes:")
    print("  • This is a SIMULATION for learning")
    print("  • Real scanning requires raw socket access")
    print("  • Always get permission before scanning")
    print("="*60 + "\n")

# ==================== MAIN EXECUTION ====================
def main():
    """Main program entry point."""
    args = parse_arguments()
    
    # Get ports to scan
    ports = get_ports_to_scan(args.ports, args.top_ports)
    
    # Display educational header
    display_educational_info(args.target, ports)
    
    # Create scanner and run simulation
    scanner = EducationalPortScanner()
    
    if args.verbose:
        print(f"[*] Scanning {args.target}")
        print(f"[*] Port range: {min(ports)}-{max(ports)}")
        print(f"[*] Total ports: {len(ports)}")
    
    # Run the simulated scan
    results = scanner.simulate_scan(args.target, ports)
    
    # Display results
    print("\n" + "="*60)
    print("SCAN RESULTS")
    print("="*60)
    print(scanner.export_results(args.output))
    
    # Statistics
    print(f"\n[*] Found {len(results)} open ports")
    print(f"[*] Scan duration: {scanner.scan_duration:.2f} seconds")
    
    # Real-world next steps
    print("\n" + "="*60)
    print("NEXT STEPS FOR REAL-WORLD TESTING:")
    print("="*60)
    print("1. To run real scans, install on your local machine:")
    print("   pip install scapy")
    print("\n2. Replace simulation with real socket code:")
    print("   import socket")
    print("   sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)")
    print("   result = sock.connect_ex((target, port))")
    print("\n3. Practice legally on:")
    print("   • HackTheBox (https://www.hackthebox.com)")
    print("   • TryHackMe (https://tryhackme.com)")
    print("   • VulnHub (https://www.vulnhub.com)")
    print("\n4. Always: GET PERMISSION BEFORE SCANNING")
    print("="*60)

if __name__ == '__main__':
    main()