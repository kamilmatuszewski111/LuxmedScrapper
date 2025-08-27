import json
import os
import time

from dotenv import load_dotenv
from loguru import logger
from playwright.sync_api import sync_playwright, Playwright, Page



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
        """
        Handles post-login popups by conditionally clicking
        the 'Save' or 'Skip' buttons if they appear.
        """
        self.conditional_click(page.get_by_role("button", name="Zapisz"))
        self.conditional_click(page.get_by_role("button", name="Pomiń"))


    def find_service(self, page: Page, service: str):
        """
        Searches for and selects the specified service in the Luxmed system.
        Handles input attributes, additional questions, and proposed solutions
        before proceeding to search for available appointments.
        """
        page.get_by_role("button", name="Umów").click()
        for attr in range(3):
            try:
                page.locator('[name^="fake-attribute"]').nth(attr).fill(value=self.service, timeout=5000)
                break
            except:
                logger.warning(f"Failed to find {self.service}. Next attempt.")
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
        """
            Counts the number of available appointment slots
            based on numeric values extracted from visible page elements.

            Returns:
                int: Total number of free slots found.
            """
        time.sleep(5)
        values = page.locator("div.card-body.p-0.ng-star-inserted span").all_inner_texts()
        return sum(int(v) for v in values if v.isdigit())
