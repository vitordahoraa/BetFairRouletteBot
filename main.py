import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

sideA = [5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26, 0]
sideB = [10, 23, 8, 30, 11, 36, 13, 27, 6, 34, 17, 25, 2, 21, 4, 19, 15, 32]


def boot(browser):  # function to boot the script which means logging and navigating through the website
    cookies = browser.find_element_by_css_selector('#onetrust-accept-btn-handler')
    time.sleep(10)
    cookies.click()
    c = open("Credentials.txt", "r").read().split(";")  # Credentials saved in a txt file inside project, where the first string is the username, and the second string is the password
    browser.find_element_by_css_selector('#ssc-liu').send_keys(c[0])
    browser.find_element_by_css_selector('#ssc-lipw').send_keys(c[1])
    time.sleep(2)
    browser.find_element_by_css_selector('#ssc-lis').click()
    time.sleep(8)
    browser.find_element_by_css_selector('#LIVE_CASINO').click()
    time.sleep(5)
    browser.find_element_by_css_selector('a.subnavigation-item:nth-child(3)').click()
    time.sleep(3)
    browser.find_element_by_xpath(
        '/html/body/div[2]/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div/div[16]/div/section').click()
    time.sleep(10)  # goto New Windows
    after = browser.window_handles[1]
    browser.switch_to.window(after)


def getResults(browser, listOfResults, previousResults, roulettes):
    time.sleep(5)
    for table in range(28): # there are 28 roulettes in live casino, and it will iterate through all of them
        try:
            for i in range(2):  # the name can be in two diferent locations, so it will iterate through them
                name = browser.find_element_by_css_selector('div.lobby-tables__item:nth-child(' + str(table + 1) + ') > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(' + str(i + 1) + ')').text
                if name in roulettes:
                    currentValues = []
                    for j in range(6):  # get the first six digits from the roulette and store them in a list
                        currentValues.append(int(browser.find_element_by_css_selector('div.lobby-tables__item:nth-child(' + str(table + 1) + ') > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(5) > div:nth-child(' + str(j + 1) + ')').text))
                    listOfResults[name] = currentValues #  store the list in a the hashmap of current values
                    if len(previousResults) != 0: #  if the previousResults are empty aka first iteration, skip this logic
                        if listOfResults[name] != previousResults[name]: #  if the current result is diferent than the last result, check if the current value has only the side A or side B numbers
                            hasAsideNumber = all(x in sideA for x in currentValues)
                            hasBsideNumber = all(x in sideB for x in currentValues)

                            if (hasAsideNumber):
                                print("A Side Encountered at " + name)
                            elif(hasBsideNumber):
                                print("B Side Encountered at " + name)

        except (NoSuchElementException, ValueError):
            print("Couldn't find elements inside the table ",table)


if __name__ == '__main__':
    browser = webdriver.Firefox()  # browser is an instance of Firefox webdriver
    browser.get("https://betfair.com/")  # get bet website

    listOfResults = {}
    previousResults = {}

    file = open("Roulettes.txt", "r")
    roulettes = file.read().split(";\n")


    boot(browser)  # boot the instance
    while (1):
        previousResults = listOfResults.copy()
        getResults(browser, listOfResults, previousResults, roulettes)
        print(listOfResults)
        print(previousResults)
        print("\n")

#    browser.close()
