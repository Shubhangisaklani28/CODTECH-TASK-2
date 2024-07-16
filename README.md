# vulnerability_scan
This Python script scans a specified range of ports on a target IP or domain to identify open ports, outdated software versions, common misconfigurations, and SSL certificate issues. It uses multithreading for efficiency and provides verbose output options. Ideal for basic network security assessments.


### Script Specification

#### Name
Vulnerablity Scanner

#### Description
This Python script scans a specified range of ports on a target IP address or domain name to identify open ports, outdated software versions, common misconfigurations, and SSL certificate issues. It uses multithreading for efficiency and provides verbose output options. The script is ideal for basic network security assessments.

#### Features
1. **Port Scanning**: Identifies open ports within a specified range.
2. **Banner Grabbing**: Retrieves and parses service banners to identify running software and versions.
3. **Outdated Software Detection**: Compares detected software versions against a predefined list of current versions to identify outdated software.
4. **Common Misconfiguration Detection**:
   - **HTTP**: Checks for accessible server-status pages.
   - **FTP**: Checks for anonymous FTP login.
   - **SSH**: Checks for SSH running on default port.
5. **SSL Certificate Inspection**:
   - Checks for expired certificates.
   - Checks for self-signed certificates.
   - Checks for weak encryption algorithms.
6. **Multithreading**: Utilizes concurrent threads for efficient scanning.
7. **Verbose Output**: Provides detailed information about the scanning process and results.

#### Usage
```sh
python port_scanner.py <target> <start_port> <end_port> [--workers <num_workers>] [--verbose]
```

#### Arguments
- `target` (str): Target IP address or domain name.
- `start_port` (int): Start port number.
- `end_port` (int): End port number.
- `--workers` (int, optional): Number of concurrent threads (default: 100).
- `--verbose` (optional): Enable verbose output.

#### Example
```sh
python port_scanner.py example.com 1 1024 --workers 200 --verbose
```

#### Dependencies
- Python 3.x
- `socket` module (standard library)
- `ssl` module (standard library)
- `argparse` module (standard library)
- `concurrent.futures` module (standard library)

#### How to Run
1. Save the script to a file, e.g., `port_scanner.py`.
2. Open a terminal or command prompt.
3. Navigate to the directory where the script is saved.
4. Execute the script with the required arguments.

This script is useful for network administrators and security professionals to perform basic network security assessments, identify potential vulnerabilities, and ensure the security of network services.
