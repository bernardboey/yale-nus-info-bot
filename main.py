import datetime

import database
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


def get_all_dates_for_week(monday: datetime.date):
    return [monday + datetime.timedelta(days=i) for i in range(7)]


def _get_week_menus(monday: datetime.date):
    menus = []
    for date in get_all_dates_for_week(monday):
        menu = database.get_menu(date)
        menus.append(menu)
    return menus


def get_current_week_menus():
    return _get_week_menus(get_current_week_monday())


def get_next_week_menus():
    return _get_week_menus(get_next_monday())


def scrape_all_menus():
    return menu_scraper.MenuScraper().get_all_menus()


def _scrape_week_menus(monday: datetime.date):
    return [menu_scraper.MenuScraper().get_menu_for_date(date) for date in get_all_dates_for_week(monday)]


def scrape_current_week_menus():
    return _scrape_week_menus(get_current_week_monday())


def scrape_next_week_menus():
    return _scrape_week_menus(get_next_monday())


def _upload_menus(menus: list[Menu]):
    for menu in menus:
        database.insert_menu(menu)


def check_whether_menus_are_different(scraped_menu: Menu, uploaded_menu: Menu):
    if scraped_menu != uploaded_menu:
        raise RuntimeError(f"Scraped menu is different from uploaded menu for {scraped_menu.datetime}.\n"
                           f"Scraped menu:\n"
                           f"{scraped_menu}\n"
                           f"Uploaded menu:\n"
                           f"{uploaded_menu}\n")


def scrape_current_week_menus_and_upload(overwrite=False):
    validate_menus_and_upload(scrape_current_week_menus(), get_current_week_menus(), overwrite)


def scrape_next_week_menus_and_upload(overwrite=False):
    validate_menus_and_upload(scrape_next_week_menus(), get_next_week_menus(), overwrite)


def validate_menus_and_upload(scraped_menus, uploaded_menus, overwrite=False):
    if None in uploaded_menus or overwrite:
        _upload_menus(scraped_menus)
    else:
        for scraped_menu, uploaded_menu in zip(scraped_menus, uploaded_menus):
            check_whether_menus_are_different(scraped_menu, uploaded_menu)


def scrape_all_menus_and_upload(overwrite=False):
    scraped_menus = scrape_all_menus()
    for scraped_menu in scraped_menus:
        date = scraped_menu.datetime
        uploaded_menu = database.get_menu(date)
        if uploaded_menu and not overwrite:
            if scraped_menu != uploaded_menu:
                check_whether_menus_are_different(scraped_menu, uploaded_menu)
        else:
            database.insert_menu(scraped_menu)


scrape_all_menus_and_upload()
