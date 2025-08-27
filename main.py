import json
import os
import time

from dotenv import load_dotenv
from loguru import logger
from playwright.sync_api import sync_playwright, Playwright, Page

from source.scrapper import LuxMedScrapper

load_dotenv(dotenv_path=".env", override=True)

SERVICE = "Konsultacja dermatologiczna"

def run() -> dict:
    with sync_playwright() as p:
        # Init browser
        # p = sync_playwright().start()
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://www.luxmed.pl/")
        page.get_by_role("button", name="Zaakceptuj wszystkie").click()
        page.get_by_role("button", name="Zaloguj").click()
        with page.expect_popup() as popup:
            page.get_by_role("button", name="Portal Pacjenta").click()
        popup_page = popup.value

        lo = LuxMedScrapper(SERVICE)
        lo.login(popup_page)
        lo.post_login_popups(popup_page)
        lo.find_service(popup_page, SERVICE)

        amount = lo.count_free_slots(popup_page)
        logger.info(f"Free slots for {SERVICE}: {amount}")

        context.close()
        browser.close()
    return {"value": amount, "service_name": SERVICE}
if __name__ == "__main__":
    result = run()
    print(json.dumps(result))
