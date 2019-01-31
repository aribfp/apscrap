import requests
import mechanicalsoup
from bs4 import BeautifulSoup
from pandas import DataFrame

def fetch_data():
    ms = mechanicalsoup.StatefulBrowser()
    ms.open('http://eudragmdp.ema.europa.eu/inspections/view/wda/searchWDA.xhtml')

    ms.select_form()
    ms['GMDPForm:j_idt195'] = 'eu countries'
   
    response = ms.submit_selected()

    if response.status_code == 200:
        bs = ms.get_current_page()
        tabledata = bs.find('table', {'id' : 'GMDPForm:j_idt221'})
        tabledata = bs.find('thead')
    
        header = []
        dicts = {}
        count = 0
        for tr in tabledata.find('tr').find_all('th'):
            if tr.find('a'):
                header.append(tr.find('a').getText().strip())
            elif tr.find('span'):
                header.append(tr.find('span').getText().strip())
            dicts[header[count]] = count
            count += 1
        #print(dicts)
        df = DataFrame(dicts, index=[0])
            
    else:
        print("NAE")
        
    df.to_excel('test.xlsx', sheet_name='sheet1', index=False)


if __name__ == '__main__':
    fetch_data()