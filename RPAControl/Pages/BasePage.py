import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from RPAControl.Drivers.ChromeDrivers import ChromeDrivers


class BasePage(object):

    driver: WebDriver
    driver = ChromeDrivers.get_driver()

    def find(self, kv) -> WebElement:
        ele = self.driver.find_element(*kv)
        return ele

    def finds(self, kv) -> list:
        time.sleep(2)
        for i in range(3):
            elements = self.driver.find_elements(*kv)
        return elements

    def click_list(self, parameter, val):
        _robotKind = (By.XPATH, '//input[@placeholder={}]'.format(parameter))
        _lis = (By.XPATH, '//div[@class="el-select-dropdown el-popper"]'
                '//ul[@class="el-scrollbar__view el-select-dropdown__list"]'
                '/li/span[text()={}]'.format(val))
        self.find(self._robotKind).click()
        time.sleep(2)
        if len(self.finds(self._lis)) >1:
            self.finds(self._lis)[1].click()
        else:
            self.find(self._lis).click()

    def robot_kind(self, robot_kind):
        _robotKind = (By.XPATH, '//input[contains(@placeholder,"机器人类型")]')
        _robotKind_dialog = (By.XPATH, '//div[@role="dialog"]//input[contains(@placeholder,"机器人类型")]')
        _li = (By.XPATH, '//li[@class="el-select-dropdown__item"]/span[text()="{}"]'.format(robot_kind))
        self.find(_robotKind).click()
        self.find(_li).click()

    def robots_kind(self, robots_kind):
        _robotGroupKind = (By.XPATH, '//input[contains(@placeholder,"机器人组类型")]')
        _lis = (By.XPATH, '//div[@class="el-select-dropdown el-popper"]//'
                          'ul[@class="el-scrollbar__view el-select-dropdown__list"]'
                          '/li/span[text()="{}"]'.format(robots_kind))
        self.finds(_robotGroupKind)[-1].click()
        self.finds(_lis)[-1].click()

    def to_home(self):
        time.sleep(1)
        ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
        return self

    def scroll(self, height):
        _js = 'document.getElementsByClassName("el-table__body-wrapper is-scrolling-none")[0].scrollTop={}'.format(height)
        self.driver.execute_script(_js)
        time.sleep(3)

    def list_operation(self, name, option, cancel=False) -> WebElement:
        _name = (By.XPATH, '//div[@class="el-table__fixed-right"]//span[text()="{}"]/../../../..//span[text()="{}"]'
                 .format(name, option))
        _del = (By.XPATH, '//span[contains(text(),"确定")]')
        _cancel = (By.XPATH, '//span[contains(text(),"取消")]')
        try:
            for i in range(3):
                ele = self.find(_name)
            ele.click()
        except:
            try:
                self.scroll(800)
                ele = self.find(_name).click()
            except:
                self.scroll(-800)
                ele = self.find(_name).click()
        if cancel:
            self.find(_cancel).click()
        else:
            self.find(_del).click()
        # todo return 为Element不合适
        return ele

    def page_operation(self, name="新 增"):
        _name = (By.XPATH, '//span[text()= "{}"]'.format(name))
        self.find(_name).click()

    def select(self, filters, value, dialog=True, ):
        _robotKind = (By.XPATH, '//input[contains(@placeholder,"{}")]'.format(filters))
        _robotKind_dialog = (By.XPATH, '//div[@role="dialog"]//input[contains(@placeholder,"{}")]'.format(filters))
        _robotValue = (By.XPATH, '//li[@class="el-select-dropdown__item"]/span[text()="{}"]'.format(value))

        if dialog:
            self.find(_robotKind_dialog).click()
            self.finds(_robotValue)[-1].click()
        else:
            self.find(_robotKind).click()
            self.finds(_robotValue)[-1].click()

    # def robot_kind(self, robot_kind):
    #     _li = (By.XPATH, '//li[@class="el-select-dropdown__item"]/span[text()="{}"]'.format(robot_kind))
    #     self.find(_robotKind).click()
    #     self.find(_li).click()


if __name__ == "__main__":
    _url = 'http://www.baidu.com'
    _keyword = (By.ID, 'kw')
    pages = BasePage()
    driver = pages.driver
    driver.get(_url)
    pages.find(_keyword).send_keys('123')
    # driver.find(_keyword).send_keys('123')
    # print(dir(driver))
