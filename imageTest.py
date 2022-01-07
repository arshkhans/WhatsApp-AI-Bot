from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import os
import time
import base64
import pyautogui

s = Service(r'C:\Users\khana\Documents\WhatsApp-AI-Bot\chromedriver_win32\chromedriver.exe')
options = webdriver.ChromeOptions()
options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
driver = webdriver.Chrome(service=s, options=options)

driver.get("https://web.whatsapp.com/")
wait = WebDriverWait(driver, 10)

searchElement = (By.CSS_SELECTOR, "#side > div.uwk68 > div > label > div > div._13NKt.copyable-text.selectable-text")
imageLoaded = (By.CSS_SELECTOR, "#main > div._1LcQK > div > div._33LGR > div.y8WcF > div:nth-child(10) > div > div.Nm1g1._22AX6 > div > div > div.gndfcl4n.l8fojup5.paxyh2gw.sfeitywo.cqsf3vkf.ajgl1lbb.p357zi0d.ac2vgrno.laorhtua.gfz4du6o.r7fjleex.g0rxnol2 > div._1bJJV")
googleSearchBar = (By.CSS_SELECTOR, "#tsf > div:nth-child(1) > div.A8SBwf > div.RNNXgb")
googleImageUpload = (By.CSS_SELECTOR, "#awyMjb")


def getElement(selector):
  element = None
  try:
      element = wait.until(EC.presence_of_element_located((
          By.XPATH, selector)))
  except:
      print("Could not find")
  finally:
      return element

def reverseImageSearch():
    urls = []
    # wait.until(EC.presence_of_element_located(imageLoaded))
    # saveImage()
    
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get("https://tineye.com/")
    
    uploadPath = '//label[contains(@id,"upload-button")]'
    upload = getElement(uploadPath)
    upload.click()
    time.sleep(1)
    
    pyautogui.write(os.getcwd()+"\imageToSave.png", interval=0.01)
    pyautogui.press('enter')
    
    searchImg = '//div[contains(@class,"row match-row")]'
    
    if getElement(searchImg) is None:
        urls = googleImage()
    else:
        soup = BeautifulSoup(driver.page_source, "html.parser")
        for i in soup.find_all("div", class_="row match-row"):
            link = i.find("div", class_="col-xs-9 match-details col-sm-9")
            urls.append(link.find("a")['href'])
        
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    print(urls)
    # sendImgLinks(urls)


def googleImage():
    urls = []
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[2])
    driver.get("https://www.google.com/imghp?hl=en")
    
    imgIcon = getElement('//div[@class="ZaFQO"]')
    imgIcon.click()
    imgUpload = getElement('//a[@class="iOGqzf H4qWMc aXIg1b"]')
    imgUpload.click()
    upload = getElement('//input[@id="awyMjb"]')
    upload.send_keys(os.getcwd()+"\imageToSave.png")
    
    image = getElement('//div[@id="Z6bGOb"]')
    image.click()
    
    if getElement('//div[@class="isv-r PNCib MSM1fd BUooTd"]') is None:
        driver.close()
        driver.switch_to.window(driver.window_handles[1])
        return 
    
    soup = BeautifulSoup(driver.page_source, "html.parser")
    for i in soup.find_all("a", class_="VFACy kGQAp sMi44c lNHeqe WGvvNb"):
        urls.append(i.get('href'))
    
    driver.close()
    driver.switch_to.window(driver.window_handles[1])
    
    return urls

def getBlobLink():
    soup = BeautifulSoup(driver.page_source, "html.parser")
    for i in soup.find_all("div", class_="_3IfUe"):
        blob = i.img["src"]
    return blob

def getBlobData(driver, uri):
    result = driver.execute_async_script("""
    var uri = arguments[0];
    var callback = arguments[1];
    var toBase64 = function(buffer){for(var r,n=new Uint8Array(buffer),t=n.length,a=new Uint8Array(4*Math.ceil(t/3)),i=new Uint8Array(64),o=0,c=0;64>c;++c)i[c]="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charCodeAt(c);for(c=0;t-t%3>c;c+=3,o+=4)r=n[c]<<16|n[c+1]<<8|n[c+2],a[o]=i[r>>18],a[o+1]=i[r>>12&63],a[o+2]=i[r>>6&63],a[o+3]=i[63&r];return t%3===1?(r=n[t-1],a[o]=i[r>>2],a[o+1]=i[r<<4&63],a[o+2]=61,a[o+3]=61):t%3===2&&(r=(n[t-2]<<8)+n[t-1],a[o]=i[r>>10],a[o+1]=i[r>>4&63],a[o+2]=i[r<<2&63],a[o+3]=61),new TextDecoder("ascii").decode(a)};
    var xhr = new XMLHttpRequest();
    xhr.responseType = 'arraybuffer';
    xhr.onload = function(){ callback(toBase64(xhr.response)) };
    xhr.onerror = function(){ callback(xhr.status) };
    xhr.open('GET', uri);
    xhr.send();
    """, uri)
    if type(result) == int :
        raise Exception("Request failed with status %s" % result)
    return base64.b64decode(result)

def saveImage():
    bytes = getBlobData(driver, getBlobLink())
    with open("imageToSave.png", "wb") as fh:
        fh.write(bytes)


def sendImgLinks(urls):
    inp_xpath = '//div[@class="_13NKt copyable-text selectable-text"][@data-tab="9"]'
    privewPath = '//div[contains(@class,"a-HbF")]'
    input_box = getElement(inp_xpath) 
    input_box.send_keys("This is what I found on the Internet" + Keys.ENTER)
    for i in urls:
        print(i)
        input_box = getElement(inp_xpath)
        input_box.send_keys(i)
        getElement(privewPath)
        input_box.send_keys(Keys.ENTER)


reverseImageSearch()