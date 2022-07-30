from bs4 import BeautifulSoup
import requests
import time
from time import sleep
from seleniumwire import webdriver as webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium_stealth import stealth
import chromedriver_autoinstaller
import webbrowser
import re
import pandas as pd
from pandas import ExcelWriter
from shutil import which

try:
	keyword = input("Name of companies (Example: Martial arts companies in the United States): ")

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

	
	url = "https://www.google.com/maps/search/" + str(keyword)

	driver.get(url)
	sleep(5)
	
	# Looking for more business
	div_mother = driver.find_element(By.XPATH, '/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]')
	scroll = div_mother.find_elements(By.CLASS_NAME, 'hfpxzc')
	scroll[0].click()

	no_list_business = {}
	list_business = {}
	business_titles = []
	business_web = []
	email_business = []
	business_addresses = []
	no_business_titles = []
	no_business_addresses = []
	no_email_business = []
	
	try:
		for i in range(100):
			print('Business number: ' + str(i))
			
			for n in range(10):
				scroll[0].send_keys(Keys.PAGE_DOWN)

			div_mother = driver.find_element(By.XPATH, '/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]')

			business_total = div_mother.find_elements(By.CLASS_NAME, 'hfpxzc')

			print(str(len(business_total)) + ' business found')

			ignore_titles = 0

			try:
				business_total[i].click()

			except Exception as e:
				print(e)
				sleep(30)
				business_total[i-1].click()
				scroll[0].send_keys(Keys.PAGE_UP)
				business_total[i].click()

			for n in range(50):
				scroll[0].send_keys(Keys.PAGE_DOWN)
			
			

			try:
				business_total[i].click()
				business_drive = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]')

				business_title = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[2]/div[1]/div[1]/div[1]/h1/span[1]').text.strip()

			except:
				try:
					print("Wait 30 seconds...")
					sleep(30)
					business_total[i].click()
					
					business_drive = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]')

					business_title = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[2]/div[1]/div[1]/div[1]/h1/span[1]').text.strip()
				
				except:
					print("Wait 30 seconds more...")
					sleep(30)
					business_total[i].click()
					
					business_drive = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]')

					business_title = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[2]/div[1]/div[1]/div[1]/h1/span[1]').text.strip()

			if business_title in list_business:
				business_title = business_title + " B" 
			
			print(business_title)


			try:
				business_address = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[7]/div[3]/button/div[1]/div[2]/div[1]').text.strip() # Plural a singular

			except:
				business_address = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[9]/div[3]/button/div[1]/div[2]/div[1]').text.strip()
				

			print(business_address)

		#	list_business["Address"] = business_addresses 
			
			business_websites = ""

																		
			try:                                    
				business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[7]/div[4]/div[2]/div/div[1]/a')
				if "places" in business_websites.get_attribute("href"):
					business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/sadsadsad').get_attribute("href")
				else: 
					if "msgsndr.com" in business_websites.get_attribute("href"):
						business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/sadsadsad').get_attribute("href")
					else:
						if "https://www.mindbodyonline.com" in business_websites.get_attribute("href"):
							business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/sadsadsad').get_attribute("href")
						else:
							if "http" in business_websites.get_attribute("href"):
								business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[7]/div[4]/div[2]/div/div[1]/a').get_attribute("href")
			except:
				try:
					business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[7]/div[5]/div[2]/div/div[1]/a')
					if "places" in business_websites.get_attribute("href"):
						business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/sdasdsad').get_attribute("href")
					else:
						if "msgsndr.com" in business_websites.get_attribute("href"):
							business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/sadsadsad').get_attribute("href")
						else:
							if "https://www.mindbodyonline.com" in business_websites.get_attribute("href"):
								business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/sadsadsad').get_attribute("href")
							else:
								if "http" in business_websites.get_attribute("href"):          
									business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[7]/div[5]/div[2]/div/div[1]/a').get_attribute("href")
				except:
					try:
						business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[7]/div[6]/div[2]/div/div[1]/a')
						if "places" in business_websites.get_attribute("href"):
							business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/asdsadsad').get_attribute("href")
						else:
							if "msgsndr.com" in business_websites.get_attribute("href"):
								business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/sadsadsad').get_attribute("href")
							else:
								if "https://www.mindbodyonline.com" in business_websites.get_attribute("href"):
									business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/sadsadsad').get_attribute("href")
								else:
									if "http" in business_websites.get_attribute("href"):
										business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[7]/div[6]/div[2]/div/div[1]/a').get_attribute("href")
					except:
						try:                                       
							business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[7]/div[7]/div[2]/div/div[1]/a')
							if "places" in business_websites.get_attribute("href"):
								business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/asdasdasdsad').get_attribute("href")
							else:
								if "msgsndr.com" in business_websites.get_attribute("href"):
									business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/sadsadsad').get_attribute("href")
								else:
									if "https://www.mindbodyonline.com" in business_websites.get_attribute("href"):
										business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/sadsadsad').get_attribute("href")
									else:
										if "http" in business_websites.get_attribute("href"):
											business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[7]/div[7]/div[2]/div/div[1]/a').get_attribute("href")
						except:
							try:
								business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[7]/div[8]/div[2]/div/div[1]/a')
								if "places" in business_websites.get_attribute("href"):
									business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/adsadasdasd').get_attribute("href")
								else:
									if "msgsndr.com" in business_websites.get_attribute("href"):
										business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/sadsadsad').get_attribute("href")
									else:
										if "https://www.mindbodyonline.com" in business_websites.get_attribute("href"):
											business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/sadsadsad').get_attribute("href")
										else:
											if "http" in business_websites.get_attribute("href"):
												business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[7]/div[8]/div[2]/div/div[1]/a').get_attribute("href")
							except:
								try:
									business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[7]/div[6]/div[2]/div/div[1]/a')
									if "places" in business_websites.get_attribute("href"):
										business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/adsadasdsadasd').get_attribute("href")
									else:
										if "msgsndr.com" in business_websites.get_attribute('href'):
											business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/sadsadsad').get_attribute('href')
										else:
											if "https://www.mindbodyonline.com" in business_websites.get_attribute('href'):
												business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/sdadasdasdadad').get_attribute('href')
											else:
												if "http" in business_websites.get_attribute('href'):
													business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[7]/div[6]/div[2]/div/div[1]/a').get_attribute('href')			
								
								except:
									try:
										business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[9]/div[6]/div[2]/div/div[1]/a')
										if "places" in business_websites.get_attribute("href"):
											business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div[3]/ssdfdsfdfsdf').get_attribute("href")
										else:
											if "msgsndr.com" in business_websites.get_attribute('href'):
												business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div[3]/sdadadasdad').get_attribute("href")
											else:
												if "https://www.mindbodyonline.com" in business_websites.get_attribute("href"):
													business_websites = business_drive.find_element(By.XPATH, '/html/body/div[3]/adadadasd').get_attribute('href')
												else:
													if "http" in business_websites.get_attribute('href'):
														business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[9]/div[6]/div[2]/div/div[1]/a').get_attribute('href')
									except:
										try:
											business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[9]/div[7]/div[2]/div/div[1]/a')
											if "places" in business_websites.get_attribute("href"):
												business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div[3]/ssdfdsfdfsdf').get_attribute("href")
											else:
												if "msgsndr.com" in business_websites.get_attribute('href'):
													business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div[3]/sdadadasdad').get_attribute("href")
												else:
													if "https://www.mindbodyonline.com" in business_websites.get_attribute("href"):
														business_websites = business_drive.find_element(By.XPATH, '/html/body/div[3]/adadadasd').get_attribute('href')
													else:
														if "http" in business_websites.get_attribute('href'):
															business_websites = business_drive.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[9]/div[7]/div[2]/div/div[1]/a').get_attribute('href')

										except Exception as e:
											business_websites = "https://vilmovil.com/"
											print("Error..." + str(e))
											pass

			try: 					
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
						business_titles.append(business_title)
						business_addresses.append(business_address)
					#	list_business["Email"] = email_business
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
							business_titles.append(business_title)
							business_addresses.append(business_address)
						#	list_business["Email"] = email_business 
							break

					if email_count == "":
						no_email_business.append("None")
						no_business_titles.append(business_title)
						no_business_addresses.append(business_address)
					#	list_business["Email"] = email_business
				  

			except:
				
				try:
					for n in range(50):
						scroll[0].send_keys(Keys.PAGE_DOWN)

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
							business_titles.append(business_title)
							business_addresses.append(business_address)
						#	list_business["Email"] = email_business
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
								business_titles.append(business_title)
								business_addresses.append(business_address)
							#	list_business["Email"] = email_business 
								break

						if email_count == "":
							no_email_business.append("None")
							no_business_titles.append(business_title)
							no_business_addresses.append(business_address)
						#	list_business["Email"] = email_business

					
							
				except:
					for n in range(50):
						scroll[0].send_keys(Keys.PAGE_DOWN)

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
							business_titles.append(business_title)
							business_addresses.append(business_address)
						#	list_business["Email"] = email_business
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
								business_titles.append(business_title)
								business_addresses.append(business_address)
							#	list_business["Email"] = email_business 
								break

						if email_count == "":
							no_email_business.append("None")
							no_business_titles.append(business_title)
							no_business_addresses.append(business_address)
						  # list_business["Email"] = email_business

	except:
		pass


	list_business["Name"] = business_titles
	list_business["Address"] = business_addresses
	list_business["Email"] = email_business

	no_list_business["Name"] = no_business_titles
	no_list_business["Address"] = no_business_addresses
	no_list_business["Email"] = no_email_business

	
	list_business = pd.DataFrame(list_business, columns = ['Name', 'Address', 'Email'])
	no_list_business = pd.DataFrame(no_list_business, columns = ['Name', 'Address', 'Email'])

	with ExcelWriter('data('+ str(keyword) +').xlsx') as writer:

		list_business.to_excel(writer, 'Data', index=False)
		no_list_business.to_excel(writer, 'No Email', index=False)

	list_business.to_csv('data('+ str(keyword) +').csv')
	
	input("Ready, press a key")

except Exception as e:
	print(e)