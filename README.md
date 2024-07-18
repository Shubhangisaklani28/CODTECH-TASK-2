Name: Shubhangi Saklani   
Company: CODTECH IT SOLUTIONS   
ID: CT6WDS212   
Domain: Cyber Security and Ethical Hacking   
Duration: June to July 2024    
Mentor:


### Overview of the Project

#### Purpose
This script is designed to scan a specified range of ports on a target IP address or domain name to identify open ports, outdated software versions, common misconfigurations, and SSL certificate issues. It leverages multithreading for efficient scanning and provides detailed feedback when requested.

#### Features
1. **Port Scanning**: Identifies open ports within a specified range.
2. **Banner Grabbing**: Retrieves service banners to identify running software and their versions.
3. **Outdated Software Detection**: Compares detected software versions against a predefined list of current versions.
4. **Common Misconfiguration Detection**:
   - **HTTP**: Checks for accessible server-status pages.
   - **FTP**: Checks for anonymous FTP login.
   - **SSH**: Checks for SSH running on the default port.
5. **SSL Certificate Inspection**:
   - Checks for expired certificates.
   - Checks for self-signed certificates.
   - Checks for weak encryption algorithms.
6. **Multithreading**: Utilizes concurrent threads for efficient scanning.
7. **Verbose Output**: Provides detailed information about the scanning process and results.

#### How It Works
1. **User Input**: Users specify the target, port range, and optional parameters for concurrency and verbosity.
2. **Port Scanning**: The script scans each port in the specified range to check if it's open.
3. **Banner Grabbing**: If a port is open, the script grabs the service banner to identify the running software and its version.
4. **Software Version Check**: It compares the detected software version against a predefined list to identify outdated software.
5. **Misconfiguration Check**: The script checks for common misconfigurations based on the detected software.
6. **SSL Certificate Check**: For SSL ports, it inspects the SSL certificate for common issues.
7. **Output**: Results are printed, including open ports, outdated software, and detected misconfigurations.

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

#### Benefits
- **Comprehensive Scanning**: Identifies open ports, outdated software, misconfigurations, and SSL issues.
- **Efficient**: Utilizes multithreading to scan ports quickly.
- **Detailed Feedback**: Provides comprehensive output with verbose option for in-depth analysis.

This script is ideal for network administrators and security professionals to perform basic network security assessments and ensure the security of network services.






