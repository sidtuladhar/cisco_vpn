# VPN Connection Script

This is a script to automate connecting to the NYU Cisco VPN server.

## Prerequisites

- Install `expect`:
  - macOS: `brew install expect`
  - Ubuntu/Debian: `sudo apt-get install expect`

## Usage

1. Clone this repository:

   ```bash
   git clone https://github.com/sidtuladhar/cisco_vpn.git
   cd cisco_vpn
   ```

2. Open the script (`cisco_connect.exp`) in a text editor and replace:

   - `your_username` with your NYU netid.
   - `your_password` with your password.

3. Make the script executable:

   ```bash
   chmod +x cisco_connect.exp
   ```

4. Run the script every time you want to connect to the VPN

   ```bash
   ./cisco_connect.exp
   ```
