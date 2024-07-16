import socket
import ssl
from concurrent.futures import ThreadPoolExecutor
import argparse
from datetime import datetime

# Predefined list of current software versions (for demonstration purposes)
# In a real-world scenario, this should be dynamically fetched from an up-to-date source.
current_versions = {
    "http": "2.4.52",
    "ssh": "8.6",
    "ftp": "7.68"
}

# Function to grab the banner
def grab_banner(target, port):
    s = socket.socket()
    s.settimeout(1)
    try:
        s.connect((target, port))
        s.send(b"HEAD / HTTP/1.0\r\n\r\n")
        banner = s.recv(1024).decode().strip()
        return banner
    except:
        return None
    finally:
        s.close()

# Function to parse the banner and extract the software and version
def parse_banner(banner):
    if "Server:" in banner:
        parts = banner.split("Server:")[1].strip().split(" ")
        if len(parts) >= 2:
            return parts[0], parts[1]
    return None, None

# Function to check for SSL misconfigurations
def check_ssl_certificate(target, port):
    misconfigurations = []
    context = ssl.create_default_context()
    with socket.create_connection((target, port)) as sock:
        with context.wrap_socket(sock, server_hostname=target) as ssock:
            cert = ssock.getpeercert()
            if not cert:
                misconfigurations.append("No SSL certificate found")
            else:
                # Check for expiration date
                expiry_date = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                if expiry_date < datetime.now():
                    misconfigurations.append("SSL certificate expired")
                
                # Check for self-signed certificate
                if cert['issuer'] == cert['subject']:
                    misconfigurations.append("Self-signed SSL certificate")
                
                # Check for weak encryption (simplified example, real-world checks would be more comprehensive)
                if ssock.cipher()[1] < 128:
                    misconfigurations.append("Weak encryption algorithm used")
    return misconfigurations

# Function to check for other misconfigurations
def check_misconfigurations(target, port, software):
    misconfigurations = []

    # Example misconfiguration check for HTTP
    if software.lower() == "http":
        s = socket.socket()
        s.settimeout(1)
        try:
            s.connect((target, port))
            s.send(b"GET /server-status HTTP/1.0\r\n\r\n")
            response = s.recv(1024).decode().strip()
            if "200 OK" in response:
                misconfigurations.append("Server-status page is accessible")
        except:
            pass
        finally:
            s.close()

    # Example misconfiguration check for FTP
    if software.lower() == "ftp":
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        try:
            s.connect((target, port))
            s.send(b"USER anonymous\r\n")
            response = s.recv(1024).decode().strip()
            if "230" in response:
                misconfigurations.append("Anonymous FTP login allowed")
        except:
            pass
        finally:
            s.close()

    # Example misconfiguration check for SSH
    if software.lower() == "ssh":
        # Simplified example, real-world checks would require more sophisticated SSH library
        if port == 22:
            misconfigurations.append("SSH on default port")

    return misconfigurations

# Function to scan a single port
def scan_port(target, port, verbose):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect((target, port))
        banner = grab_banner(target, port)
        software, version = parse_banner(banner) if banner else (None, None)
        is_open = True
        if verbose:
            print(f"Port {port} is open")
            if software and version:
                print(f"  Running {software} version {version}")
        misconfigurations = check_misconfigurations(target, port, software) if software else []
        if port in [443, 8443]:  # Common SSL ports
            ssl_misconfigs = check_ssl_certificate(target, port)
            misconfigurations.extend(ssl_misconfigs)
        return port, is_open, software, version, misconfigurations
    except (socket.timeout, ConnectionRefusedError):
        if verbose:
            print(f"Port {port} is closed")
        return port, False, None, None, []
    finally:
        s.close()

# Main function to scan ports in the given range
def main(target, start_port, end_port, max_workers, verbose):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = executor.map(lambda port: scan_port(target, port, verbose), range(start_port, end_port + 1))

    open_ports = []
    outdated_software = []
    misconfigurations = []

    for port, is_open, software, version, misconfigs in results:
        if is_open:
            open_ports.append(port)
            if software and version:
                current_version = current_versions.get(software.lower())
                if current_version and version < current_version:
                    outdated_software.append((port, software, version, current_version))
            if misconfigs:
                misconfigurations.append((port, software, misconfigs))
    
    if open_ports:
        print(f"Open ports on {target}: {open_ports}")
    else:
        print(f"No open ports found on {target} in the range {start_port}-{end_port}")

    if outdated_software:
        print("Outdated software versions detected:")
        for port, software, version, current_version in outdated_software:
            print(f"  Port {port}: {software} {version} (current: {current_version})")
    else:
        print("No outdated software versions detected.")

    if misconfigurations:
        print("Misconfigurations detected:")
        for port, software, misconfigs in misconfigurations:
            print(f"  Port {port}: {software}")
            for misconfig in misconfigs:
                print(f"    {misconfig}")
    else:
        print("No misconfigurations detected.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Network Port Scanner")
    parser.add_argument("target", type=str, help="Target IP address or domain name")
    parser.add_argument("start_port", type=int, help="Start port number")
    parser.add_argument("end_port", type=int, help="End port number")
    parser.add_argument("--workers", type=int, default=100, help="Number of concurrent threads (default: 100)")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    main(args.target, args.start_port, args.end_port, args.workers, args.verbose)
