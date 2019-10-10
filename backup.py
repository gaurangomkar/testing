import requests
import bs4
import time
import pandas as pd
import re
from datetime import datetime,timedelta,date
from dateutil.relativedelta import relativedelta
from notetifications.slack_notification import SlackNotifier
import time
import math
import copy

list_scraper_outp=[]
stocklist=[]
list_scraper_outp15mins=[]
list_scraper_outp_hourly=[]
namelist=[]
difflist=[]

#List of stocks to scrape the data from
scraping_list=['https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?symbolCode=238&symbol=SBIN&symbol=sbin&instrument=OPTSTK&date=-&segmentLink=17&segmentLink=17',
'https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?symbolCode=242&symbol=RELIANCE&symbol=reliance&instrument=OPTSTK&date=-&segmentLink=17&segmentLink=17',
'https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?symbolCode=2212&symbol=TCS&symbol=tcs&instrument=OPTSTK&date=-&segmentLink=17&segmentLink=17',
'https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?symbolCode=798&symbol=HDFC&symbol=hdfc&instrument=OPTSTK&date=-&segmentLink=17&segmentLink=17',
'https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?symbolCode=797&symbol=HDFCBANK&symbol=hdfcbank&instrument=OPTSTK&date=-&segmentLink=17&segmentLink=17',
'https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?symbolCode=2143&symbol=MARUTI&symbol=maruti&instrument=OPTSTK&date=-&segmentLink=17&segmentLink=17',
'https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?symbolCode=2749&symbol=BAJAJFINSV&symbol=BAJAJFINSV&instrument=OPTSTK&date=-&segmentLink=17&segmentLink=17',
'https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?symbolCode=1606&symbol=ICICIBANK&symbol=ICICIBANK&instrument=OPTSTK&date=-&segmentLink=17&segmentLink=17',
'https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?symbolCode=1693&symbol=AXISBANK&symbol=axis%20bank&instrument=OPTSTK&date=-&segmentLink=17&segmentLink=17',
'https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?symbolCode=1656&symbol=INDUSINDBK&symbol=INDUSINDBK&instrument=OPTSTK&date=-&segmentLink=17&segmentLink=17',
'https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?symbolCode=309&symbol=FEDERALBNK&symbol=FEDERALBNK&instrument=OPTSTK&date=-&segmentLink=17&segmentLink=17',
'https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?symbolCode=624&symbol=WIPRO&symbol=WIPRO&instrument=OPTSTK&date=-&segmentLink=17&segmentLink=17',
'https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?symbolCode=2421&symbol=TECHM&symbol=TECHM&instrument=OPTSTK&date=-&segmentLink=17&segmentLink=17',
'https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?symbolCode=1828&symbol=HCLTECH&symbol=HCLTECH&instrument=OPTSTK&date=-&segmentLink=17&segmentLink=17',
'https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?symbolCode=180&symbol=INFY&symbol=INFY&instrument=OPTSTK&date=-&segmentLink=17&segmentLink=17',
'https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?symbolCode=818&symbol=ITC&symbol=ITC&instrument=OPTSTK&date=-&segmentLink=17&segmentLink=17',
'https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?symbolCode=237&symbol=VEDL&symbol=VEDL&instrument=OPTSTK&date=-&segmentLink=17&segmentLink=17',
'https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?symbolCode=234&symbol=TATASTEEL&symbol=tatasteel&instrument=OPTSTK&date=-&segmentLink=17&segmentLink=17',
'https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?symbolCode=1105&symbol=ZEEL&symbol=zee&instrument=OPTSTK&date=-&segmentLink=17&segmentLink=17',
'https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?segmentLink=17&instrument=OPTIDX&symbol=NIFTY&date=31OCT2019',
'https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?segmentLink=17&instrument=OPTIDX&symbol=BANKNIFTY&date=31OCT2019'
]
#Stocks currently being monitored
stocknamelist=['SBIN','RELIANCE','TCS','HDFC','HDFCBANK','MARUTI','BAJAJFINSV',
'ICICIBANK','AXISBANK','INDUSINDBK','FEDERALBNK','WIPRO','TECHM','HCLTECH','INFY','ITC','VEDL','TATASTEEL','ZEEL']
#Indices being monitored
index_name_list=['NIFTY','BANKNIFTY']

