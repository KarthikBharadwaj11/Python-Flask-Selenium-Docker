from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PATH = "/home/kb/Downloads/chromedriver"
driver = webdriver.Chrome(PATH)

driver.get("https://techwithtim.net")

print(driver.title)
 
search = driver.find_element_by_name("s")
search.send_keys("test")
search.send_keys(Keys.RETURN)

 
try:
    main = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.ID, "main"))
    )

    articles = main.find_elements_by_tag_name("article")
    for article in articles:
        header = article.find_element_by_class_name("entry-summary")
        print(header.text)
finally:
    driver.quit()


    



#print(main.text)


#print(driver.page_source)


