import webbrowser
import gtk.gdk
import datetime
import time
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

source = 'ORD'
dest = 'DEN'

def populateWeekendDates():
	weekend_dates = []
	start = datetime.datetime.now()
	#3 months into the future
	end =  (start + datetime.timedelta(6*365/12))
	begin = start
	delta = datetime.timedelta(days=1)
	diff = 0
	#ONLY CALCULATE FRIDAY SINCE YOU CAN DO THE MATH FOR SUNDAY..
	weekend = set([3])
	while(begin<=end):
		if(begin.weekday() in weekend):
			weekend_dates.append(begin)
			diff+=1
		begin+=delta
	return weekend_dates

def browserScreenshot(url,start_date,end_date):
	try:
		browser = webdriver.Firefox()
		browser.get(url)
		delay = 1 # seconds
		wait = WebDriverWait(browser, delay)
		wait.until(EC.presence_of_element_located((By.ID, 'root')))
		print "Page is ready!"
		time.sleep(1)
		stringtime = str(start_date) + '->' + str(end_date)
		newdir = "images/" + dest + "/"
		if not os.path.exists(newdir):
			os.makedirs(newdir)
		filename = "images/" + dest + "/flight" + stringtime + ".png"
		browser.save_screenshot(filename)
		print "Saved screenshot here:" + filename
		browser.close()
	except TimeoutException:
		print "Loading took too much time!"


weekend_dates = populateWeekendDates()


def makeCalls(weekend_dates):
	for date in weekend_dates:
		start_date = datetime.datetime.strftime(date,'%Y-%m-%d')
		end_date = datetime.datetime.strftime(date+datetime.timedelta(3),'%Y-%m-%d')
		url = 'https://www.google.com/flights/#search;f='+source+',MDW;t='+dest+';d='+start_date+';r='+end_date+''
		browserScreenshot(url,start_date, end_date)




makeCalls(weekend_dates)


