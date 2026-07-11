import time

import allure

from pages.homepage import Homepage
@allure.step("launch browser with chrome")
@allure.tag("smoke")
def test_launch_url(driver):
   print("trying to open browser.....")
   home=Homepage(driver)  
   home.get_title_element()
   print(f"page title: {driver.title}")
   print("second_time_page title",driver.title)
   print("launch browser completed")


