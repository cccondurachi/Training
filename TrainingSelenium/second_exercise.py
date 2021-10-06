from selenium import webdriver
from selenium.webdriver.common.keys import Keys



def second_exercise():
    driver = webdriver.Chrome("chromedriver.exe")
    driver.get("http://www.python.org")
    search_path = '//*[@id="id-search-field"]'
    input_element = driver.find_element_by_xpath(search_path)
    input_element.send_keys('decorator')
    input_element.send_keys(Keys.ENTER)

    first_link_xpath = '//*[@id="content"]/div/section/form/ul/li[1]/h3/a'
    first_link = driver.find_element_by_xpath(first_link_xpath).click()

    examples_xpath = '// *[ @ id = "id80"]'
    elements = driver.find_element_by_xpath(examples_xpath).click()

    elements_total_xpath = '// *[ @ id = "examples"] / ol'
    elements_total = driver.find_element_by_xpath(elements_total_xpath)
    children = elements_total.find_elements_by_xpath("./*")
    if len(children) == 5:
        print('Current example count is 5')
    else:
        print(('Current example count is not 5'))




