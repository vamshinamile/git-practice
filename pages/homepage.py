from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
# from utilities.logger import get_logger
# logger = get_logger()
from utilities.logger import logger



class Homepage:
    def __init__(self,driver):
        self.driver=driver
        self.search_box=(By.XPATH,"//input[@placeholder='Search Amazon.in']")
        self.wait=WebDriverWait(driver,10)
        self.product_titles = (
        By.XPATH,
         "//div[@data-component-type='s-search-result']//h2[@class='a-size-mini s-line-clamp-1']/span")
        self.first_product=(By.XPATH,
         "(//button[@name='submit.addToCart'])[1]")
        self.cart = (By.ID, "nav-cart")

        self.empty_cart_msg = (
        By.XPATH,
        "//h1[contains(text(),'Your Amazon Cart is empty')]")
    def get_title_element(self):
        logger.info("capturig page titles")
        return self.wait.until(EC.visibility_of_element_located(self.search_box))
    def enter_value_in_search_box(self,search_text):
        logger.info(f"Entering search text : {search_text}")
        self.driver.find_element(*self.search_box).send_keys(search_text, Keys.ENTER)

    def get_search_result_titles(self):
        logger.info("search results capturing")
        return self.driver.find_elements(*self.product_titles)
    def click_button(self):
        logger.info("Adding first product to cart")
        self.driver.find_element(*self.first_product).click()
    def click_cart(self):
        logger.info("clicking the add to cart button")
        self.wait.until(
        EC.element_to_be_clickable(self.cart)
    ).click()


    def get_empty_cart_message(self):
        logger.info("empty cart message verifying")
        return self.wait.until(
        EC.visibility_of_element_located(self.empty_cart_msg)
    ).text
    def message_checking(self):
        logger.info("message checking")