#Author: Arib Franklin Pelayo
#Description: Script to extract data from given URL and export data to excel
#Technologies used: Python, Selenium and Beautifulsoup

#Imports
import requests
import mechanicalsoup
import time
from bs4 import BeautifulSoup
from pandas import DataFrame
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from math import ceil

#Globals
hd = list()
an = list()
ah = list()
sd = list() 
dataToExport = {}

#Variable Set-up
def fetch_data():
    driver = webdriver.Firefox()
    driver.implicitly_wait(50)
    driver.get('http://eudragmdp.ema.europa.eu/inspections/view/wda/searchWDA.xhtml')
    
    element = driver.find_element_by_name("GMDPForm:j_idt195")
    allOptions = element.find_elements_by_tag_name("option") 

    #Optional - Can add loop to naviate all data from dropdown
    #Set static value 0 - For Testing Purpose
    for index, key in enumerate(allOptions):
        if(0 == index):
            key.click()
            key.submit()
        else:
            pass

    driver.find_element_by_name("GMDPForm:j_idt216").click()

    #Utilize implicite wait to display ajax response from submitted form
    div = driver.find_element_by_id("GMDPForm:wdaSearchPanel")
    
    #Get total number of page without URL change
    total = div.find_element_by_id('GMDPForm:wdaSearchPanel_header').text.split("of ")
    pagecount = ceil(int(total[1]) / 10)
    
    html = driver.page_source
    bs = BeautifulSoup(html, 'html.parser')
    tabledata = bs.find('table', {'id' : 'GMDPForm:j_idt221'})

    pophead(tabledata)
    populate(driver, tabledata, 1, pagecount)

#Header set
def pophead(tabledata):
    head = tabledata.find('thead')

    for tr in head.find('tr').find_all('th'):
        hd.append(tr.text.strip())

#Populate List for Extracted Data
def populate(driver, tabledata, initpage, pagecount):
    body = tabledata.find('tbody')

    for tr in body.find_all('tr'):
        for index, td in enumerate(tr.find_all('td')):
            if index == 0:
                an.append(td.text)
            elif index == 2:
                ah.append(td.text)
            elif index == 3:
                #Optional - For formatting purpose only
                definition = ''
                for div in td.find_all('div'):
                    if len(div.text.strip()) > 0:
                        definition += div.text.strip() + '\n'
                    else:
                        pass #Can set own condition
                sd.append(definition)
            else:
                pass

    if initpage == 1:
        pagination(driver, pagecount)

#Paginate Ajax Forms
def pagination(driver, pagecount):
    try:
        for count in range(2, pagecount + 1):
            element = driver.find_element_by_link_text('{}'.format(count))
            element.click()

            time.sleep(10)
            bs = BeautifulSoup(driver.page_source, 'html.parser')
            tabledata = bs.find('table', {'id' : 'GMDPForm:j_idt221'})

            populate(driver, tabledata, count, pagecount)
    except:
        exportexcel()

    #Success Paginate
    exportexcel()

#Set Frame Data for Excel
def exportexcel():
    dataToExport[hd[0]] = list(filter(None, an))  
    dataToExport[hd[2]] = list(filter(None, ah)) 
    dataToExport[hd[3]] = list(filter(None, sd)) 

    df = DataFrame(dataToExport)
    df = df[[ hd[0], hd[2], hd[3] ]]
        
    #Rename Excel File and Sheet
    df.to_excel('FileExport.xlsx', sheet_name='Sheet 1', index=False)

#Base call
if __name__ == '__main__':
    fetch_data()