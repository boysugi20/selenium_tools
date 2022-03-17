
## Installation

1. Download chromedriver
     ```bash
    https://chromedriver.chromium.org/downloads
    ```
2. Install tor
     ```bash
    sudo apt-get install tor
    ```
3. Check tor installation 
    ```bash
    curl --socks5 localhost:9050 --socks5-hostname localhost:9050 -s https://check.torproject.org/ | cat | grep -m 1 Congratulations | xargs
    ```
4. Generate hash password (add to tor config)
     ```bash
    tor --hash-password Pa55w0rd
    ```
5. Change tor config (ControlPort 9051, CookieAuthentication 1, HashedControlPassword ###)
     ```bash
    sudo nano /etc/tor/torrc
    ```
6. Restart tor
     ```bash
    sudo service tor restart
    ```
7. Install required libraries
     ```bash
    pip install -r requirement.txt
    ```

## Configuration

 1. "Pa55w0rd" is the default pass (configurable in tools > functions.py > renew_connection() )
 2. "9051" is the default port (configurable in tools > functions.py > renew_connection() )

## Usage

 1. Run check_installation.py
     ```bash
    python check_installation.py --headless --ip_link 'https://wtfismyip.com/text' --chromedriver '/usr/lib/chromium-browser/chromedriver'
    ```
