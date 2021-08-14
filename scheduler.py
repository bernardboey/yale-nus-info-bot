import time

import schedule

import main

schedule.every().day.at("23:00").do(main.scrape_menus_and_upload)
schedule.every().sunday.at("18:00").do(main.scrape_menus_and_upload)
schedule.every().sunday.at("19:00").do(main.scrape_menus_and_upload)
schedule.every().sunday.at("20:00").do(main.scrape_menus_and_upload)
schedule.every().sunday.at("21:00").do(main.scrape_menus_and_upload)
schedule.every().sunday.at("22:00").do(main.scrape_menus_and_upload)
schedule.every().monday.at("00:00").do(main.scrape_menus_and_upload)
schedule.every().monday.at("01:00").do(main.scrape_menus_and_upload)
schedule.every().monday.at("02:00").do(main.scrape_menus_and_upload)

while True:
    schedule.run_pending()
    time.sleep(1)
