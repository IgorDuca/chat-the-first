from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from chatgui import chatbot_response

import time
import random
import json

import numpy as np

user_tokens = json.loads(open('user_tokens.json').read())

class Client:
    def __init__(self):
        self.driver = webdriver.Chrome("C:/Users/IGOR/chromedriver.exe")
        self.username = user_tokens["username"]
        self.password = user_tokens["password"]
    def start(self):
        driver = self.driver

        driver.get("https://discord.com/channels/311627659828527104/879662694335135784")

        driver.implicitly_wait(10)

        driver.find_element_by_xpath("/html/body/div/div[2]/div/div/div/div/form/div/div/div[1]/div[2]/div[1]/div/div[2]/input").send_keys(self.username)
        time.sleep(.5)
        driver.find_element_by_xpath("/html/body/div/div[2]/div/div/div/div/form/div/div/div[1]/div[2]/div[2]/div/input").send_keys(self.password)
        time.sleep(.5)

        driver.find_element_by_xpath("/html/body/div/div[2]/div/div/div/div/form/div/div/div[1]/div[2]/button[2]").click()
    def sending_group_messages(self):

        driver = self.driver

        driver.get("https://discord.com/channels/311627659828527104/879662694335135784")

        message_list = ["oie, alguém pra conversar? mandem dm", "oie, me chamem na dm, vamo conversar", "oiii, alguém pra conversar na dm? me chama aí", "oieeee, me chamem na dm, vamo cvs"]
        conversation_init_message = random.choice(message_list)

        driver = self.driver

        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div[2]/main/form/div/div/div/div[1]/div/div[1]/div[2]"))).send_keys(conversation_init_message + Keys.RETURN)

    def entering_dms(self):

        driver = self.driver

        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "wrapper-1BJsBx"))).click()

        dm = driver.find_elements_by_class_name("channel-2QD9_O")

        return dm
    
    def getting_dm_count(self, elements):

        unread_messages = []

        for i in elements:
            label = str(i.get_attribute("aria-label"))

            if(label == 'None'):
                print("Ignorando dm irrelevante...")
            else: 
                print("")
                print(label)

                word_list = label.split()
                print(word_list)

                for word in word_list:
                    if(word == "unread,"):
                        print("Dm ainda não foi lida!")
                        unread_messages.append(i)

        return unread_messages
    
    def sending_dm_messages(self, element):
        driver = self.driver

        def send_message():
            element.click()

            msgs = np.array(driver.find_elements_by_class_name("messageContent-2qWWxC"))

            message_count = len(msgs)
            last_message = msgs[message_count - 1].text

            print("")
            print("LAST MESSAGE")
            print(last_message)
            print("")

            response = chatbot_response(last_message)

            chat = driver.find_element_by_xpath("/html/body/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div[2]/main/form/div/div[1]/div/div[3]/div[2]/div")

            chat.send_keys(response + Keys.RETURN)

            driver.get("https://discord.com/channels/@me")

        send_message(element)
            
        

cl = Client()
cl.start()

dms = cl.entering_dms()
unread_dms = cl.getting_dm_count(dms)
count = len(unread_dms)

print("")
print("LISTA DE DM'S")
print(dms)
print("")

print("")
print("FORAM CARREGADAS " + str(count) + " DM'S")
print("")

while count == 0:
    cl.sending_dm_messages(unread_dms)

cl.sending_group_messages()