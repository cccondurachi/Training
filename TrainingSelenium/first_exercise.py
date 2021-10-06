from selenium import webdriver
from selenium.webdriver import ActionChains

def first_exercise():
    driver = webdriver.Chrome("chromedriver.exe")
    driver.get("http://www.python.org")
    xpath_downloads = '//*[@id="downloads"]/a'

    xpath_all_releases = '//*[@id="downloads"]/ul/li[1]/a'

    # object of ActionChains
    a = ActionChains(driver)
    # identify element
    m = driver.find_element_by_xpath(xpath_downloads)
    # hover over element
    a.move_to_element(m).perform()
    # identify sub menu element
    n = driver.find_element_by_xpath(xpath_all_releases)
    # hover over element and click
    a.move_to_element(n).click().perform()
    most_recent_release = driver.find_element_by_xpath('//*[@id="content"]/div/section/div[1]/ol/li[1]')
    children = most_recent_release.find_elements_by_xpath(".//*")

    print("Most recent release:")
    for child in children:
        print(child.get_attribute("class"), child.get_attribute('innerHTML'))

    # driver.implicitly_wait(2)

    # close browser
    driver.close()