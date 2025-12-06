#!/usr/bin/env python3
"""
Educational Port Scanner
A safe, learning-focused port scanner for cybersecurity education.
"""

import argparse
import socket
import time
import json
import csv
import random
from typing import List, Dict, Optional
import sys

# Common ports and their services
COMMON_PORTS = {
    20: "ftp-data", 21: "ftp", 22: "ssh", 23: "telnet", 25: "smtp",
    53: "dns", 67: "dhcp", 68: "dhcp", 69: "tftp", 80: "http",
    110: "pop3", 119: "nntp", 123: "ntp", 137: "netbios-ns",
    138: "netbios-dgm", 139: "netbios-ssn", 143: "imap", 161: "snmp",
    162: "snmptrap", 179: "bgp", 194: "irc", 389: "ldap",
    443: "https", 445: "microsoft-ds", 465: "smtps", 514: "syslog",
    515: "printer", 587: "smtp-submission", 631: "ipp", 636: "ldaps",
    993: "imaps", 995: "pop3s", 1080: "socks", 1194: "openvpn",
    1433: "mssql", 1521: "oracle", 1723: "pptp", 2049: "nfs",
    2082: "cpanel", 2083: "cpanel-ssl", 2086: "whm", 2087: "whm-ssl",
    2095: "webmail", 2096: "webmail-ssl", 2222: "directadmin",
    2375: "docker", 2376: "docker-ssl", 3000: "node", 3306: "mysql",
    3389: "rdp", 5432: "postgresql", 5900: "vnc", 5984: "couchdb",
    6379: "redis", 7474: "neo4j", 8000: "http-alt", 8080: "http-proxy",
    8443: "https-alt", 8888: "sun-answerbook", 9000: "jenkins",
    9001: "tor", 9042: "cassandra", 9090: "cockpit", 9200: "elastic",
    9300: "elastic", 27017: "mongodb", 28017: "mongodb-http",
}

