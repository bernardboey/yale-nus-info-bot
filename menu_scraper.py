import datetime
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement

from menu import MealCategory, MealType, Meal, Menu


class MenuScraper:
    URL = "https://satscampuseats.yale-nus.edu.sg/our-food"
    USERNAME = os.environ.get("NUSNET_1")
    PASSWORD = os.environ.get("NUSNET_PASSWORD_1")

    def __init__(self):
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.driver.implicitly_wait(5)
        self.login()

    def login(self):
        self.driver.get(self.URL)

        # All HTML elements start with e. For example, e_log_in represents the log_in element.

        e_log_in = self.driver.find_element_by_xpath("//button")
        e_log_in.click()

        e_username = self.driver.find_element_by_id("userNameInput")
        e_username.send_keys(f"nusstu\\{self.USERNAME}")

        e_password = self.driver.find_element_by_id("passwordInput")
        e_password.send_keys(self.PASSWORD)

        e_sign_in = self.driver.find_element_by_id("submitButton")
        e_sign_in.click()

        e_our_food = self.driver.find_element_by_xpath("//header//ul//button")
        e_our_food.click()

    def get_all_date_buttons(self):
        e_date_buttons = self.driver.find_elements_by_xpath(f"//div[contains(@class,'MuiTabs-scroller')]//button")
        # Exclude first element because it represents the "Today" date button.
        return e_date_buttons[1:]

    def get_available_dates(self):
        return [self.get_date_from_button_element(e_date_button) for e_date_button in self.get_all_date_buttons()]

    @staticmethod
    def get_date_from_button_element(e_date_button: WebElement):
        date_string = e_date_button.text.split("\n")[1]
        return datetime.datetime.strptime(date_string, "%d %b %Y").date()

    def select_date(self, date: datetime.date):
        for e_date_button in self.get_all_date_buttons():
            if self.get_date_from_button_element(e_date_button) == date:
                e_date_button.click()
                return
        raise ValueError(f"Date unavailable: {date}")

    def get_all_menus(self):
        menus = []
        for date in self.get_available_dates():
            self.select_date(date)
            menu = self.get_day_menu()
            menu.set_date(date)
            menus.append(menu)
        return menus

    def get_menu_for_date(self, date: datetime.date):
        self.select_date(date)
        menu = self.get_day_menu()
        menu.set_date(date)

    def get_day_menu(self) -> Menu:
        """

        Will return the menu that is currently displayed in the browser. This is dependent on what date was selected
        (using self.select_date(date)). If no date was selected, today's menu will be returned as that is the default
        menu that is displayed on the website.

        Returns:

        """
        menu = Menu()
        e_meal_sections = self.driver.find_elements_by_xpath("//div[@id='root']/div/div/div/div/div/div[3]/div/div")
        for e_meal_section in e_meal_sections[1:]:
            e_meal_name = e_meal_section.find_element_by_tag_name("h2")
            meal = Meal(e_meal_name.text)
            menu.add_meal(meal)
            e_meal_types = e_meal_section.find_elements_by_xpath("div")
            for e_meal_type in e_meal_types:
                e_meal_type_name = e_meal_type.find_element_by_tag_name("h3")
                meal_type = MealType(e_meal_type_name.text)
                meal.add_type(meal_type)
                e_meal_categories = e_meal_type.find_elements_by_xpath("div[2]/div/div")
                for e_meal_category in e_meal_categories:
                    meal_category = MealCategory(e_meal_category.text)
                    meal_type.add_category(meal_category)
        return menu
