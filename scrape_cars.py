#Web Scrapping to get all the deatils from the page by traversing through all the pages and getting the data into json/CSV

from lxml import html
from bs4 import BeautifulSoup
import requests
import re
import json

#Pass the URL that you want to be scrapped.
url = "https://www.cars.com/dealers/buy/10001/?rd=99999&sortBy=DISTANCE&order=ASC&page=1&perPage=500"

#Split in & so that I can change the page number in the loop and send the request.
urlList = url.split("&")

#Open file in append mode to write the output
with open('carsDealers.csv', 'a') as my_file:
	for x in range(83):  #Pre known value - 83 pages to traverse so run the loop 83 times.
		urlList[3] = ( url.split("&")[3][:5] + str(x+1))   #Change the page number
		parsedUrl = "&".join(urlList)   #create new URL with the changed page number
		print ("\n" + parsedUrl)
		page = requests.get(parsedUrl)   # Send Request
		if page.status_code == 200:    # Status Code Success  
			soup = BeautifulSoup(page.content, "html.parser")
			for div in  soup.findAll("div", class_="page-body "):    # From the response filter only the required div and class
				cardealers = str(div.findAll("script")[3])    # From the script tag, select 3rd tag for our use case
				j = json.loads(cardealers[50:-83])     # Substring so that it can be converted into json
				for each in j['dealerSummaryList']:    # Traverse through only 1 required key
					my_file.write(each['name'].replace(',',' ') + ',' + each['addressLine1'].replace(',',' ') + ',' + str(each['addressLine2']).replace(',',' ') + ',' + each['city'].replace(',',' ') + ',' + each['state'].replace(',',' ') + ',' + each['zip'] + ',' + each['latitude'] + ',' + each['longitude'] + '\n')
			print ("Success Request Code " + str(page.status_code))
			#my_file.write("\n AppenderNewContentForNextPage " + str(x+1) + page.text)
			del soup
			del page
		else:
			print ("Failed Request code " + str(page.status_code))



