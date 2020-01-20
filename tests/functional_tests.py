import unittest
from selenium import webdriver


class ApplicationLoginFunctionality(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_index_page_logged_out(self):
        driver = self.driver
        driver.get('http://127.0.0.1:8000/')
        assert "You are not logged in" in driver.page_source
        assert "Language" not in driver.page_source

    def test_index_page_login_logout(self):
        driver = self.driver
        driver.get('http://127.0.0.1:8000/')
        driver.find_element_by_id("loginButton").click()

        driver.find_element_by_id("id_username").send_keys("postgres")
        driver.find_element_by_id("id_password").send_keys("postgres")
        driver.find_element_by_xpath("//button[text()='Login']").click()
        assert "You are not logged in" not in driver.page_source
        assert "Language" in driver.page_source

        driver.find_element_by_id("logoutButton").click()
        assert "You are not logged in" in driver.page_source

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()

#print("Testing language evaluator on localhost 127.0.0.1:8000")

# create a new Firefox session
#driver = webdriver.Firefox()
#driver.maximize_window()

# visit page/login
#driver.get('http://127.0.0.1:8000/')
#assert "You are not logged in" in driver.page_source
#
# # Submit form and assert output
# inputElement = driver.find_element_by_id("et_pb_contact_name_0")
# inputElement.send_keys("Kajetan Parzyszek")
# inputElement2 = driver.find_element_by_id("et_pb_contact_message_0")
# inputElement2.send_keys("TEST MESSAGE")
# inputElement2.submit()
# driver.implicitly_wait(30)
# outputElement = driver.find_element_by_css_selector("div.et-pb-contact-message p")
# if outputElement.text == "Form filled out successfully":
#     print("PASSED: send form TEST")
# else:
#     print("FAILED: send form TEST")
#
# # login TEST
# driver.get('https://courses.ultimateqa.com/users/sign_in')
# # Submit form and assert result
# inputElement = driver.find_element_by_id('user_email')
# inputElement.send_keys('kajetan123@gmail.com')
# inputElement2 = driver.find_element_by_id('user_password')
# inputElement2.send_keys('alamakota')
# inputElement2.submit()
# driver.implicitly_wait(30)
# outputElement = driver.find_element_by_class_name("user-name")
# if outputElement.text == "Kajetan P":
#     print("PASSED: login success TEST")
# else:
#     print("FAILED: login success TEST")
# # logout TEST
# driver.get('https://courses.ultimateqa.com/users/sign_out')
# driver.implicitly_wait(30)
# outputElement = driver.find_element_by_class_name("my-account")
# if outputElement.text == "Sign In":
#     print("PASSED: logout TEST")
# else:
#     print("FAILED: logout TEST")
#
# # link redirect TEST
# driver.get('https://www.ultimateqa.com/simple-html-elements-for-automation/')
# # find link and click it then assert redirect effect
# inputElement = driver.find_element_by_id("simpleElementsLink")
# inputElement.click()
# driver.implicitly_wait(30)
# outputElement = driver.find_element_by_class_name("entry-title")
# if outputElement.text == "Link success":
#     print("PASSED: link redirect TEST")
# else:
#     print("FAILED: link redirect TEST")


#driver.quit()