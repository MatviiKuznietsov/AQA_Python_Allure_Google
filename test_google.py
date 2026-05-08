import pytest
import allure
from pages.google_home_page import GoogleHomePage


@allure.feature("Google Homepage ")
class TestGoogleHomepage:
    
    @allure.feature("Google Homepage ")
    @allure.story("Page Load Verification")
    @allure.title("Verify Google homepage loads successfully")
    @allure.description("Test that Google homepage loads and displays the search form")
    def test_google_homepage_loads(self, google_home_page: GoogleHomePage):
        with allure.step("Navigate to Google homepage"):
            google_home_page.navigate()
        with allure.step("Verify page is fully loaded"):
            google_home_page.verify_page_fully_loaded()

    @allure.feature("Google Homepage ")
    @allure.story("Search Functionality")
    @allure.title("Verify search input accepts text")
    @allure.description("Test that the search input field accepts user input")
    def test_search_input_accepts_text(self, google_home_page: GoogleHomePage):
        search_query = "Playwright testing"
        
        with allure.step("Navigate to Google homepage"):
            google_home_page.navigate()
            
        with allure.step("Type search query"):
            google_home_page.type_search_query(search_query)
        
        with allure.step("Verify search input has expected value"):
            google_home_page.verify_search_input_has_value(search_query)

    @allure.feature("Google Homepage")
    @allure.story("Navigation Elements")
    @allure.title("Verify navigation links are present")
    @allure.description("Test that main navigation links are visible on the page")
    def test_navigation_links_present(self, google_home_page: GoogleHomePage):
        with allure.step("Navigate to Google homepage"):
            google_home_page.navigate()
        with allure.step("Verify all navigation elements are present"):
            google_home_page.verify_all_navigation_elements_present()