aggeregated_list_stock_index=['SBIN','RELIANCE','TCS','HDFC','HDFCBANK','MARUTI','BAJAJFINSV',
'ICICIBANK','AXISBANK','INDUSINDBK','FEDERALBNK','WIPRO','TECHM','HCLTECH','INFY','ITC','VEDL',
'TATASTEEL','ZEEL','NIFTY','BANKNIFTY']

#Scrape the live values of OI every 15mins
def scraperlist15mins():
	global list_scraper_outp15mins
	list_scraper_outp15mins=[]	
	o=0
	for i in range(len(scraping_list)):		
		while (o < len(namelist)):
			flag=True
			while flag:
				try:
					respon=requests.get(scraping_list[i],timeout=10)
				except:
					continue
				if (respon.status_code != 200):
					print("Bad Request")
					continue
				if(len(respon.text)  <= 1):
					print("Size Exception")	
					continue				
				flag=False
			
			soupe=bs4.BeautifulSoup(respon.text,'lxml')
			col = soupe.find_all('tr')
			for j in range(o,o+14):
				try:					
					print(namelist[j])
					for result in col:
						flag=False
						a=(str(result).split("\n"))
						for op in range(len(a)):
							if str(namelist[j]) in str(a[op]):							
								if namelist[j].endswith("PE"):
									open_intrest_pe=a[op+7].split(">")[1].split("<")[0].strip(" ").replace(",","")
									if(open_intrest_pe.isnumeric()):
										list_scraper_outp15mins.append(open_intrest_pe)
										flag=True				
									else:
										list_scraper_outp15mins.append("None")
										flag=True
								else:
									open_intrest_ce=a[op-7].split(">")[1].split("<")[0].strip(" ").replace(",","")
									if(open_intrest_ce.isnumeric()):
										list_scraper_outp15mins.append(open_intrest_ce)
										flag=True									
									else:
										list_scraper_outp15mins.append("None")
										flag=True
					else:
						if(flag==False):
							list_scraper_outp15mins.append("None")


										
																									
				except Exception as e:
					print(e)
					list_scraper_outp15mins.append('None')
					continue

			o+=14
			break


#Scrape the live valuses of OI every hour 		
def scraperlisthourly():
	global list_scraper_outp_hourly
	list_scraper_outp_hourly=[]
	o=0
	for i in range(len(scraping_list)):	
		while (o < len(namelist)):
			while flag:
				try:
					respon=requests.get(scraping_list[i],timeout=10)
				except:
					continue
				if (respon.status_code != 200):
					print("Bad Request")
					continue
				if(len(respon.text)  <= 1):
					print("Size Exception")
					continue				
				flag=False
						
			soupe=bs4.BeautifulSoup(respon.text,'lxml')
			col = soupe.find_all('tr')
			#print(len(col))
			for j in range(o,o+14):
				try:					
					print(namelist[j])
					for result in col:
						flag=False
						a=(str(result).split("\n"))
						for op in range(len(a)):
							if str(namelist[j]) in str(a[op]):							
								if namelist[j].endswith("PE"):
									open_intrest_pe=a[op+7].split(">")[1].split("<")[0].strip(" ").replace(",","")
									if(open_intrest_pe.isnumeric()):
										list_scraper_outp_hourly.append(open_intrest_pe)
										flag=True							
									else:										
										list_scraper_outp_hourly.append("None")
										flag=True	
								else:
									open_intrest_ce=a[op-7].split(">")[1].split("<")[0].strip(" ").replace(",","")
									if(open_intrest_ce.isnumeric()):										
										list_scraper_outp_hourly.append(open_intrest_ce)
										flag=True										
									else:										
										list_scraper_outp_hourly.append("None")
										flag=True

						else:
							if(flag==False):
								list_scraper_outp_hourly.append("None")

				except Exception as e:
					print(e)
					list_scraper_outp_hourly.append('None')
					continue

			o+=14
			break


