# Google Test Framework with Playwright and Allure

This project contains a test framework using Playwright and Allure for testing the Google homepage, implemented with the Page Object pattern for better maintainability and reusability.

## Project Structure

```
AllureHW/
├── requirements.txt          # Project dependencies
├── conftest.py              # Pytest configuration and fixtures
├── test_google.py           # Test cases for Google homepage
├── pytest.ini              # Pytest configuration
├── pages/                   # Page Object directory
│   ├── __init__.py         # Pages package initializer
│   └── google_home_page.py # Google homepage Page Object
└── README.md               # This file
```

## Page Object Pattern

This framework implements the Page Object pattern, which provides the following benefits:

- **Separation of concerns**: Page logic is separated from test logic
- **Reusability**: Page methods can be reused across multiple tests
- **Maintainability**: Changes in UI only require updates to Page Objects
- **Readability**: Tests become more readable and focused on business logic

### GoogleHomePage Page Object

The `GoogleHomePage` class encapsulates all interactions with the Google homepage:

- **Locators**: All element selectors are defined in one place
- **Actions**: Methods for performing actions (navigate, type, click)
- **Verifications**: Methods for asserting page state
- **Allure integration**: Each method includes `@allure.step` decorators for detailed reporting

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install Playwright browsers:
```bash
playwright install
```

3. Install Allure commandline (if not already installed):
- Download from: https://github.com/allure-framework/allure2/releases
- Or use package manager:
  - Windows: `choco install allure`
  - macOS: `brew install allure`
  - Linux: `sudo apt-get install allure`

## Running Tests

### Run all tests:
```bash
pytest
```

### Run specific test file:
```bash
pytest test_google.py
```

### Run with verbose output:
```bash
pytest -v
```

### Run with headless mode (default):
```bash
pytest --headed=false
```

### Run with headed mode (show browser):
```bash
pytest --headed=true
```

## Generating Allure Reports

### Generate and serve Allure report:
```bash
allure serve allure-results
```

### Generate static Allure report:
```bash
allure generate allure-results --clean -o allure-report
```

Then open `allure-report/index.html` in your browser.

## Test Cases

The framework includes 3 basic tests for Google homepage:

1. **test_google_homepage_loads** - Verifies the Google homepage loads successfully
2. **test_search_input_accepts_text** - Tests that the search input accepts user input
3. **test_navigation_links_present** - Verifies navigation elements are present

## Allure Features

- **@allure.feature()** - Groups tests by features
- **@allure.story()** - Groups tests by user stories
- **@allure.title()** - Custom test titles
- **@allure.description()** - Test descriptions
- **@allure.step()** - Step-by-step test execution reporting

## Clean Up

To clean up test results and reports:
```bash
rm -rf allure-results allure-report
```
