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

from QuestionDetection import main

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer


# Replace below path with the absolute path to chromedriver in your computer
s = Service(r'C:\Users\khana\Documents\WhatsApp-AI-Bot\chromedriver_win32\chromedriver.exe')
options = webdriver.ChromeOptions()
options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
driver = webdriver.Chrome(service=s, options=options)

driver.get("https://google.com/")
wait = WebDriverWait(driver, 10)

searchElement = (By.CSS_SELECTOR, "#side > div.uwk68 > div > label > div > div._13NKt.copyable-text.selectable-text")
imageLoaded = (By.CSS_SELECTOR, "#main > div._1LcQK > div > div._33LGR > div.y8WcF > div:nth-child(10) > div > div.Nm1g1._22AX6 > div > div > div.gndfcl4n.l8fojup5.paxyh2gw.sfeitywo.cqsf3vkf.ajgl1lbb.p357zi0d.ac2vgrno.laorhtua.gfz4du6o.r7fjleex.g0rxnol2 > div._1bJJV")

googleSearchBar = (By.CSS_SELECTOR,"#tsf > div:nth-child(1) > div.A8SBwf > div.RNNXgb")

chatbot = ChatBot("Bot", read_only=True,logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': "None",
            'maximum_similarity_threshold': 0.8
        }])

checkQ = main.IsQuestion()

trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.custom.greetings")

def getElement(selector):
  element = None
  try:
      element = wait.until(EC.presence_of_element_located((
          By.XPATH, selector)))
  except:
      print("Could not find")
  finally:
      return element

def sendMessage(number,message):
    # search = driver.find_element(searchElement)
    # search.send_keys(number+Keys.ENTER)
    
    x_arg = '//span[contains(@title,"' + number + '")]'
    group_title = getElement(x_arg)
    group_title.click()
    inp_xpath = '//div[@class="_13NKt copyable-text selectable-text"][@data-tab="9"]'
    input_box = getElement(inp_xpath)
    input_box.send_keys(message + Keys.ENTER)

def enterChat(number):
    x_arg = '//span[contains(@title,"' + number + '")]'
    group_title = getElement(x_arg)
    group_title.click()

def getMessage(number):
    x_arg = '//span[contains(@title,"' + number + '")]'
    group_title = getElement(x_arg)
    group_title.click()
    pass

def openUnread(scrolls=1):
    initial = 10
    for i in range(0, scrolls):
        driver.execute_script("document.getElementById('pane-side').scrollTop={}".format(initial))
        soup = BeautifulSoup(driver.page_source, "html.parser")
        for i in soup.find_all("div", class_="_3OvU8"):
            if i.find("div", class_="_1pJ9J"):
                username = i.find("span", class_="_3q9s6").text
                time.sleep(1)
                enterChat(username)
                sendreply()
                closeChat()
                time.sleep(1)
        initial += 10
 
 
def sendreply():
    soup = BeautifulSoup(driver.page_source, "html.parser")
    for i in soup.find_all("div", class_="message-in"):
        latest = i
    text = latest.find("div", class_="_22Msk")
    img = latest.find("div", class_="cm280p3y")
    vid = latest.find("div", class_="qkl8S _2HVTy")
    if text:
        try:
            message = i.find("span", class_="selectable-text").text
            if len(message) < 2:
                reply = "Please provide me with more than one charater"
            else:
                reply = chatbot.get_response(message)
                print(reply,type(reply),reply.text)
                if reply.text == "None" :
                    if (checkQ.predict_question(message)):
                        reply.text = "Googling your Question..(Not Available Right Now)"
                        reply.text = google(message)
                    else:
                        reply.text = "I am sorry, but I do not understand."
            inp_xpath = '//div[@class="_13NKt copyable-text selectable-text"][@data-tab="9"]'
            input_box = getElement(inp_xpath)
            input_box.send_keys(reply.text + Keys.ENTER)
        except Exception as ex:
            print(ex)
            reply = "I can't understand emojis"
            inp_xpath = '//div[@class="_13NKt copyable-text selectable-text"][@data-tab="9"]'
            input_box = getElement(inp_xpath)
            input_box.send_keys(reply + Keys.ENTER)
    elif img:
        reverseImageSearch()
    elif vid:
        inp_xpath = '//div[@class="_13NKt copyable-text selectable-text"][@data-tab="9"]'
        input_box = getElement(inp_xpath) 
        input_box.send_keys("I dont understand videos" + Keys.ENTER)

   

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


def closeChat():
    chatSettingPath = '//div[@class="_26lC3"][@data-tab ="6"][@title="Menu"]'
    chatSetting = getElement(chatSettingPath)
    chatSetting.click()
    time.sleep(1)
    closeChatPath = '//div[@class="_2oldI dJxPU"][@aria-label="Close chat"]' 
    closeChat = getElement(closeChatPath)
    closeChat.click()

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

def reverseImageSearch():
    urls = []
    time.sleep(2)
    # wait.until(EC.presence_of_element_located(imageLoaded))
    saveImage()
    
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
    
    getElement(searchImg)
    
    soup = BeautifulSoup(driver.page_source, "html.parser")
    for i in soup.find_all("div", class_="row match-row"):
        link = i.find("div", class_="col-xs-9 match-details col-sm-9")
        urls.append(link.find("a")['href'])
        
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    sendImgLinks(urls)

# wait.until(EC.presence_of_element_located(searchElement))

def google(message):
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get("https://www.google.com/search?q="+message)
    wait.until(EC.presence_of_element_located(googleSearchBar))
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    gTime = soup.find("div", class_="vk_gy vk_sh card-section sL6Rbf")
    gWeather = soup.find("div", class_="nawv0d")
    gDef = soup.find("div", class_="lr_container yc7KLc mBNN3d") 
    gWiki = soup.find("div", class_="liYKde g VjDLd")
    if gTime:
        return googleTime(gTime)
    elif gWeather :
        return googleWeather(gWeather)
    elif gDef:
        return googleDef(gDef)
    elif gWiki:
        return googleWiki(gWiki)
    
    return("I dont understand")

def googleTime(gTime):
    hh_ss = gTime.find("div", class_="gsrt vk_bk FzvWSb YwPhnf").text
    loc = gTime.find("span", class_="vk_gy vk_sh").text
    return loc.strip()+": "+hh_ss
    
def googleWeather(gWeather):
    c = gWeather.find("span", id="wob_tm").text
    x_arg = '//a[@class="wob_t"][@data-metric="false"]' 
    change = getElement(x_arg)
    change.click()
    soup = BeautifulSoup(driver.page_source, "html.parser")
    f = soup.find("span", id="wob_ttm").text
    loc = gWeather.find("div", class_="wob_loc q8U8x").text
    stat = gWeather.find("div", class_="wob_dcp").text
    return loc+": "+c+" °C"+" | "+f+" °F "+"("+stat+")"

def googleDef(gDef):
    try:
        data = gDef.find("div", class_="O5uR6d LTKOO").text
    except:
        data = gDef.find("div", class_="LTKOO sY7ric").text
    return data

def googleWiki(gWiki):
    data = gWiki.find("div", class_="kno-rdesc").text
    return data

while(True):
    received = input("->")
    if len(received) < 2:
        botReply = "Please provide me with more than one charater"
    else:
        botReply = chatbot.get_response(received)
        if botReply.text == 'None':
            if (checkQ.predict_question(received)):
                print("Googling your Question")
                print(google(received))
                
                continue
            else:
                print("I am sorry, but I do not understand.")
                continue
    print(botReply)