class PortScanner:
    """Educational port scanner for learning networking concepts."""
    
    def __init__(self, timeout: float = 1.0, simulate: bool = True):
        """
        Initialize the port scanner.
        
        Args:
            timeout: Socket timeout in seconds
            simulate: If True, use simulation mode (safe for learning)
        """
        self.timeout = timeout
        self.simulate = simulate
        self.current_target = None
        self.start_time = None
        self.scan_results = []
        
    def _real_scan_port(self, target: str, port: int, timeout: float) -> bool:
        """
        Perform actual socket connection to check port status.
        
        Args:
            target: Hostname or IP address
            port: Port number to scan
            timeout: Connection timeout
            
        Returns:
            True if port is open, False otherwise
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((target, port))
            sock.close()
            return result == 0
        except:
            return False
    
    def _should_port_be_open(self, port: int) -> bool:
        """
        Determine if a port is open. Uses real scan when not in simulation mode.
        
        Args:
            port: Port number to check
            
        Returns:
            True if port is open (or simulated as open), False otherwise
        """
        if not self.simulate:  # REAL MODE
            return self._real_scan_port(self.current_target, port, self.timeout)
        else:  # SIMULATION MODE
            # Educational simulation - higher chance for common ports
            if port in COMMON_PORTS:
                return random.random() < 0.4  # 40% chance for common ports
            return random.random() < 0.1  # 10% chance for other ports
    
    def _get_service_banner(self, port: int, is_open: bool) -> str:
        """
        Get simulated or real service banner.
        
        Args:
            port: Port number
            is_open: Whether the port is open
            
        Returns:
            Service banner string
        """
        if not is_open:
            return ""
            
        # Common service banners
        banners = {
            22: "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.3",
            80: "HTTP/1.1 200 OK\nServer: nginx/1.18.0\nDate: ...",
            443: "HTTP/1.1 200 OK\nServer: Apache/2.4.41\n...",
            3306: "5.7.32\x00...MySQL",  # MySQL handshake
            3389: "\x03\x00\x00\x13\x0e\xd0\x00\x00\x124\x00\x02",  # RDP
            5432: "E\x00\x00\x00\x0c\x00\x00\x00\x00",  # PostgreSQL
        }
        
        if port in banners:
            return banners[port]
        
        # Generic banners for common services
        if port in COMMON_PORTS:
            service = COMMON_PORTS[port]
            if "http" in service:
                return f"HTTP/1.1 200 OK\nServer: {random.choice(['nginx', 'Apache', 'lighttpd'])}"
            elif service in ["ssh", "ftp", "smtp"]:
                return f"220 {service.upper()} Service Ready"
        
        return f"{COMMON_PORTS.get(port, 'Unknown')} service detected"
    
    def simulate_scan(self, target: str, ports: List[int]) -> List[Dict]:
        """
        Simulate scanning ports with realistic delays and results.
        Perfect for learning in restricted environments like Replit.
        
        Args:
            target: Target hostname or IP
            ports: List of ports to scan
            
        Returns:
            List of scan results
        """
        self.current_target = target
        self.start_time = time.time()
        self.scan_results = []
        
        print(f"[*] Scanning {len(ports)} ports on {target}")
        print(f"[*] Mode: {'Simulation' if self.simulate else 'Real Socket'}")
        
        for i, port in enumerate(ports, 1):
            # Realistic delay for educational purposes
            if not self.simulate:
                time.sleep(0.05)  # Small delay for real scans
            else:
                time.sleep(0.02)  # Faster for simulation
            
            # Show progress
            if i % max(1, len(ports) // 10) == 0 or i == len(ports):
                progress = (i / len(ports)) * 100
                print(f"    Progress: {i}/{len(ports)} ports ({progress:.1f}%)")
            
            # Check port
            is_open = self._should_port_be_open(port)
            banner = ""
            
            if is_open:
                banner = self._get_service_banner(port, is_open)
                print(f"    [+] Port {port}/tcp open - {COMMON_PORTS.get(port, 'unknown')}")
            
            self.scan_results.append({
                'port': port,
                'state': 'open' if is_open else 'closed',
                'service': COMMON_PORTS.get(port, 'unknown'),
                'banner': banner
            })
        
        return self.scan_results
    
    def get_scan_summary(self) -> Dict:
        """Get scan statistics and summary."""
        if not self.scan_results:
            return {}
        
        open_ports = [r for r in self.scan_results if r['state'] == 'open']
        duration = time.time() - self.start_time if self.start_time else 0
        
        return {
            'target': self.current_target,
            'total_ports': len(self.scan_results),
            'open_ports': len(open_ports),
            'duration': duration,
            'mode': 'simulation' if self.simulate else 'real'
        }

def get_ports_to_scan(port_spec: str, top_ports: int = 20) -> List[int]:
    """
    Parse port specification into list of port numbers.
    
    Args:
        port_spec: Port specification (top, common, all, range, or list)
        top_ports: Number of top ports when using 'top'
        
    Returns:
        List of port numbers
    """
    port_spec = port_spec.lower().strip()
    
    if port_spec == 'top':
        # Return top N most common ports
        sorted_ports = sorted(COMMON_PORTS.keys())
        return sorted_ports[:min(top_ports, len(sorted_ports))]
    
    elif port_spec == 'common':
        # Return all known common ports
        return list(COMMON_PORTS.keys())
    
    elif port_spec == 'all':
        # Return 1-1024 (well-known ports)
        return list(range(1, 1025))
    
    elif '-' in port_spec:
        # Port range like "1-100"
        try:
            start, end = map(int, port_spec.split('-'))
            return list(range(start, end + 1))
        except:
            print(f"[-] Invalid port range: {port_spec}")
            return []
    
    elif ',' in port_spec:
        # Comma-separated list like "22,80,443"
        try:
            ports = []
            for part in port_spec.split(','):
                if '-' in part:
                    start, end = map(int, part.split('-'))
                    ports.extend(range(start, end + 1))
                else:
                    ports.append(int(part.strip()))
            return sorted(set(ports))
        except:
            print(f"[-] Invalid port list: {port_spec}")
            return []
    
    else:
        # Single port
        try:
            return [int(port_spec)]
        except:
            print(f"[-] Invalid port specification: {port_spec}")
            return []

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
    parser.add_argument('--real', action='store_true',
                       help='Perform real socket scanning (not simulation)')
    parser.add_argument('--top-ports', type=int, default=20,
                       help='Number of top ports to scan when using "top"')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Show detailed information')
    
    return parser.parse_args()

def print_results_table(results: List[Dict], summary: Dict):
    """Print results in table format."""
    print("\n" + "="*60)
    print("SCAN RESULTS".center(60))
    print("="*60)
    
    if not results:
        print("No ports scanned.")
        return
    
    # Print header
    print(f"{'PORT':<8} {'STATE':<10} {'SERVICE':<20} {'BANNER':<30}")
    print("-" * 60)
    
    # Print results
    for result in results:
        if result['state'] == 'open' or args.verbose:
            port = result['port']
            state = result['state']
            service = result['service']
            banner = result['banner'].split('\n')[0][:28] + "..." if len(result['banner'].split('\n')[0]) > 28 else result['banner'].split('\n')[0]
            print(f"{port:<8} {state:<10} {service:<20} {banner:<30}")
    
    print("="*60)
    print(f"\n[*] Target: {summary.get('target', 'Unknown')}")
    print(f"[*] Scanned {summary.get('total_ports', 0)} ports")
    print(f"[*] Found {summary.get('open_ports', 0)} open ports")
    print(f"[*] Mode: {summary.get('mode', 'unknown').upper()}")
    print(f"[*] Duration: {summary.get('duration', 0):.2f} seconds")
    print("="*60)

def print_educational_info():
    """Print educational information about port scanning."""
    print("\n" + "="*50)
    print("EDUCATIONAL PORT SCANNER - CYBERSECURITY LEARNING TOOL")
    print("="*50 + "\n")
    
    print("🔍 What this teaches you:")
    print("- How port scanners enumerate services")
    print("- Common port/service mappings")
    print("- Network protocol fundamentals")
    print("- Security assessment methodology\n")
    
    print("⚠️ Important Notes:")
    print("- This tool is for EDUCATIONAL PURPOSES ONLY")
    print("- Always get permission before scanning any network")
    print("- Use simulation mode in restricted environments")
    print("- Real scanning requires proper network access\n")

def print_real_world_instructions():
    """Print instructions for real-world practice."""
    print("\n" + "="*50)
    print("NEXT STEPS FOR REAL-WORLD TESTING:")
    print("="*50 + "\n")
    
    print("1. To run real scans, install on your local machine:")
    print("   pip install scapy\n")
    
    print("2. Replace simulation with real socket code:")
    print("   import socket")
    print("   sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)")
    print("   result = sock.connect_ex((target, port))\n")
    
    print("3. Practice legally on:")
    print("   - HackTheBox (https://www.hackthebox.com)")
    print("   - TryHackMe (https://tryhackme.com)")
    print("   - VulnHub (https://www.vulnhub.com)\n")
    
    print("4. Always: GET PERMISSION BEFORE SCANNING")
    print("="*50)

def save_results(results: List[Dict], summary: Dict, filename: str, format_type: str):
    """Save scan results to file."""
    if format_type == 'json':
        data = {
            'scan_results': results,
            'summary': summary,
            'timestamp': time.time()
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"[*] Results saved to {filename}")
    
    elif format_type == 'csv':
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['port', 'state', 'service', 'banner'])
            writer.writeheader()
            for result in results:
                writer.writerow(result)
        print(f"[*] Results saved to {filename}")

def main():
    """Main function."""
    global args
    args = parse_arguments()
    
    # Get ports to scan
    ports = get_ports_to_scan(args.ports, args.top_ports)
    if not ports:
        print("[-] No valid ports to scan.")
        return
    
    # Print educational info (only in simulation mode or first run)
    if not args.real:
        print_educational_info()
    
    print(f"Target: {args.target}")
    print(f"Ports to scan: {len(ports)}")
    print(f"Mode: {'Real Socket Scanning' if args.real else 'Simulation (Educational)'}")
    print()
    
    # Create and run scanner
    scanner = PortScanner(simulate=not args.real, timeout=1.0)
    results = scanner.simulate_scan(args.target, ports)
    summary = scanner.get_scan_summary()
    
    # Display results
    if args.output == 'table':
        print_results_table(results, summary)
    elif args.output in ['json', 'csv']:
        filename = f"scan_results_{args.target.replace('.', '_')}_{int(time.time())}.{args.output}"
        save_results(results, summary, filename, args.output)
        print(f"\n[*] Scan completed in {summary.get('duration', 0):.2f} seconds")
        print(f"[*] Found {summary.get('open_ports', 0)} open ports")
    
    # Show educational footer
    if not args.real:
        print_real_world_instructions()

if __name__ == "__main__":
    main()
