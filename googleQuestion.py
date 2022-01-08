from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

class google(object):
    def __init__(self):
        s = Service(r'C:\Users\khana\Documents\WhatsApp-AI-Bot\chromedriver_win32\chromedriver.exe')
        options = webdriver.ChromeOptions()
        options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        self.driver = webdriver.Chrome(service=s, options=options)
        self.driver.get("https://google.com/")
        self.wait = WebDriverWait(self.driver, 10)
        self.googleSearchBar = (By.CSS_SELECTOR,"#tsf > div:nth-child(1) > div.A8SBwf > div.RNNXgb")
    
    def getElement(self,selector):
        element = None
        try:
            element = self.wait.until(EC.presence_of_element_located((
                By.XPATH, selector)))
        except:
            print("Could not find")
        finally:
            return element
    
    def getGoogle(self, message):
        self.driver.get("https://www.google.com/search?q="+message)
        self.wait.until(EC.presence_of_element_located(self.googleSearchBar))
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        
        gTime = soup.find("div", class_="vk_gy vk_sh card-section sL6Rbf")
        gWeather = soup.find("div", class_="nawv0d")
        gDef = soup.find("div", class_="lr_container yc7KLc mBNN3d") 
        gWiki = soup.find("div", class_="liYKde g VjDLd")
        
        response = None
        
        if gTime:
            response = self.googleTime(gTime)
        elif gWeather :
            response = self.googleWeather(gWeather)
        elif gDef:
            response = self.googleDef(gDef)
        elif gWiki:
            response = self.googleWiki(gWiki)
        
        self.driver.close()
        if response is None:
            return("I dont understand")
        else:
            return response
    
    def googleTime(self, gTime):
        hh_ss = gTime.find("div", class_="gsrt vk_bk FzvWSb YwPhnf").text
        loc = gTime.find("span", class_="vk_gy vk_sh").text
        return loc.strip()+": "+hh_ss
    
    def googleWeather(self, gWeather):
        c = gWeather.find("span", id="wob_tm").text
        x_arg = '//a[@class="wob_t"][@data-metric="false"]' 
        change = self.getElement(x_arg)
        change.click()
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        f = soup.find("span", id="wob_ttm").text
        loc = gWeather.find("div", class_="wob_loc q8U8x").text
        stat = gWeather.find("div", class_="wob_dcp").text
        return loc+": "+c+" °C"+" | "+f+" °F "+"("+stat+")"

    def googleDef(self, gDef):
        try:
            data = gDef.find("div", class_="O5uR6d LTKOO").text
        except:
            data = gDef.find("div", class_="LTKOO sY7ric").text
        return data

    def googleWiki(self, gWiki):
        data = gWiki.find("div", class_="kno-rdesc").text
        return data