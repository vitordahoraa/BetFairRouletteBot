import time
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
import pymysql.cursors
import datetime
from datetime import datetime

sideA = [10, 5, 24, 16, 33, 1, 23, 8, 30, 11, 36]
neutral = [20, 14, 31, 9, 22, 13, 27, 6, 34, 7, 29, 18, 34, 17, 25, 2]
sideB = [0, 32, 15, 19, 4, 21, 26, 3, 35, 12, 28]


def boot(browser):  # function to boot the script which means logging and navigating through the website
    time.sleep(10)
    cookies = browser.find_element(By.CSS_SELECTOR,'#onetrust-accept-btn-handler')
    cookies.click()
    c = open("Credentials.txt", "r").read().split(";")  # Credentials saved in a txt file inside project, where the first string is the username, and the second string is the password
    browser.find_element(By.CSS_SELECTOR,'#ssc-liu').send_keys(c[0])
    browser.find_element(By.CSS_SELECTOR,'#ssc-lipw').send_keys(c[1])
    time.sleep(2)
    browser.find_element(By.CSS_SELECTOR,'#ssc-lis').click()
    time.sleep(8)
    browser.find_element(By.CSS_SELECTOR,'#LIVE_CASINO').click()
    time.sleep(5)
    browser.find_element(By.CSS_SELECTOR,'a.subnavigation-item:nth-child(3)').click()
    time.sleep(3)
    browser.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div/div[16]/div/section').click()
    time.sleep(10)  # goto New Windows
    after = browser.window_handles[1]
    browser.switch_to.window(after)


