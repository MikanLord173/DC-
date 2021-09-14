import time
from bs4 import BeautifulSoup
from selenium import webdriver

def run():
    chrome = webdriver.Chrome('C:\\Code\\chromedriver')
    chrome.get('https://webap1.kshs.kh.edu.tw/kshsSSO/publicWebAP/bodyTemp/bodyTempQuery.aspx')

    ID = chrome.find_element_by_id('ContentPlaceHolder1_txtId')
    password = chrome.find_element_by_id('ContentPlaceHolder1_txtPassword')
    confirm = chrome.find_element_by_id('ContentPlaceHolder1_btnId')

    ID.send_keys('080142')
    password.send_keys('080142')
    confirm.click()

    time.sleep(3)
    link = chrome.find_element_by_id('ContentPlaceHolder1_HyperLink1')
    link.click()

    soup = BeautifulSoup(chrome.page_source, 'html.parser')
    rows = soup.find(id='ContentPlaceHolder1_gv0').find_all('tr')

    missing = []
    for a in rows:
        data = a.find_all('td')
        if data:
            student = []
            for b in data:
                if b.getText() == '\xa0':
                    pass
                else:
                    student.append(b.getText())
            if len(student) != 11 and student[2] != '33':
                missing.append(student[2])
    chrome.close()
    print(missing)
    return missing
