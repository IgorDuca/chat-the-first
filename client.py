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

unread_messages = []

class Client:
    def __init__(self):
        self.driver = webdriver.Chrome("C:/Users/IGOR/chromedriver.exe")
        self.username = user_tokens["username"]
        self.password = user_tokens["password"]
    def start(self):
        driver = self.driver

        driver.get("https://discord.com/channels/311627659828527104/879662660092821574")

        driver.implicitly_wait(10)

        driver.find_element_by_xpath("/html/body/div/div[2]/div/div/div/div/form/div/div/div[1]/div[2]/div[1]/div/div[2]/input").send_keys(self.username)
        time.sleep(.5)
        driver.find_element_by_xpath("/html/body/div/div[2]/div/div/div/div/form/div/div/div[1]/div[2]/div[2]/div/input").send_keys(self.password)
        time.sleep(.5)

        driver.find_element_by_xpath("/html/body/div/div[2]/div/div/div/div/form/div/div/div[1]/div[2]/button[2]").click()
    def sending_group_messages(self):

        message_list = ["oie, alguém pra conversar? mandem dm", "oie, me chamem na dm, vamo conversar", "oiii, alguém pra conversar na dm? me chama aí", "oieeee, me chamem na dm, vamo cvs"]
        conversation_init_message = random.choice(message_list)

        driver = self.driver

        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div[2]/main/form/div/div/div/div[1]/div/div[1]/div[2]"))).send_keys(conversation_init_message + Keys.RETURN)
        
    def gettingMessages(self):
        driver = self.driver

        driver.maximize_window()

        driver.implicitly_wait(10)

        element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[2]/div/div[2]/div/div/div/div[2]/div[1]/nav/div[2]/div/a[3]/div")))
        element.click()
        
        driver.implicitly_wait(10)

        messages = driver.find_elements_by_class_name("message-2qnXI6")
        message_length = len(messages)

        print("Foram carregadas " + str(message_length) + " mensagens")

    def getting_dm_count(self):
        driver = self.driver

        dms = driver.find_elements_by_class_name("listItemWrapper-KhRmzM")
        dmCount = len(dms) - 1

        return dmCount

    def entering_dms(self):

        driver = self.driver

        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "wrapper-1BJsBx"))).click()

        dm = driver.find_elements_by_class_name("channel-2QD9_O")

        print(dm)

        for i in dm:
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
            
            if(len(unread_messages) >= 1):
                i.click()

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

                time.sleep(100)
        

cl = Client()
# cl.start()

# cl.entering_dms()

# while len(unread_messages) < 1:
#     cl.sending_group_messages()
#     time.sleep(100)
#     cl.entering_dms()
#     time.sleep(100)

# cl.entering_dms()