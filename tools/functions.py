from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from selenium.common.exceptions import TimeoutException

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains

import stem
import stem.connection
from stem import Signal
from stem.control import Controller

import time

import urllib.request as urllib2

from fake_useragent import UserAgent

#Signal TOR for a new connection 
def renew_connection():
	'''
	Renews tor connection (change IP)
	'''

	with Controller.from_port(port = 9051) as controller:
		controller.authenticate(password = 'Pa55w0rd')
		controller.signal(Signal.NEWNYM)
		time.sleep(controller.get_newnym_wait())

#Generate Service object
def get_chrome_driver_service(path):
	'''
	Returns Service object to be used when creating chrome driver instances.

			Parameters:
					path (str): Path to chromedriver

			Returns:
					Service (obj): object for creating driver instances.
	'''

	service = Service(path)

	return service

        #Generate fake user agent

#Generate fake user agent
def get_fake_ua():
	'''
	Returns random user agent from fake-useragent library

			Returns:
					user_agent (str): random user agent.
	'''

	fake_ua = UserAgent()

	user_agent = fake_ua.random

	return user_agent

#Create a driver instance
def get_driver(chromeDriverPath, ipCheckLink, user_agent, headless = True):
	'''
	Returns chrome driver

			Parameters:
					chromeDriverService (str): Service object
					ipCheckLink (str): URL to check ip Address
					user_agent (obj): user agent
					headless (bool): headless or not

			Returns:
					driver (obj): chrome driver instances
					driver_info (dict): user_agent, ip
	'''

	options = webdriver.ChromeOptions()

	if(headless):
		options.add_argument('--headless')

	options.add_argument('--no-sandbox')
	options.add_argument('--disable-dev-shm-usage')
	options.add_argument('--ignore-certificate-errors')
	options.add_argument('--incognito')
	options.add_argument('--log-level=3')
	options.add_experimental_option('excludeSwitches', ['enable-logging'])

	options.add_argument("user-agent=" + str(user_agent))

	proxy = "socks5://localhost:9050"
	options.add_argument('--proxy-server=%s' % proxy)

	# Try passing service, else pass path
	try:
		driver = webdriver.Chrome(service = get_chrome_driver_service(chromeDriverPath), options = options)
	except Exception:
		driver = webdriver.Chrome(chromeDriverPath, options = options)

	ip = check_ip(ipCheckLink, driver)

	driver_info = {'user_agent': user_agent, 'ip': ip}

	return driver, driver_info

#Check driver IP
def check_ip(ipCheckLink, driver):
	'''
	Returns ip address used by specified driver instance

			Parameters:
					ipCheckLink (str): URL to check ip Address
					driver (obj): Chrome driver

			Returns:
					ip (str): ip address
	'''

	driver.get(ipCheckLink)
	check_ip_html = driver.page_source
	soup = BeautifulSoup(check_ip_html, 'lxml')

	ip = str(soup.find("pre").text)

	ip = ip.strip()

	return ip

#Click button
def click_button(driver, wait_time, xpath):

	button = WebDriverWait(driver, wait_time).until(ec.element_to_be_clickable((By.XPATH, xpath)))
	button.click()

	return

#Click item from dropdown
def click_dropdown_item(driver, wait_time, xpath, index):

	items = driver.find_elements_by_xpath(xpath)
	action = ActionChains(driver)
	action.move_to_element(items[index]).perform()

	return

#Input text
def input_text(driver, wait_time, xpath, text, clear = False):

	text_input = WebDriverWait(driver, wait_time).until(ec.visibility_of_element_located((By.XPATH, xpath)))

	if (clear):
		text_input.send_keys(u'\ue009' + u'\ue003')

	text_input.send_keys(text)

	return

