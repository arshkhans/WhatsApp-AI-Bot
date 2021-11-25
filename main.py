from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer


# Replace below path with the absolute path
# to chromedriver in your computer
s = Service(r'C:\Users\khana\Documents\Bot\chromedriver_win32\chromedriver.exe')
options = webdriver.ChromeOptions()
options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
driver = webdriver.Chrome(service=s, options=options)

driver.get("https://web.whatsapp.com/")
wait = WebDriverWait(driver, 1000)

searchElement = (By.CSS_SELECTOR, "#side > div.uwk68 > div > label > div > div._13NKt.copyable-text.selectable-text")

chatbot = ChatBot("Nameless", read_only=True)

trainer = ChatterBotCorpusTrainer(chatbot)

trainer.train("chatterbot.corpus.english" )

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
                enterChat(username)
                sendreply()
                closeChat()
                time.sleep(1)
        initial += 10
 
 
def sendreply():
    soup = BeautifulSoup(driver.page_source, "html.parser")
    for i in soup.find_all("div", class_="message-in"):
        message = i.find("span", class_="selectable-text").text
    reply = chatbot.get_response(message)
    inp_xpath = '//div[@class="_13NKt copyable-text selectable-text"][@data-tab="9"]'
    input_box = getElement(inp_xpath)
    input_box.send_keys(reply.text + Keys.ENTER)


def closeChat():
    chatSettingPath = '//div[@class="_26lC3"][@data-tab ="6"][@title="Menu"]'
    chatSetting = getElement(chatSettingPath)
    chatSetting.click()
    time.sleep(1)
    closeChatPath = '//div[@class="_2oldI dJxPU"][@aria-label="Close chat"]' 
    closeChat = getElement(closeChatPath)
    closeChat.click()


wait.until(EC.presence_of_element_located(searchElement))
while(True):
    openUnread()