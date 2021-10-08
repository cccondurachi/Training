from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from functools import wraps

def measure(func):
    @wraps(func)
    def _open_and_close_browser(*args, **kwargs):
        driver = webdriver.Chrome("chromedriver.exe")
        driver.get("http://www.python.org")
        try:
            return func(driver, *args, **kwargs)
        finally:
            driver.close()
    return _open_and_close_browser

class SeleniumTests:

    @staticmethod
    @measure
    def first_exercise(driver):
        downloads_xpath = './/li[@id="downloads"]/a'
        all_releases_xpath = './/a[@href="/downloads/"]'
        # object of ActionChains
        a = ActionChains(driver)
        # identify element
        downloads_button = driver.find_element_by_xpath(downloads_xpath)
        # hover over element
        a.move_to_element(downloads_button).perform()

        # identify sub menu element
        all_releases_button = driver.find_element_by_xpath(all_releases_xpath)
        # hover over element and click
        a.move_to_element(all_releases_button).click().perform()
        # nu reusesc sa inlocuiesc li[1] - nu stiu de ce sa ma leg
        most_recent_version_xpath = './/ol[@class="list-row-container menu"]/li[1]/span[@class="release-version"]'
        most_recent_version = driver.find_element_by_xpath(most_recent_version_xpath)

        print("Most recent version is:",most_recent_version.get_attribute('innerHTML') )


    @staticmethod
    @measure
    def second_exercise(driver):
        search_path = '//input[@id="id-search-field"]'
        input_element = driver.find_element_by_xpath(search_path)
        input_element.send_keys('decorator')
        input_element.send_keys(Keys.ENTER)

        first_link_xpath = './/a[@href="/dev/peps/pep-0318/"]'
        first_link = driver.find_element_by_xpath(first_link_xpath).click()

        examples_xpath = './/a[@id="id80"]'
        elements = driver.find_element_by_xpath(examples_xpath).click()

        elements_total_xpath = './/ol[@class="arabic"]'
        elements_total = driver.find_element_by_xpath(elements_total_xpath)
        elements_number = elements_total.find_elements_by_xpath("./li")
        if len(elements_number) == 5:
            print('Current example count is 5')
        else:
            print(('Current example count is not 5'))


if __name__ == '__main__':
    # SeleniumTests.first_exercise()
    SeleniumTests.second_exercise()
