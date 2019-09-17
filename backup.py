
Gaurang <govishwasrao99@gmail.com>
11:20 AM (2 hours ago)
to me

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
#atm_list=[]
#atm_itm_list=[]

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
'https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?segmentLink=17&instrument=OPTIDX&symbol=NIFTY&date=26SEP2019',
'https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?segmentLink=17&instrument=OPTIDX&symbol=BANKNIFTY&date=26SEP2019'
]
#Stocks currently being monitored
stocknamelist=['SBIN','RELIANCE','TCS','HDFC','HDFCBANK','MARUTI','BAJAJFINSV',
'ICICIBANK','AXISBANK','INDUSINDBK','FEDERALBNK','WIPRO','TECHM','HCLTECH','INFY','ITC','VEDL','TATASTEEL','ZEEL']
#Indices being monitored
index_name_list=['NIFTY','BANKNIFTY']

aggeregated_list_stock_index=['SBIN','RELIANCE','TCS','HDFC','HDFCBANK','MARUTI','BAJAJFINSV',
'ICICIBANK','AXISBANK','INDUSINDBK','FEDERALBNK','WIPRO','TECHM','HCLTECH','INFY','ITC','VEDL',
'TATASTEEL','ZEEL','NIFTY','BANKNIFTY']


def scraperlist15mins():
	global list_scraper_outp15mins
	list_scraper_outp15mins=[]
	
	o=0
	for i in range(len(scraping_list)):
		
		while (o < len(namelist)):
			
			respon=requests.get(scraping_list[i],timeout=10)
			soupe=bs4.BeautifulSoup(respon.text,'lxml')
			for j in range(o,o+10):
				try:
					result = soupe.find_all('a', attrs={'href': re.compile(namelist[j])})
					
					#Make OI list over here
					list_scraper_outp15mins.append(float(str(result[0]).split('target="_blank">')[1].split('<')[0]))
				except:
					list_scraper_outp15mins.append('None')
					continue

			o+=10
			break
			
def scraperlisthourly():
	global list_scraper_outp_hourly
	list_scraper_outp_hourly=[]
	
	o=0
	for i in range(len(scraping_list)):
		
		while (o < len(namelist)):
			
			respon=requests.get(scraping_list[i],timeout=10)
			soupe=bs4.BeautifulSoup(respon.text,'lxml')
			for j in range(o,o+10):
				try:
					result = soupe.find_all('a', attrs={'href': re.compile(namelist[j])})
					
					#Make OI list over here hourly calculation
					list_scraper_outp_hourly.append(float(str(result[0]).split('target="_blank">')[1].split('<')[0]))
				except:
					list_scraper_outp_hourly.append('None')
					continue

			o+=10
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
			list2.append(format(u[j+4],'.2f'))
			list2.append(format(u[j-4],'.2f'))
	return sorted(list2)

	
#Calculation for option pivots levels for index same as above
def optionpricefinderindex(stockname):
	list1=[]
	list2=[]
	list3=[]
	#global atm_list
	#global atm_itm_list
	stocklist='https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?symbolCode=238&symbol={}&symbol={}&instrument=OPTIDX&date=-&segmentLink=17&segmentLink=17'.format(stockname,stockname)
	

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
			list2.append(format(u[j+4],'.2f'))
			list2.append(format(u[j-4],'.2f'))
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
			stocklist.append('https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/getFOHistoricalData.jsp?underlying={}&instrument=OPTSTK&expiry=26SEP2019&type=CE&strike={}&fromDate=undefined&toDate=undefined&datePeriod=3months'.format(i,d[o]))
			namelist.append('{}&instrument=OPTSTK&strike={}&type=CE'.format(i,d[o]))
			namelist.append('{}&instrument=OPTSTK&strike={}&type=PE'.format(i,d[o]))
			stocklist.append('https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/getFOHistoricalData.jsp?underlying={}&instrument=OPTSTK&expiry=26SEP2019&type=PE&strike={}&fromDate=undefined&toDate=undefined&datePeriod=3months'.format(i,d[o]))
				
	for i in index_name_list:
		print(i)	
		d=optionpricefinderindex(i)			
		print(d)
		for o in range(len(d)):		
			stocklist.append('https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/getFOHistoricalData.jsp?underlying={}&instrument=OPTIDX&expiry=26SEP2019&type=CE&strike={}&fromDate=undefined&toDate=undefined&datePeriod=3months'.format(i,d[o]))
			namelist.append('{}&instrument=OPTIDX&strike={}&type=CE'.format(i,d[o]))
			namelist.append('{}&instrument=OPTIDX&strike={}&type=PE'.format(i,d[o]))
			stocklist.append('https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/getFOHistoricalData.jsp?underlying={}&instrument=OPTIDX&expiry=26SEP2019&type=PE&strike={}&fromDate=undefined&toDate=undefined&datePeriod=3months'.format(i,d[o]))					
		print(namelist)
		print(stocklist)


stringmaker(stocknamelist,index_name_list)

#Initilizing the notifier class
notifier = SlackNotifier("https://hooks.slack.com/services/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")
def comaparator(temp_list,main_list):
	global difflist
	difflist=[]
	for i in range(len(temp_list)):
		difflist.append(abs((main_list[i]-temp_list[i])/main_list[i]))

while True:
	try:
		with open('open_intrest.txt','a') as fd:
			minutes_now=datetime.now().minute
			if(minutes_now % 15 == 0):
				temp_list_scraper_outp15mins=list_scraper_outp15mins
				scraperlist15mins()
				comaparator(temp_list_scraper_outp15mins,list_scraper_outp15mins)
			if(minutes_now % 60 == 0):
				temp_list_scraper_outp_hourly=list_scraper_outp_hourly
				scraperlisthourly()
				comaparator(temp_list_scraper_outp_hourly,list_scraper_outp_hourly)



			scraperlist()

			fd.write("\n")
			fd.write(str(datetime.now()))


	except:
		continue
