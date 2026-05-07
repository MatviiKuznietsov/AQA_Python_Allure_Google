import pytest
from playwright.sync_api import Page, expect
from pages.google_home_page import GoogleHomePage


@pytest.fixture(scope="function")
def setup_page(page: Page):
    """Configure playwright page"""
    page.set_viewport_size({"width": 1280, "height": 720})
    return page


@pytest.fixture(scope="function")
def google_home_page(setup_page: Page):
    """Google homepage page object fixture"""
    return GoogleHomePage(setup_page)
