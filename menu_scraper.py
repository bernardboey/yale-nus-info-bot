import bs4
import requests

from menu import MealCategory, MealType, Meal, Menu

DAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
DAY_TO_TABS = {day: f"tab{i}" for i, day in enumerate(DAYS, start=1)}


class MenuScraper:
    URL = "https://studentlife.yale-nus.edu.sg/dining-experience/daily-dining-menu/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/92.0.4515.131 Safari/537.36"
    }

    def __init__(self):
        response = requests.get(self.URL, headers=self.headers)
        self.soup = bs4.BeautifulSoup(response.text, "html.parser")

    @staticmethod
    def get_meal_type_from_table(table: bs4.element.Tag, name: str):
        meal_type = MealType(name)
        category_name = "No category"
        for tr in table.find_all("tr"):
            tds = tr.find_all("td")
            if len(tds) == 2:
                category_name = tds[0].get_text()
            items = tds[-1].get_text()
            meal_type.add_category(MealCategory(category_name, items))
            if len(tds) > 2:
                raise ValueError("Error: More than 2 columns")
        return meal_type

    def get_day_menu(self, day: str):
        menu = Menu(day)
        tab = self.soup.find("div", id=DAY_TO_TABS[day])
        meals_soup = tab.find_all("div", class_="menu-list")
        for meal_soup in meals_soup:
            meal_name = meal_soup.find("h4").get_text().title()
            meal = Meal(meal_name)
            tables = meal_soup.find_all("table")
            meal.add_type(self.get_meal_type_from_table(tables[0], "Bento"))
            if len(tables) == 2:
                meal.add_type(self.get_meal_type_from_table(tables[1], "Grab & Go"))
            if len(tables) > 2:
                raise ValueError("Error: More than 2 tables")
            menu.add_meal(meal)
        return menu

    def get_week_menu(self):
        """

        Returns:
            A list of Menu objects for each day of the week.
        """
        return [self.get_day_menu(day) for day in DAYS]