#Calculating all the option pivot levels for stock from the medium
def optionpricefinder(stockname):
	list1=[]
	list2=[]
	list3=[]
	#global atm_list
	#global atm_itm_list
	stocklist='https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?symbolCode=238&symbol={}&symbol={}&instrument=OPTSTK&date=-&segmentLink=17&segmentLink=17'.format(stockname,stockname)
	
	print(stocklist)
	flag=True
	while flag:
		try:			
			respon=requests.get(stocklist,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'},timeout=20)
		except:
			print("Time-out")
			continue
		if (respon.status_code != 200):
			continue
			print("Bad Request")
		if(len(respon.text)  <= 1):
			print("Size Exception")				
			continue			
		flag=False

	soupe=bs4.BeautifulSoup(respon.text,'lxml')
	result = soupe.find_all('a', attrs={'href': re.compile("javascript:chartPopup")})
	result1 = soupe.find_all('b', attrs={'style': re.compile("font-size:1.2em")})
	x=str(result1[0]).split(" ")
	curent_price=float((x[2][:-4]))
	for i in range(len(result)):
		a=str((result[i])).split(",")[3].strip(" '")
		(list1.append(float(a)))
	u=(sorted(list(set(list1))))
	
	for i in u:
		list3.append((((i-curent_price))))
	
	#to select all the strike prices
	for j in range(len(list3)-1):
	
		if(list3[j] <= 0 and list3[j+1] > 0):
			list2.append(format(u[j],'.2f'))
			list2.append(format(u[j+1],'.2f'))
			list2.append(format(u[j-1],'.2f'))
			list2.append(format(u[j+2],'.2f'))
			list2.append(format(u[j-2],'.2f'))
			list2.append(format(u[j+3],'.2f'))
			list2.append(format(u[j-3],'.2f'))
	return sorted(list2)
	
#Calculation for option pivots levels for index same as above
def optionpricefinderindex(stockname):
	list1=[]
	list2=[]
	list3=[]
	stocklist='https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?symbolCode=238&symbol={}&symbol={}&instrument=OPTIDX&date=31OCT2019&segmentLink=17&segmentLink=17'.format(stockname,stockname)
	
	flag=True
	while flag:
		try:
			respon=requests.get(stocklist,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'},timeout=20)
		except:
			continue	
		if (respon.status_code != 200):
			print("Bad Request")
			continue
		if(len(respon.text)  <= 1):
			print("Size Exception")				
			continue
		flag=False
				
	soupe=bs4.BeautifulSoup(respon.text,'lxml')
	result = soupe.find_all('a', attrs={'href': re.compile("javascript:chartPopup")})
	result1 = soupe.find_all('b', attrs={'style': re.compile("font-size:1.2em")})
	x=str(result1[0]).split(" ")
	curent_price=float((x[2][:-4]))
	for i in range(len(result)):
		a=str((result[i])).split(",")[3].strip(" '")
		(list1.append(float(a)))
	u=(sorted(list(set(list1))))

	for i in u:
		list3.append(((i-curent_price)))
	
	#to select strike prices
	for j in range(len(list3)-1):
		if(list3[j] <= 0 and list3[j+1] > 0):
			list2.append(format(u[j],'.2f'))
			list2.append(format(u[j+1],'.2f'))
			list2.append(format(u[j-1],'.2f'))
			list2.append(format(u[j+2],'.2f'))
			list2.append(format(u[j-2],'.2f'))
			list2.append(format(u[j+3],'.2f'))
			list2.append(format(u[j-3],'.2f'))
	return sorted(list2)
	
#optionpricefinder("WIPRO")
#Making all the string to hit in order to fetch all the data
def stringmaker(stocknamelist,index_name_list):
	global stocklist
	global namelist
	stocklist=[]
	namelist=[]	
	for i in stocknamelist:		
		d=optionpricefinder(i)				
		print(d)
		for o in range(len(d)):		
			stocklist.append('https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/getFOHistoricalData.jsp?underlying={}&instrument=OPTSTK&expiry=31OCT2019&type=CE&strike={}&fromDate=undefined&toDate=undefined&datePeriod=3months'.format(i,d[o]))
			namelist.append('{}&amp;instrument=OPTSTK&amp;strike={}&amp;type=CE'.format(i,d[o]))
			namelist.append('{}&amp;instrument=OPTSTK&amp;strike={}&amp;type=PE'.format(i,d[o]))
			stocklist.append('https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/getFOHistoricalData.jsp?underlying={}&instrument=OPTSTK&expiry=31OCT2019&type=PE&strike={}&fromDate=undefined&toDate=undefined&datePeriod=3months'.format(i,d[o]))
				
	for i in index_name_list:
		print(i)	
		d=optionpricefinderindex(i)			
		print(d)
		for o in range(len(d)):		
			stocklist.append('https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/getFOHistoricalData.jsp?underlying={}&instrument=OPTIDX&expiry=31OCT2019&type=CE&strike={}&fromDate=undefined&toDate=undefined&datePeriod=3months'.format(i,d[o]))
			namelist.append('{}&amp;instrument=OPTIDX&amp;strike={}&amp;type=CE'.format(i,d[o]))
			namelist.append('{}&amp;instrument=OPTIDX&amp;strike={}&amp;type=PE'.format(i,d[o]))
			stocklist.append('https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/getFOHistoricalData.jsp?underlying={}&instrument=OPTIDX&expiry=31OCT2019&type=PE&strike={}&fromDate=undefined&toDate=undefined&datePeriod=3months'.format(i,d[o]))					
		print(namelist)
		print(stocklist)

stringmaker(stocknamelist,index_name_list)

#Initilizing the notifier class
notifier = SlackNotifier("https://hooks.slack.com/services/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")

#Comapares the activity in last 15min and hour
def comaparator(temp_list,main_list):
	global difflist
	difflist=[]
	for i in range(len(temp_list)):
		if ((main_list[i]) != 'None') and ((temp_list[i]) != 'None'):
			difflist.append(str(abs((int(main_list[i])-int(temp_list[i]))/int(main_list[i])))+(namelist[i]))
	return sorted(difflist)

while True:
	try:
		with open('open_intrest.txt','a') as fd:
			minutes_now=datetime.now().minute
			if(minutes_now % 15 == 0):
				op=[]
				fd.write(str(datetime.now()))
				fd.write("15mins")
				fd.write("\n")
				temp_list_scraper_outp15mins=list_scraper_outp15mins
				print(temp_list_scraper_outp15mins)
				print("!!!!!!!!!!!")
				scraperlist15mins()
				print(len(temp_list_scraper_outp15mins))
				time.sleep(5)
				if(len(temp_list_scraper_outp15mins) > 0):
					op=comaparator(temp_list_scraper_outp15mins,list_scraper_outp15mins)
					notifier.notify("15 min ::")
					notifier.notify(str(op[-20:]))
					fd.write(str(op))
			if(minutes_now % 60 == 0):
				op=[]
				fd.write(str(datetime.now()))
				fd.write("60mins")
				fd.write("\n")
				temp_list_scraper_outp_hourly=list_scraper_outp_hourly
				scraperlisthourly()
				if (len(temp_list_scraper_outp_hourly) != 0):
					op=comaparator(temp_list_scraper_outp_hourly,list_scraper_outp_hourly)
					notifier.notify("hourly")
					notifier.notify(str(op[-20:]))
					print(op)
					fd.write(str(op))
			time.sleep(50)
	
	except:
		continue
