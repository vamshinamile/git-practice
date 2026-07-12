import time
import allure
from pages.homepage import Homepage

@allure.step("verifying the search")
@allure.severity(allure.severity_level.MINOR)
def test_search_fun(driver):
    home=Homepage(driver)
    home.get_title_element()
    home.enter_value_in_search_box("iphone")
    title_list=home.get_search_result_titles()
    for title in title_list[:2]:
        print(title.text)
        assert "Apple" in title.text

# @allure.feature("search")
# @allure.severity(allure.severity_level.CRITICAL)
# def test_add_cart_to_product(driver):
#     home = Homepage(driver)
#     home.click_button()
#     time.sleep(10)
#     print("Item added to cart")
    