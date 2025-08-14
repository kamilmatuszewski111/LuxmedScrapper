import os
import time

from dotenv import load_dotenv
from loguru import logger
from playwright.sync_api import sync_playwright, Playwright, Page

load_dotenv(dotenv_path=".env", override=True)

SERVICE = "Konsultacja dermatologiczna"

class LuxMedScrapper:
    def __init__(self, service):
        self.service = service

    @staticmethod
    def conditional_click(locator):
        """
        Click element only if exists.
        """
        time.sleep(1)
        if locator.count():
            locator.click()

    @staticmethod
    def login(page: Page):
        """
        Login procedure.
        """
        page.get_by_role("textbox", name="Wpisz login").press_sequentially(str(os.getenv("LOGIN")))
        page.get_by_role("textbox", name="Wpisz hasło").press_sequentially(str(os.getenv("PASSWORD")))
        page.get_by_role("button", name="Zaloguj się").click()

    def post_login_popups(self, page: Page):
        """"""
        self.conditional_click(page.get_by_role("button", name="Zapisz"))
        self.conditional_click(page.get_by_role("button", name="Pomiń"))


    def find_service(self, page: Page, service: str):
        """"""
        page.get_by_role("button", name="Umów").click()
        for attr in range(3):
            try:
                page.locator('[name^="fake-attribute"]').nth(attr).fill(value=SERVICE, timeout=5000)
                break
            except:
                logger.warning(f"Failed to find {SERVICE}. Next attempt.")
        # page.get_by_text(service).click()
        page.locator('//*[@id="parent_15"]/div[1]').click()

        self.conditional_click(page.get_by_text("Inne"))
        self.conditional_click(page.get_by_role("button", name="Dalej"))
        self.conditional_click(page.get_by_text("Inny powód"))

        if page.get_by_text("Odpowiedz na pytanie").count():
            page.locator('[for="answerId_1"]').first.click()
        if page.get_by_text("Proponowane rozwiązanie").count():
            page.get_by_text('Dermatolog - wizyta w placówce', exact=True).click()

        self.conditional_click(page.get_by_role("button", name="Dalej"))
        self.conditional_click(page.get_by_role("button", name="Szukaj"))

    @staticmethod
    def count_free_slots(page: Page) -> int:

        values = page.locator("div.card-body.p-0.ng-star-inserted span").all_inner_texts()
        return sum(int(v) for v in values if v.isdigit())

def run() -> None:
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
        print(f"Free slots for {SERVICE}: {amount}")

        context.close()
        browser.close()

if __name__ == "__main__":
    run()

