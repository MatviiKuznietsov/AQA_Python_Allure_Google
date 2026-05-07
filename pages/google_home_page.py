from playwright.sync_api import Page, expect
import allure
import re


class GoogleHomePage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://www.google.com/"
        
        self.search_input = page.locator("[name='q']")
        self.search_form = page.locator("form[action='/search'], form[role='search']")
        self.gmail_link = page.locator("a[href*='mail.google.com']")
        self.images_link = page.locator("a[href*='imghp']")
        self.apps_button = page.locator("a[aria-label*='Google'], a[aria-label*='Приложения'], a[href*='about/products']")
        self.sign_in_button = page.locator("a[href*='accounts.google.com'], a[href*='ServiceLogin'], button:has-text('Sign in'), button:has-text('Войти')")
        self.consent_accept_button = page.locator("button:has-text('Accept all'), button:has-text('Принять все')")

    @allure.step("Navigate to Google homepage")
    def navigate(self):
        self.page.goto(self.url)
        if self.consent_accept_button.is_visible(timeout=5000):
            self.consent_accept_button.click()
        return self
    
    @allure.step("Get page title")
    def get_title(self):
        """Get current page title"""
        return self.page.title()
    
    @allure.step("Verify page title contains 'Google'")
    def verify_title_contains_google(self):
        """Verify that page title contains 'Google'"""
        expect(self.page).to_have_title(re.compile("Google"))
    
    @allure.step("Verify search form is visible")
    def verify_search_form_visible(self):
        """Verify that search form is visible"""
        expect(self.search_form).to_be_visible()
    
    @allure.step("Verify search input is present")
    def verify_search_input_present(self):
        """Verify that search input is present"""
        expect(self.search_input).to_be_visible()
    
    @allure.step("Type search query: {query}")
    def type_search_query(self, query: str):
        """Type text in search input"""
        self.search_input.fill(query)
        return self
    
    @allure.step("Get search input value")
    def get_search_input_value(self):
        """Get current value of search input"""
        return self.search_input.input_value()
    
    @allure.step("Verify search input has value: {expected_value}")
    def verify_search_input_has_value(self, expected_value: str):
        """Verify that search input has expected value"""
        expect(self.search_input).to_have_value(expected_value)
    
    @allure.step("Verify Gmail link is present")
    def verify_gmail_link_present(self):
        """Verify that Gmail link is present"""
        expect(self.gmail_link).to_be_visible()
    
    @allure.step("Verify Images link is present")
    def verify_images_link_present(self):
        """Verify that Images link is present"""
        expect(self.images_link).to_be_visible()
    
    @allure.step("Verify Google Apps button is present")
    def verify_apps_button_present(self):
        """Verify that Google Apps button is present"""
        expect(self.apps_button).to_be_visible()
    
    @allure.step("Verify Sign In button is present")
    def verify_sign_in_button_present(self):
        """Verify that Sign In button is present"""
        expect(self.sign_in_button).to_be_visible()
    
    @allure.step("Verify all navigation elements are present")
    def verify_all_navigation_elements_present(self):
        """Verify all main navigation elements are present"""
        self.verify_gmail_link_present()
        self.verify_images_link_present()
        self.verify_apps_button_present()
        self.verify_sign_in_button_present()
    
    @allure.step("Verify page is fully loaded")
    def verify_page_fully_loaded(self):
        """Verify that all main page elements are loaded"""
        self.verify_title_contains_google()
        self.verify_search_form_visible()
        self.verify_search_input_present()
