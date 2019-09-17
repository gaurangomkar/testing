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
list_daily_pivots_std1=[]
list_daily_pivots_std_updater=[]
stocklist=[]
closingprice_list=[]
currentprice_list=[]
namelist=[]
atm_list=[]
atm_itm_list=[]

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

#Function to calcuate current price of stocks
def currentprice():
	global currentprice_list
	currentprice_list=[]
	for stock in scraping_list:		
	#Below while loop ensures that no request is bad withot any exception
		flag=True
		while flag:
			try:
				respon=requests.get(stock,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'},timeout=20)
			except:
				continue
			#if the request we get is bad then request again  	
			if (respon.status_code != 200):
				continue
			#if there is a empty text string  then request again
			if(len(respon.text)  <= 1):
				continue
			flag=False
		soupe=bs4.BeautifulSoup(respon.text,'lxml')
		result_current_price = soupe.find_all('b', attrs={'style': re.compile("font-size:1.2em")})
		x=str(result_current_price[0]).split(" ")
		curent_price=float((x[2][:-4]))
		currentprice_list.append(float(curent_price))
	print(currentprice_list)
	




#This function is used to calculate the atm call.
def myround(x, base):
   
    return format((base *((math.floor(float(x)/base)))),'.1f')
  
#This is the main updater function which returns the stocks to be updated
def stockupdater():
	returnlist=[]
	global atm_list
	global atm_itm_list
	global atm_update_list
	global atm_itm_update_list
	print(atm_update_list)
	print(atm_itm_update_list)
	for i in range(len(aggeregated_list_stock_index)):

		x=myround(currentprice_list[i],atm_itm_update_list[i])
		if(float(x) != float(atm_update_list[i])):
			atm_update_list[i]=float(x)
			returnlist.append(aggeregated_list_stock_index[i])


	print(atm_update_list)
	print(returnlist)
	return returnlist
	




#Function to calculate Pivot levels of Stocks
def optionpivots():
	# to calculate todays date
	x=datetime.now()
	# to calculate last months last date
	lastmonthlast=(x-timedelta(days=x.day))
	#to calculate last month first date
	d= lastmonthlast - relativedelta(months=1)+relativedelta(days=1)
	print(len(stocklist))
	#to itreate through all the stocks made by stringmaker function
	for i in stocklist:

		datelist=[]
		openlist=[]
		highlist=[]
		lowlist=[]
		closelist=[]
		
		flag=True
		print(i)
		while flag:
			try:
				respon=requests.get(i,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'},timeout=20)
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
		string=str(soupe).split('\n')
		#Making a Dataframe 
		try:
			for j in range(1,len(string)-1):
				O=(datetime.strptime(string[j].split('<td>')[1][:-5], '%d-%b-%Y'))
				print(O)
				#Date logic
				u=str(O.strftime('%d-%m-%Y'))
				datelist.append(datetime.strptime(u,('%d-%m-%Y')))
				openlist.append(float(string[j].split('<td>')[2][:-5]))
				highlist.append(float(string[j].split('<td>')[3][:-5]))
				lowlist.append(float(string[j].split('<td>')[4][:-5]))
				closelist.append(float(string[j].split('<td>')[5][:-5]))
			dicto=pd.DataFrame({'date': datelist,'close':closelist,'high':highlist,'open':openlist,'low':lowlist})
			k=dicto.set_index('date')
		except:
			
			dicto=pd.DataFrame({'date':['00-00-0000'],'close':[0.0],'high':[0.0],'low':[0.0],'open': [0.0]})
			k=dicto.set_index('date')
			
		global list_daily_pivots_std1
		if(len(k) > 6):
			temp_list=[]
			a=[]
			max_high=[]
			a=(k.loc[str(lastmonthlast):str(d)])

			max_high.append((a['high'].max()))
			max_high.append((a['low'].max()))
			max_high.append((a['close'].max()))
			high=max(max_high)
			min_low=[]
			#print(a)
			#print(len(k))
			low=float(a.groupby('low').first().iloc[:1].index.values[0])

			#if low is 0.0 then we consider second low
			close=(a.head(1)['close'].values[0])
			if(low==0.0 and len(a) != 1):
				second_low=(a.groupby('low').first())
				if((len(second_low) == 1)):
					low=0.0
					high=0.0
					close=0.0
				else:
					second_low=float(second_low.iloc[1:2].index.values[0])
					min_low.append(second_low)
					min_low.append(a['close'].min())
					low=min(min_low)

			#calculating fibonacci and standard pivots
			pivot_point=round(((high+low+close)/3.0),2)
			r1=(2*pivot_point)-low
			s1=round(((2*pivot_point)-high),2)
			r2=round((pivot_point+(high-low)),2)
			s2=round((pivot_point-(high-low)),2)
			r3=round((pivot_point+2*(high-low)),2)
			s3=round((pivot_point-2*(high-low)),2)
			s11=round((pivot_point-(0.382*(high-low))),2)
			s22=round((pivot_point-(0.618*(high-low))),2)
			s33=round((pivot_point-(1.0*(high-low))),2)
			r33=round((pivot_point+(1.0*(high-low))),2)
			r11=round((pivot_point+(0.382*(high-low))),2)
			r22=round((pivot_point+(0.618*(high-low))),2)
			temp_list1=[r1,s1,r2,s2,r3,s3,pivot_point,r11,s11,r22,s22,r33,s33]
			temp_list2=sorted(list(set(temp_list1)))
			temp_list=temp_list2[:7]
			if(len(temp_list) > 1):
				print(temp_list)
				difference_list=[temp_list[i+1]-temp_list[(i)] for i in range(len(temp_list)-1)]
				print(difference_list)
				minimum_difference=min(difference_list)

				index=difference_list.index(minimum_difference)
				print(temp_list)
				print(minimum_difference)
				print(index)

				if(temp_list[index+1]  < 0):
					non_negative_list=[i for i in temp_list if i > 0]
					if len(non_negative_list) > 2:
						list_daily_pivots_std1.append(non_negative_list[:2])
					else:
						list_daily_pivots_std1.append(non_negative_list[:])



					
				else:
					list_to_insert=temp_list[:index+2]
					non_negative_list=[i for i in list_to_insert if i > 0]
				#	print(non_negative_list)
					list_daily_pivots_std1.append(non_negative_list)

			else:
				list_daily_pivots_std1.append(temp_list)
				#print(temp_list)

		else:
			temp_list=[0.0]
			list_daily_pivots_std1.append(temp_list)
			print(temp_list)


	
	#print(list_daily_pivots_std1)
	#print(len(list_final8))
	print(len(list_daily_pivots_std1))


 #Function used for getting premium of stocks made by the stringmaker
def scraperlist():
	global list_scraper_outp
	list_scraper_outp=[]
	
	
	o=0
	for i in range(len(scraping_list)):
		
		while (o < len(namelist)):
			
			respon=requests.get(scraping_list[i],timeout=10)
			soupe=bs4.BeautifulSoup(respon.text,'lxml')
			for j in range(o,o+10):
				try:
					result = soupe.find_all('a', attrs={'href': re.compile(namelist[j])})
					list_scraper_outp.append(float(str(result[0]).split('target="_blank">')[1].split('<')[0]))
				except:
					list_scraper_outp.append(0.0)
					continue

			o+=10
			break


#Function to check the closeness of piovot levels to current premium
def proximity_logic_daily(list_daily_pivots_std1,list_scraper_outp):
	x=list_daily_pivots_std1
	proxmity_list2=[]
	value1=list_scraper_outp
	for k in range(len(x)):
	    val=value1[k]
	   # print(namelist[k])
	    lambda_values = list(map(lambda x: (x *0.005) + x, x[k]))
	    
	    lambda_valuess = list(map(lambda x: x-(x *0.005) ,x[k]))
	    
	    for i in range(len(lambda_values)):
	        #print(lambda_values[i])
	        for j in range (len(lambda_valuess)):
	            if (i==j):
	                if val>=lambda_valuess[i] and val<= lambda_values[i] and len(lambda_values)>1:
	                	proxmity_list2.append(namelist[k])
	return (set(proxmity_list2))
#proximity_logic_daily(list_daily_pivots_std1,list_scraper_outp)

#Calculating all the option pivot levels for stock from the medium
def optionpricefinder(stockname):
	list1=[]
	list2=[]
	list3=[]
	global atm_list
	global atm_itm_list
	stocklist='https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?symbolCode=238&symbol={}&symbol={}&instrument=OPTSTK&date=-&segmentLink=17&segmentLink=17'.format(stockname,stockname)
	
	print(stocklist)
	flag=True
	while flag:
		try:
			print('x')
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
			atm_list.append(u[j])
			atm_itm_list.append(u[j+1]-u[j])
			list2.append(format(u[j+1],'.2f'))
			list2.append(format(u[j-1],'.2f'))
			list2.append(format(u[j+2],'.2f'))
			list2.append(format(u[j-2],'.2f'))
			#list2.append(format(u[j+3],'.2f'))
			#list2.append(format(u[j-3],'.2f'))
	return sorted(list2)

	
#Calculation for option pivots levels for index same as above
def optionpricefinderindex(stockname):
	list1=[]
	list2=[]
	list3=[]
	global atm_list
	global atm_itm_list
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
			atm_list.append(u[j])
			atm_itm_list.append(u[j+1]-u[j])
			#format(foo, '.3f'
			list2.append(format(u[j-1],'.2f'))
			list2.append(format(u[j+2],'.2f'))
			list2.append(format(u[j-2],'.2f'))
			#list2.append(format(u[j+3],'.2f'))
			#list2.append(format(u[j-3],'.2f'))
	return sorted(list2)

	
#optionpricefinder("WIPRO")
#Making all the string to hit in order to fetch all the data
def stringmaker(stocknamelist,index_name_list):
	print(stocknamelist)
	stocknamelist=stocknamelist

	index_name_list=index_name_list
	
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
#When we get any stock to update this function is called
def updater(list1):
	#make strings
	global list_daily_pivots_std1
	global namelist
	namelist1=[]
	for i in list1:
		stocklist1=[]
		namelist1=[]
		list_daily_pivots_std_updater=[]
		if i not in ['NIFTY','BANKNIFTY']:
			d=optionpricefinder(i)
			for o in range(len(d)):
				#print(i)
				#time.sleep(5)
				stocklist1.append('https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/getFOHistoricalData.jsp?underlying={}&instrument=OPTSTK&expiry=26SEP2019&type=CE&strike={}&fromDate=undefined&toDate=undefined&datePeriod=3months'.format(i,d[o]))
				namelist1.append('{}&instrument=OPTSTK&strike={}&type=CE'.format(i,d[o]))
				namelist1.append('{}&instrument=OPTSTK&strike={}&type=PE'.format(i,d[o]))
				stocklist1.append('https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/getFOHistoricalData.jsp?underlying={}&instrument=OPTSTK&expiry=26SEP2019&type=PE&strike={}&fromDate=undefined&toDate=undefined&datePeriod=3months'.format(i,d[o]))
				
		else:
			d=optionpricefinderindex(i)
			for o in range(len(d)):
				#print(i)
				#time.sleep(5)
				stocklist1.append('https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/getFOHistoricalData.jsp?underlying={}&instrument=OPTIDX&expiry=26SEP2019&type=CE&strike={}&fromDate=undefined&toDate=undefined&datePeriod=3months'.format(i,d[o]))
				namelist1.append('{}&instrument=OPTIDX&strike={}&type=CE'.format(i,d[o]))
				namelist1.append('{}&instrument=OPTIDX&strike={}&type=PE'.format(i,d[o]))
				stocklist1.append('https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/getFOHistoricalData.jsp?underlying={}&instrument=OPTIDX&expiry=26SEP2019&type=PE&strike={}&fromDate=undefined&toDate=undefined&datePeriod=3months'.format(i,d[o]))

	#	aggeregated_list_stock_index=[]
	#Taking the index to modify the standard pivot list
		indexposn=aggeregated_list_stock_index.index(i)
		#As 10 strike price are there we are multiplying by 10
		start_index=indexposn*10
		#end_index=indexposn*14
		print(start_index)
		print(stocklist1)
		#time.sleep(5)
		updated_list=optionpivotsupdater(stocklist1)
		#print(updated_list)
		#time.sleep(5)
		print(namelist)
		for i in range(len(updated_list)):
			print(start_index+i)
			list_daily_pivots_std1[start_index+i]=updated_list[i]
			namelist[start_index+i]=namelist1[i]
		print(namelist)




#notifier = SlackNotifier("https://hooks.slack.com/services/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")
#If the stock has moved 2% up or down following function will be called which will recalulate pivot levels and replace them in the main list
#same as option pivots function
def optionpivotsupdater(updater_list):
	global list_daily_pivots_std_updater
	list_daily_pivots_std_updater=[]
	stocklist1=updater_list
	x=datetime.now()
	lastmonthlast=(x-timedelta(days=x.day))
	d= lastmonthlast - relativedelta(months=1)+relativedelta(days=1)
	#response_list=[]
	print(len(stocklist1))
	for i in stocklist1:

		datelist=[]
		openlist=[]
		highlist=[]
		lowlist=[]
		closelist=[]
		
		flag=True
		while flag:
			try:
				respon=requests.get(i,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'},timeout=20)
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
		string=str(soupe).split('\n')
		try:
			for j in range(1,len(string)-1):
				print(string[j])
				O=(datetime.strptime(string[j].split('<td>')[1][:-5], '%d-%b-%Y'))
				print(O)
				u=str(O.strftime('%d-%m-%Y'))
				datelist.append(datetime.strptime(u,('%d-%m-%Y')))
				openlist.append(float(string[j].split('<td>')[2][:-5]))
				highlist.append(float(string[j].split('<td>')[3][:-5]))
				lowlist.append(float(string[j].split('<td>')[4][:-5]))
				closelist.append(float(string[j].split('<td>')[5][:-5]))

			dicto=pd.DataFrame({'date': datelist,'close':closelist,'high':highlist,'open':openlist,'low':lowlist})
			k=dicto.set_index('date')
			print(k)
		except:
			dicto=pd.DataFrame({'date':['00-00-0000'],'close':[0.0],'high':[0.0],'low':[0.0],'open': [0.0]})
			k=dicto.set_index('date')
			print(k)
		
		
		if(len(k) > 6):
			temp_list=[]
			a=[]
			ho=[]
			a=(k.loc[str(lastmonthlast):str(d)])
			ho.append((a['high'].max()))
			ho.append((a['low'].max()))
			ho.append((a['close'].max()))
			high=max(ho)
			lowee=[]
			print(a)
			print(len(k))
			low=float(a.groupby('low').first().iloc[:1].index.values[0])

			
			close=(a.head(1)['close'].values[0])
			if(low==0.0 and len(a) != 1):
				low1=(a.groupby('low').first())
				if((len(low1) == 1)):
					low=0.0
					high=0.0
					close=0.0
				else:
					low1=float(low1.iloc[1:2].index.values[0])
					lowee.append(low1)
					lowee.append(a['close'].min())
					print(lowee)
					low=min(lowee)

				
			pivot_point=round(((high+low+close)/3.0),2)
			r1=(2*pivot_point)-low
			s1=round(((2*pivot_point)-high),2)
			r2=round((pivot_point+(high-low)),2)
			s2=round((pivot_point-(high-low)),2)
			r3=round((pivot_point+2*(high-low)),2)
			s3=round((pivot_point-2*(high-low)),2)
			s11=round((pivot_point-(0.382*(high-low))),2)
			s22=round((pivot_point-(0.618*(high-low))),2)
			s33=round((pivot_point-(1.0*(high-low))),2)
			r33=round((pivot_point+(1.0*(high-low))),2)
			r11=round((pivot_point+(0.382*(high-low))),2)
			r22=round((pivot_point+(0.618*(high-low))),2)
			temp_list1=[r1,s1,r2,s2,r3,s3,pivot_point,r11,s11,r22,s22,r33,s33]
			temp_list2=sorted(list(set(temp_list1)))
			temp_list=temp_list2[:7]
			if(len(temp_list) > 1):
				print(temp_list)
				difference_list=[temp_list[i+1]-temp_list[(i)] for i in range(len(temp_list)-1)]
				print(difference_list)
				minimum_difference=min(difference_list)

				index=difference_list.index(minimum_difference)
				print(temp_list)
				print(minimum_difference)
				print(index)

				if(temp_list[index+1]  < 0):
					non_negative_list=[i for i in temp_list if i > 0]
					if len(non_negative_list) > 2:
						list_daily_pivots_std_updater.append(non_negative_list[:2])
					else:
						list_daily_pivots_std_updater.append(non_negative_list[:])
					
				else:
					list_to_insert=temp_list[:index+2]
					non_negative_list=[i for i in list_to_insert if i > 0]
					print(non_negative_list)
			
					list_daily_pivots_std_updater.append(non_negative_list)

			else:
				list_daily_pivots_std_updater.append(temp_list)
			
			#	print(temp_list)

		else:
			temp_list=[0.0]
			list_daily_pivots_std_updater.append(temp_list)
			#print(temp_list)


	
	print(list_daily_pivots_std_updater)
	return list_daily_pivots_std_updater
	#print(len(response_list))
	#print(len(list_daily_pivots_std_updater))
			


#Blocking the options which have come before
block_list=[]
stringmaker(stocknamelist,index_name_list)
optionpivots()

atm_update_list=copy.deepcopy(atm_list)
atm_itm_update_list=copy.deepcopy(atm_itm_list)

#Initilizing the notifier class
notifier = SlackNotifier("https://hooks.slack.com/services/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")


while True:
	try:
		#print('yes')
		with open('ho.txt','a') as fd:
			currentprice()
			#time.sleep(5)
			updater_list=stockupdater()
			
			if(len(updater_list)>0):  
				updater(updater_list)
				 
			
			scraperlist()
			print(list_daily_pivots_std1)
			print(list_scraper_outp)
			
			
			x=proximity_logic_daily(list_daily_pivots_std1,list_scraper_outp)
			print(x)
			fd.write("\n")
			fd.write(str(datetime.now()))
			fd.write(str(updater_list))
			for i in x:
				if i not in block_list:
					notifier.notify("###################################")
					a=namelist.index(i)
					price=list_scraper_outp[a]
					x=i.split("&")
					notifier.notify(" option pivots:-   "+ str(x[0] + "-" +x[2]+"-"+x[3][-2:])+"-"+str(price))
					#notifier.notify(" stocks updated:-   "+ str(updater_list))
					block_list.append(i)
					block_list=list(set(block_list))
					#fd.write(str(datetime.now()))
					fd.write(str(x[0] + "-" +x[2]+"-"+x[3][-2:])+"-"+str(price))
					fd.write(" ")
			fd.write("\n")
			fd.write("\n")
			fd.close()
		print(block_list)
		time.sleep(30)
	
	except:
		continue 














