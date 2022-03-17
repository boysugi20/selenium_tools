import time
import random
import argparse
import tools.functions as tools

message = """
----------------------------------------------------------------------------------------------------------

Testing selenium and tor proxy

Checklist:
 1. Download chromedriver (change path in this file)
 2. Install tor (sudo apt-get install tor) 
 3. Check tor installation 
    (curl --socks5 localhost:9050 --socks5-hostname localhost:9050 -s https://check.torproject.org/ | cat | grep -m 1 Congratulations | xargs)
 4. Generate hash password (add to tor config) (tor --hash-password Pa55w0rd)
 5. Change tor config (sudo nano /etc/tor/torrc) (ControlPort 9051, CookieAuthentication 1, HashedControlPassword ###)
 6. Restart tor (sudo service tor restart)
 7. Install required libraries

Note:
 1. "Pa55w0rd" is the default pass (configurable in tools > functions.py > renew_connection() )
 2. "9051" is the default port (configurable in tools > functions.py > renew_connection() )

----------------------------------------------------------------------------------------------------------
"""

ap = argparse.ArgumentParser()
ap.add_argument("-ip","--ip_link", type=str, default = 'https://wtfismyip.com/text') 
ap.add_argument("-hl","--headless", type=bool, default = False) 
ap.add_argument("-cd","--chromedriver", type=str, default = '/usr/lib/chromium-browser/chromedriver') 
args = ap.parse_args()

print(message)

ipCheckLink = args.ip_link
chromeDriverPath = args.chromedriver

print('\n[INFO] Starting test...\n')

for i in range(0, 3):

    tools.renew_connection()

    user_agent = tools.get_fake_ua()
    driver, driver_info = tools.get_driver(chromeDriverPath, ipCheckLink, user_agent, headless = args.headless)

    print(driver_info)

    driver.quit()

print('\n[INFO] Testing completed!\n')