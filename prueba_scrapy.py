from bs4 import BeautifulSoup
import requests
import time
from time import sleep
from seleniumwire import webdriver as webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium_stealth import stealth
import chromedriver_autoinstaller
import webbrowser
import re
import pandas as pd
from shutil import which

try:
	chromedriver_autoinstaller.install()
	options = webdriver.ChromeOptions()
	options.add_argument('--headless')
	options.add_argument('--log-level=3')
	options.add_argument('--window-size=1920,1080')
	options.add_argument('--disable-dev-shm-usage')
	options.add_argument('--start-maximized')
	options.add_argument('--disable-blink-features=AutomationControlled')
	lista = ['enable-automation', 'enable-logging']
	options.add_experimental_option('excludeSwitches', lista)

	s = Service(which("chromedriver"))

	driver = webdriver.Chrome(executable_path = 'chromedriver', options=options)

	

	stealth(
		driver,
		languages=["us-US", "us"],
		vendor="Google Inc.",
		platform="Win32",
		webgl_vendor="Intel Inc.",
		renderer = "Intel Iris OpenGL Engine",
		fix_hairline=True,
		)



	# Create a request interceptor
	def interceptor(request):
		del request.headers['Referer']  # Delete the header first
		request.headers['Referer'] = 'some_referer'

	driver.request_interceptor = interceptor

	keyword = "Martial Arts studios united states"
	url = "https://www.google.com/maps/search/" + str(keyword)

	driver.get(url)
	sleep(5)
	# Looking for more business
	div_mother = driver.find_element(By.XPATH, '/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]')
	scroll = div_mother.find_elements(By.CLASS_NAME, 'hfpxzc')
	scroll[0].click()
	for j in range(4):
		for i in range(200):
			scroll[0].send_keys(Keys.DOWN)
		sleep(2)
		

	div_mother = driver.find_element(By.XPATH, '/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]')
	sleep(10)

	print("1")

	business_total = div_mother.find_elements(By.CLASS_NAME, 'hfpxzc')

	print(str(len(business_total)) + ' Encontrados')
	print("2")

	# business_websites = driver.find_elements(By.CLASS_NAME, 'yYlJEf.Q7PwXb.L48Cpd')

	# business_titles_web = driver.find_elements(By.CLASS_NAME, 'dbg0pd.eDIkBe')

	list_business = {}
	business_titles = []
	business_web = []
	email_business = []
	business_addresses = []

	ignore_titles = 0

	for business in business_total:

		business.click()
		sleep(15)
		
		business_drive = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]')

		business_title = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[2]/div[1]/div[1]/div[1]/h1/span[1]').text.strip()

	#	if len(business_title) == 0:
		#	business_title = business.find_element(By.CLASS_NAME, 'rgnuSb.xYjf2e').text.strip()

		if business_title in list_business:
			business_title = business_title + " B" 

		print(business_title)

		business_titles.append(business_title)

		list_business["Name"] = business_titles

		business_address = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[7]/div[3]/button/div[1]/div[2]/div[1]').text.strip() # Plural a singular

	#	if len(business_address) == 0:
	#		business_address = business.find_element(By.CLASS_NAME, 'deyx8d').click()
	#		sleep(10)
	#		business_address = driver.find_element(By.CLASS_NAME, ' wV5uyc')
	#		business_address = business_address.find_element(By.CLASS_NAME, 'fccl3c').text.strip()
			
	#	else:
	#		business_address = business.find_element(By.CLASS_NAME, 'cXedhc').click()
	#		sleep(10)
	#		business_address = driver.find_element(By.CLASS_NAME, 't3HED')
	#		business_address = business_address.find_element(By.CLASS_NAME, 'LrzXr').text.strip()

		business_addresses.append(business_address)

		print(business_address)

		list_business["Address"] = business_addresses 
		
		business_websites = ""
																	
		try:
			print("Primer intento")                                    
			business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[7]/div[4]/div[2]/div/div[1]/a')
			if "places" in business_websites.get_attribute("href"):
				business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/sadsadsad').get_attribute("href")
			else: 
				if "msgsndr.com" in business_websites.get_attribute("href"):
					business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/sadsadsad').get_attribute("href")
				else:
					if "http" in business_websites.get_attribute("href"):
						business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[7]/div[4]/div[2]/div/div[1]/a').get_attribute("href")
		except:
			try:
				print("Segundo intento")
				business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[7]/div[5]/div[2]/div/div[1]/a')
				if "places" in business_websites.get_attribute("href"):
					business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/sdasdsad').get_attribute("href")
				else:
					if "msgsndr.com" in business_websites.get_attribute("href"):
						business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/sadsadsad').get_attribute("href")
					else:
						if "http" in business_websites.get_attribute("href"):
							business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[7]/div[5]/div[2]/div/div[1]/a').get_attribute("href")
			except:
				try:
					print("Error...")
					print("Tercer intento")
					business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[7]/div[6]/div[2]/div/div[1]/a')
					if "places" in business_websites.get_attribute("href"):
						business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/asdsadsad').get_attribute("href")
					else:
						if "msgsndr.com" in business_websites.get_attribute("href"):
							business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/sadsadsad').get_attribute("href")
						else:
							if "http" in business_websites.get_attribute("href"):
								business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[7]/div[6]/div[2]/div/div[1]/a').get_attribute("href")
				except:
					try:
						print("Error...")
						print("Cuarto intento")                                           
						business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[7]/div[7]/div[2]/div/div[1]/a')
						if "places" in business_websites.get_attribute("href"):
							business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/asdasdasdsad').get_attribute("href")
						else:
							if "msgsndr.com" in business_websites.get_attribute("href"):
								business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/sadsadsad').get_attribute("href")
							else:
								if "http" in business_websites.get_attribute("href"):
									business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[7]/div[7]/div[2]/div/div[1]/a').get_attribute("href")
					except:
						try:
							print("Error...")
							print("Quinto intento")
							business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[7]/div[8]/div[2]/div/div[1]/a')
							if "places" in business_websites.get_attribute("href"):
								business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/adsadasdasd').get_attribute("href")
							else:
								if "msgsndr.com" in business_websites.get_attribute("href"):
									business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/sadsadsad').get_attribute("href")
								else:
									if "http" in business_websites.get_attribute("href"):
										business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[7]/div[8]/div[2]/div/div[1]/a').get_attribute("href")
						except Exception as e:
							print("Error...." + str(e))	

	#	if len(business_websites) == 0:
	#		business_websites = driver.find_element(By.CLASS_NAME, ' wV5uyc')
	#		business_websites = business.find_element(By.CLASS_NAME, 'VfPpkd-dgl2Hf-ppHlrf-sM5MNb').get_attribute("href")
	#	else:
	#		business_websites = business.find_element(By.CLASS_NAME, 'yYlJEf.Q7PwXb.L48Cpd').get_attribute("href")

		headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36', 'referer':'https://google.es',}

		
		req = requests.get(business_websites, headers=headers, timeout=10)
		
		sleep(5)

		soup = BeautifulSoup(req.text, "html.parser")
											
		emails = soup.find_all('div')
		
		email_count = ""

		print("Searching..." + str(business_websites))
		
		for email in emails:
			email = email.text.strip()
			email = re.findall(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}', email)

			if email:
				email_count = email
				email_business.append(email[0])
				list_business["Email"] = email_business
				break

		if email_count == "":
	
			print("Searching in contact page")
			business_websites = business_websites + "contact"

			req = requests.get(business_websites, headers=headers, timeout=10)

			sleep(5)

			soup = BeautifulSoup(req.text, "html.parser")
													
			emails = soup.find_all('div')

			for email in emails:
				email = email.text.strip()
				email = re.findall(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}', email)

				if email:
					email_count = email
					email_business.append(email[0])
					list_business["Email"] = email_business 
					break

			if email_count == "":
				email_business.append("None")
				list_business["Email"] = email_business 
		
		

	print(list_business)
	business = pd.DataFrame(list_business, columns = ['Name', 'Address', 'Email'])
	business.to_csv('data.csv')
	business.to_excel('data.xlsx', sheet_name='data')
	
	print(4)
	
	input("Ready, press a key")

except Exception as e:
	print(e)