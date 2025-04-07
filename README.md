Cyberbezpieczeństwo Projekt - Narzędzie diagnostyczne sieci

Narzędzie diagnostyczne sieci (Network Diagnostic Tool)
This application provides a graphical interface for various network diagnostic tools, allowing users to monitor WiFi networks, trace network routes, and view active network connections.

Features
WiFi Scanner
Scans and displays available WiFi networks in your area
Shows detailed information including:
SSID (network name)
Channel number
Frequency (2.4 GHz or 5 GHz)
Signal strength (in dBm)
Automatically refreshes every 10 seconds
Supports manual scanning with a button click
Traceroute
Traces the route packets take to a specified network destination
Shows each hop along the network path
Compatible with Windows, Linux, and macOS platforms
Displays results in real-time
Netstat
Displays active network connections on your system
Shows listening ports and established connections
Adapts commands based on your operating system
Outputs detailed network statistics
Requirements
Python 3.x
PyQt5
Operating system support for native network commands:
Windows: netsh, tracert, netstat
Linux: traceroute, netstat or ss
macOS: traceroute, netstat