def getResults(browser, mapOfResults, previousResults, roulettes, connection,mapOfTriggers):
    today = datetime.today()
    MaxNumber = 10  # Max number of roulette results to be analysed
    triggerNumber = 5  # number of numbers both in side A or Side B to trigger the message
    time.sleep(5)
    for table in range(28): # there are 28 roulettes in live casino, and it will iterate through all of them
        try:
            for i in range(2):  # the name can be in two different locations, so it will iterate through them
                name = browser.find_element(By.CSS_SELECTOR,'div.lobby-tables__item:nth-child(' + str(table + 1) + ') > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(' + str(i + 1) + ')').text
                if name in roulettes:
                    currentValues = []
                    for j in range(MaxNumber): # get a max of digits from the roulette and store them in a list. Default(10)
                        value = int(browser.find_element(By.CSS_SELECTOR,'div.lobby-tables__item:nth-child(' + str(table + 1) + ') > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(5) > div:nth-child(' + str(j + 1) + ')').text)
                        currentValues.append(value)
                    mapOfResults[name] = currentValues #  store the list in the hashmap of current values
                    if len(previousResults) != 0: #  if the previousResults are empty aka first iteration, skip this logic
                        if mapOfResults[name] != previousResults[name]: #  if the current result is diferent than the last result, check if the current value has only the side A or side B numbers
                            temp = []
                            for k in range(MaxNumber):  # iterate through the numbers to be analysed
                                if currentValues[k] in sideA:
                                    if(all(x in sideA for x in temp) or not temp):  # if the numbers in the temporary list is all A, than insert the A number in it. Don't do that if the temp is empty
                                        temp.append(currentValues[k])
                                    else:
                                        temp.clear()
                                        temp.append(currentValues[k])
                                if currentValues[k] in sideB:
                                    if(all(x in sideB for x in temp) or not temp):  # if the numbers in the temporary list is all B, than insert the B number in it. Don't do that if the temp is empty
                                        temp.append(currentValues[k])
                                    else:
                                        temp.clear()
                                        temp.append(currentValues[k])

                                if len(temp) == triggerNumber:
                                    if(all(x in sideA for x in temp)):
                                        if(temp != mapOfTriggers[name]):
                                            with connection.cursor() as cursor:
                                                print("A SIDE FOUND IN ", name)
                                                mapOfTriggers[name] = temp.copy()
                                                sql = "INSERT INTO pi_whats_msgs_sends (id_msg , id_sequencia, id_user, cavalo, contato, data_envio, enviada) VALUES (1,0,1,%s,%s,%s,0)"
                                                #cursor.execute(sql,(name + " LADO A",5581983276882,datetime.strptime(today.strftime("%d/%m/%y") + " 01:00:00", "%d/%m/%y %H:%M:%S")))
                                                cursor.execute(sql,(name + " LADO A",554799400084,datetime.strptime(today.strftime("%d/%m/%y") + " 01:00:00", "%d/%m/%y %H:%M:%S")))
                                                #cursor.execute(sql,(name + " LADO A",5581999707076,datetime.strptime(today.strftime("%d/%m/%y") + " 01:00:00", "%d/%m/%y %H:%M:%S")))
                                                #cursor.execute(sql,(name + " LADO A",5547996773770,datetime.strptime(today.strftime("%d/%m/%y") + " 01:00:00", "%d/%m/%y %H:%M:%S")))
                                                #cursor.execute(sql,(name + " LADO A",351925197353,datetime.strptime(today.strftime("%d/%m/%y") + " 01:00:00", "%d/%m/%y %H:%M:%S")))
                                                cursor.execute(sql,(name + " LADO A",5547996773770,datetime.strptime(today.strftime("%d/%m/%y") + " 01:00:00", "%d/%m/%y %H:%M:%S")))
                                                print(mapOfTriggers)
                                                temp.clear()
                                    if(all(x in sideB for x in temp)):
                                        if(temp != mapOfTriggers[name]):
                                            with connection.cursor() as cursor:
                                                mapOfTriggers[name] = temp.copy()
                                                print("B SIDE FOUND IN ", name)
                                                sql = "INSERT INTO pi_whats_msgs_sends (id_msg , id_sequencia, id_user, cavalo, contato, data_envio, enviada) VALUES (1,0,1,%s,%s,%s,0)"
                                                #cursor.execute(sql,( name + " LADO B", 5581983276882, datetime.strptime(today.strftime("%d/%m/%y") + " 01:00:00", "%d/%m/%y %H:%M:%S")))
                                                cursor.execute(sql, (name + " LADO B", 554799400084, datetime.strptime(today.strftime("%d/%m/%y") + " 01:00:00", "%d/%m/%y %H:%M:%S")))
                                                #cursor.execute(sql,( name + " LADO B", 5581999707076, datetime.strptime(today.strftime("%d/%m/%y") + " 01:00:00", "%d/%m/%y %H:%M:%S")))
                                                #cursor.execute(sql,( name + " LADO B", 5547996773770, datetime.strptime(today.strftime("%d/%m/%y") + " 01:00:00", "%d/%m/%y %H:%M:%S")))
                                                #cursor.execute(sql,( name + " LADO B", 351925197353, datetime.strptime(today.strftime("%d/%m/%y") + " 01:00:00", "%d/%m/%y %H:%M:%S")))
                                                cursor.execute(sql, (name + " LADO B", 5547996773770, datetime.strptime(today.strftime("%d/%m/%y") + " 01:00:00", "%d/%m/%y %H:%M:%S")))
                                                print(mapOfTriggers)
                                                temp.clear()
                            print("triggerNumber in ", name, " is ", len(temp))

        except (NoSuchElementException, ValueError):
            a = 0


if __name__ == '__main__':
    with open("ConnectionInfo.txt", "r") as connectionFile:
        info = connectionFile.read().split(";\n")
        host = info[0]
        dbUser = info[1]
        dbPass = info[2]
        dbName = info[3]

    connection = pymysql.connect(host=host, user=dbUser, password=dbPass, database=dbName, cursorclass=pymysql.cursors.DictCursor)



    browser = webdriver.Firefox()  # browser is an instance of Firefox webdriver
    browser.get("https://betfair.com/")  # get bet website
    mapOfResults = {}
    previousResults = {}
    
    mapOfTriggers = {}
    with open("Roulettes.txt", "r") as file:
        roulettes = file.read().split(";\n")

    for name in roulettes:
        mapOfTriggers[name] = []  # mapOfTriggers is to save the last trigger of a certain roulette, so that future iterations don't consider it. This only works if the triggerNumber is greater than 4, otherwise there can be more than 1 sequence of A or B numbers inside the MaxNumber, when the maxNumber is set to 10(default).

    with connection:
        boot(browser)  # boot the instance

        while (1):
            previousResults = mapOfResults.copy()
            getResults(browser, mapOfResults, previousResults, roulettes,connection,mapOfTriggers)

#    browser.close()
