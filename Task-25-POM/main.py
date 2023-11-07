"""
Using python selenium Explicit wait, Expectd conditions and chrome webdriver kindly do the following mentioned bwlow
    1. Go to https://www.imdb.com/search/name/
    2. fill the data in the input bboxes . select Boxes and Drop down menu on the webpage and do search
    3. Do not use sleep() method for the task.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from webdriver_manager.chrome import ChromeDriverManager

from Data import data
from Locators import locators


class IMDB:
    def __init__(self) :
        self.driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()))
        self.wait = WebDriverWait(self.driver,10)
        self.actions = ActionChains(self.driver)
        self.title_preffered = "IMDb: Advanced Name Search - IMDb"

    def access_URL(self):
        """
        Access IMDb's advanced name search URL and maximize the window.
        """
        try:
            self.driver.maximize_window()
            self.driver.get(data.IMDB_Data().url)
        
        except Exception as selenium_error:
            print(f"An exception occurred: {selenium_error}")

    def check_title(self):
        """
        Checking whether the page is IMDB advanced search 
        if another version of this same url loads it quickly shutdown
        """
        try:
            title_got = self.driver.title
            if title_got == self.title_preffered:
                self.fill_datas()
            else:
                print(f"opened in different ui format :{self.driver.title} other than the code written for {self.title_preffered} :\n please retry")

        except Exception as selenium_error:
            print(f"An Exception ocuured: {selenium_error}")

    def fill_datas(self):
        """
        Enter data into the IMDb search form and click search botton.
        """
        try:
            # Entering name in input
            name = self.wait.until(EC.visibility_of_element_located(
                (By.NAME,locators.IMDM_locators().name_input_name)))
            name.send_keys(data.IMDB_Data().name_box)

            # Entering name in input
            birthday_min = self.wait.until(EC.visibility_of_element_located(
                (By.NAME,locators.IMDM_locators().bd_min_name)))
            birthday_min.send_keys(data.IMDB_Data().bd_min)

            birthday_max = self.wait.until(EC.visibility_of_element_located(
                (By.NAME,locators.IMDM_locators().bd_max_name)))
            birthday_max.send_keys(data.IMDB_Data().bd_max)

            # Selecting name group in check box
            ng_oscar_nom = self.wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR,locators.IMDM_locators().ng_oscar_nominee_for)))
            ng_oscar_nom.click()

            # Entering gender identity
            gi = self.wait.until(EC.visibility_of_element_located(
                (By.ID,locators.IMDM_locators().gi_id)))
            gi.click()

            # Entering a film name and then select options which are dynamically visible after filling data
            self.wait.until(EC.visibility_of_element_located(
                (By.ID,locators.IMDM_locators().filmography_id))).send_keys("iron")
            search_results = self.wait.until(EC.visibility_of_all_elements_located(
                (By.CLASS_NAME, locators.IMDM_locators().filmography_select_class)))
            desired_text = "Iron Man"

            # Iterate through the search results and find the desired text
            for search_result in search_results:
                text = search_result.text
                if desired_text in text:
                    search_result.click()  # Click the matching search result
                    break

            # Selecting name data based on which search result will be shown
            name_data = self.wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR,locators.IMDM_locators().name_data_ip)))
            name_data.click()

            # Setting adults included
            adult_names = self.wait.until(EC.visibility_of_element_located(
                (By.ID,locators.IMDM_locators().an_include_id)))
            adult_names.click()

            # Select count and sort format through Select tag
            do_search_count = self.wait.until(EC.visibility_of_element_located(
                (By.ID,locators.IMDM_locators().do_sea_count_ip)))
            do_search_count.click()
            search_count = self.wait.until(EC.visibility_of_element_located(
                (By.XPATH,locators.IMDM_locators().search_count)))
            search_count.click()

            dp_sort = self.wait.until(EC.visibility_of_element_located(
                (By.XPATH,locators.IMDM_locators().do_sort_ip)))
            dp_sort.click()
            sort = self.wait.until(EC.visibility_of_element_located(
                (By.XPATH,locators.IMDM_locators().sort_ip)))
            sort.click()

            # Clicking Search button
            search_button = self.wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR,locators.IMDM_locators().btn_type)))
            search_button.click()

            # Checking results
            self.checking_results()
            
        except Exception as selenium_error:
            print(f"An exception occurred: {selenium_error}")

        finally:
            self.close_browser()
    
    def checking_results(self):
        """
        Showing result of the search
        """
        try:
            # title of the loaded page
            saarch_result_tab_title = self.driver.title
            print(f"Page Title : {saarch_result_tab_title}")
            
            # Number search results matching in searched page
            search_result = self.wait.until(EC.visibility_of_element_located(
                (By.XPATH,"//div[@id='main']//span"))).text
            print(f"Search results :{search_result}")
        except Exception as selenium_error:
            print(f"Checking Results error: {selenium_error}")
    
    def close_browser(self):
        self.driver.quit()
    

imdb = IMDB()

imdb.access_URL()
imdb.check_title()
