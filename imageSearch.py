from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import os

class imageSeach(object):
    def __init__(self):
        s = Service(r'C:\Users\khana\Documents\WhatsApp-AI-Bot\chromedriver_win32\chromedriver.exe')
        options = webdriver.ChromeOptions()
        options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        self.driver = webdriver.Chrome(service=s, options=options)

        self.driver.get("https://tineye.com/")
        self.wait = WebDriverWait(self.driver, 10)
    
    def getElement(self,selector):
        element = None
        try:
            element = self.wait.until(EC.presence_of_element_located((
                By.XPATH, selector)))
        except:
            print("Could not find: "+selector)
        finally:
            return element

    def reverseImageSearch(self):
        urls = []  
        uploadPath = '//input[@id="upload_box"]'
        upload = self.getElement(uploadPath)
        upload.send_keys(os.getcwd()+"\imageToSave.png")

        result = self.getElement('//div[@class="col-sm-9 col-md-8 col-lg-6"]')
        
        try:
            if result.text[:1] == "0":
                urls = self.googleImage()
        except:
            result = self.getElement('//div[@class="search-details"]')
            if result is None:
                urls = self.googleImage()
            else:
                soup = BeautifulSoup(self.driver.page_source, "html.parser")
                for i in soup.find_all("div", class_="row match-row"):
                    link = i.find("div", class_="col-xs-9 match-details col-sm-9")
                    urls.append(link.find("a")['href'])
        self.driver.close()
        return urls

    def googleImage(self):
        urls = []
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get("https://www.google.com/imghp?hl=en")
        
        imgIcon = self.getElement('//div[@class="ZaFQO"]')
        imgIcon.click()
        imgUpload = self.getElement('//a[@class="iOGqzf H4qWMc aXIg1b"]')
        imgUpload.click()
        upload = self.getElement('//input[@id="awyMjb"]')
        upload.send_keys(os.getcwd()+"\imageToSave.png")
        
        image = self.getElement('//div[@id="Z6bGOb"]')
        image.click()
        
        if self.getElement('//div[@class="isv-r PNCib MSM1fd BUooTd"]') is None:
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[1])
            return 
        
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        for i in soup.find_all("a", class_="VFACy kGQAp sMi44c lNHeqe WGvvNb"):
            urls.append(i.get('href'))
        
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        return urls
    