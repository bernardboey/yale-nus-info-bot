import datetime

import firebase
from menu import Menu
import menu_scraper


def get_current_week_monday():
    today = datetime.date.today()
    monday = today - datetime.timedelta(days=today.weekday())
    return monday


def get_next_monday():
    today = datetime.date.today()
    monday = today + datetime.timedelta(days=(7 - today.weekday()))
    return monday


def get_week_menus(monday: datetime.date):
    menus = []
    for i in range(7):
        date = monday + datetime.timedelta(days=i)
        menu_dict = firebase.get_menu(date)
        menu = Menu.parse_from_dict(menu_dict) if menu_dict else None
        menus.append(menu)
    return menus


def get_current_week_menus():
    return get_week_menus(get_current_week_monday())


def get_next_week_menus():
    return get_week_menus(get_next_monday())


def scrape_current_week_menus():
    return menu_scraper.MenuScraper().get_week_menu()


def menus_are_equal(old_menus: list[Menu], new_menus: list[Menu]):
    for old_menu, new_menu in zip(old_menus, new_menus):
        if old_menu is None:
            return False
        if old_menu.to_dict() != new_menu.to_dict():
            return False
    return True


def set_dates(menus: list[Menu], monday: datetime.date):
    for i, menu in enumerate(menus):
        date = monday + datetime.timedelta(days=i)
        menu.set_date(date)


def set_current_week_dates(menus: list[Menu]):
    set_dates(menus, get_current_week_monday())


def set_next_week_dates(menus: list[Menu]):
    set_dates(menus, get_next_monday())


def _upload_menus(menus: list[Menu]):
    for menu in menus:
        firebase.insert_menu(menu.to_dict())


def scrape_menus_and_upload():
    current_week_menus = get_current_week_menus()
    next_week_menus = get_next_week_menus()
    scraped_menus = scrape_current_week_menus()

    # Check if next week menus are missing
    if None in next_week_menus:
        # Check if current week menus differ from scraped menus or are missing
        if not menus_are_equal(current_week_menus, scraped_menus):
            # Check if today is Sunday
            if datetime.date.today().weekday() == 7:
                set_next_week_dates(scraped_menus)
            else:
                set_current_week_dates(scraped_menus)
            _upload_menus(scraped_menus)
    else:
        # Check if next week menus differ from scraped menus or are missing
        if not menus_are_equal(next_week_menus, scraped_menus):
            set_next_week_dates(scraped_menus)
            _upload_menus(scraped_menus)
