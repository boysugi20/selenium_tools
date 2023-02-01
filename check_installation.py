import argparse
import functions as tools

message = """
----------------------------------------------------------------------------------------------------------

Testing selenium and proxy

TOR Checklist:
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
 3. Proxy list in ip:port:username:pass format and seperated 1 per line (proxy list.txt)

----------------------------------------------------------------------------------------------------------
"""

ap = argparse.ArgumentParser()
ap.add_argument("-hl","--headless", type=bool, default = True) 
ap.add_argument("-cd","--chromedriver", type=str, default = '/usr/lib/chromium-browser/chromedriver') 
args = ap.parse_args()

print(message)

chromeDriverPath = args.chromedriver

# List of proxy (format ip:port:username:pass) [line seperated]
with open("proxy list.txt") as file:
    proxy = [line.rstrip() for line in file]

print('\n[INFO] Starting selenium test...\n')

try:

    for i in range(0, 3):

        driver, driver_info = tools.get_driver(chromeDriverPath, headless = args.headless)

        print(driver_info)

        tools.driver_quit(driver)

except Exception as e:
    print(e)

print('\n\n[INFO] Starting TOR test...\n')

try:
    for i in range(0, 3):

        tools.renew_connection()

        user_agent = tools.get_fake_ua()
        driver, driver_info = tools.get_driver(chromeDriverPath, True, user_agent, headless = args.headless)

        print(driver_info)

        tools.driver_quit(driver)
except Exception as e:
    print(e)

print('\n\n[INFO] Starting proxy test...\n')

try:

    for i in range(0, 3):

        proxy_obj = tools.Proxy(proxy)
        proxy_url = proxy_obj.get_free_proxy()
        proxy_obj.set_proxy_busy(proxy_url)

        user_agent = tools.get_fake_ua()
        driver, driver_info = tools.get_driver(chromeDriverPath, True, user_agent, proxy=proxy_url, headless = args.headless)

        print(driver_info)

        tools.driver_quit(driver)
except Exception as e:
    print(e)

print('\n[INFO] Testing completed!\n')