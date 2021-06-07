from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

class googleSearch:
    def __init__(self):

        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')  # Last I checked this was necessary.
        self.driver = webdriver.Chrome(chrome_options=options, executable_path=ChromeDriverManager().install())

    def getResult(self, searchQuery):
        driver =  self.driver
        driver.get("https://www.google.co.in/search?q="+searchQuery)
        try:
            oneResultElement = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, "//div[@class ='Z0LcW XcVN5d']/parent::div[not(@data-attrid='')]/div")))
            resultText = oneResultElement.text
        except TimeoutException:
            speak("Let me think sir")
            try:
                oneResultElement = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "//h2[.='Featured snippet from the web']//ancestor::div[@class='xpdopen']//span[contains(@class,'hgKElc')]")))
                resultText = oneResultElement.text
            except TimeoutException:
                try:
                    oneResultElement = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "(//div[@data-dobid='dfn'])[1]")))
                    resultText = oneResultElement.text
                except TimeoutException:
                    try:
                        WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "//div[@class='mhd1Ld']//a")))
                        listLinks = driver.find_elements_by_xpath("//div[@class='mhd1Ld']//a")
                        linkTexts = [link.text for link in listLinks]
                        if len(linkTexts) >=10:
                            linkTexts = linkTexts[:10]              
                        resultText = ', '.join(linkTexts)
                    except TimeoutException:
                        speak("trying hard sir")
                        try:
                            topResultXpath = "//h2[.='Featured snippet from the web']//ancestor::div[@class='xpdopen']"
                            oneResultElement = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, topResultXpath+"//ul")))
                            listResults = driver.find_elements_by_xpath(topResultXpath+"//ul/li")
                            listResults = [el.text[:-4] for el in listResults]
                            moreResultsLink = driver.find_element_by_xpath(topResultXpath+"//a")
                            resultText = ', '.join(listResults)
                        except TimeoutException:
                            resultText = None

        if not resultText:
            try:
                singleResult = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH,"//div[@id='NotFQb']/*[@class='vXQmIe gsrt']")))
                resultText = singleResult.get_attribute('value')
            except TimeoutException:
                resultText = None

        if not resultText:
            speak("trying last try sir")
            try:
                singleResult = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH,"//div[@class='dDoNo vk_bk gsrt gzfeS']")))
                resultText = singleResult.text
            except TimeoutException:
                resultText = "Sorry I could not help you in this. please try again"
        return resultText   

from speakfile import speak
