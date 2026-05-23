# 99acres Buy Module Automation Report

## Project Title

Automation Testing of 99acres Buy Module Using Selenium with Python

## Project Overview

This project focuses on automating the Buy module of the real estate website 99acres. The automation framework is developed using Selenium WebDriver with Python and follows the Page Object Model design pattern. The purpose of this module is to validate important user actions in the property-buying flow, such as searching for properties, viewing search results, applying filters, opening property details, and verifying contact information.

The project also includes screenshot capture and Allure reporting support so that test execution evidence can be reviewed clearly after running the test suite.

## Application Under Test

Website: https://www.99acres.com

Module: Buy Module

Test Domain: Selenium with Python

## Tools and Technologies Used

- Python
- Selenium WebDriver
- Pytest
- Allure Pytest
- OpenPyXL
- Page Object Model
- Chrome Browser
- WebDriver Manager

## Framework Design

The project is organized using the Page Object Model. Each web page or page section has a separate class containing locators and reusable methods. This makes the automation framework more readable, reusable, and maintainable.

Main folders used in the project:

- `pages`: Contains page classes and web element locators
- `tests`: Contains pytest test cases
- `utilities`: Contains helper files such as logger, Excel reader, and screenshot helper
- `test_data`: Contains test data in Excel format
- `screenshots`: Stores screenshots captured during execution
- `allure-results`: Stores Allure test execution result files

## Real Website Analysis

The real 99acres website contains multiple property modules such as Buy, Rent, New Launch, Commercial, Plots/Land, and Projects. For the Buy module, the user can search for properties by entering a city or locality.

For example, searching for Hyderabad in the Buy module opens a results page similar to:

```text
https://www.99acres.com/search/property/buy/hyderabad?city=269&keyword=Hyderabad&preference=S&res_com=R
```

The Buy results page commonly displays a heading like:

```text
Property in Hyderabad for Sale
```

Important filters observed in the Buy module include:

- Budget
- Type of property
- Number of bedrooms
- Construction status
- Posted by
- Area
- Localities
- Amenities
- RERA Approved
- Properties with photos
- Properties with videos

Buy property cards show sale prices such as `Rs. 84.95 Lac`, `Rs. 1.61 Cr`, or similar values. This is different from the Rent module, where prices are shown as monthly rent.

## Buy Module Test Scenarios

Four positive test cases were implemented for the Buy module.

### Test Case 1: Verify User Can Search Buy Properties by Location

Objective:

To verify that the user can select the Buy tab, enter a location, and navigate to the buy property results page.

Steps:

1. Open 99acres website.
2. Click the Buy tab.
3. Enter location as Hyderabad.
4. Click the Search button.
5. Verify that the Buy results page is displayed.
6. Verify that the page heading contains the searched city.

Expected Result:

The Buy property results page should open successfully and display properties for the selected city.

### Test Case 2: Verify Buy Results Count Is Displayed

Objective:

To verify that the Buy results page displays available property count.

Steps:

1. Open 99acres website.
2. Search for Buy properties in Hyderabad.
3. Capture the results count from the search results page.
4. Verify that the count is greater than zero.

Expected Result:

The page should display a valid property count for the searched location.

### Test Case 3: Verify User Can Apply Buy Property Filters

Objective:

To verify that the user can apply important Buy module filters and still get property results.

Filters Applied:

- 2 BHK
- Residential Apartment
- Ready To Move
- Owner
- Locality
- RERA Approved

Steps:

1. Open the Buy results page.
2. Apply 2 BHK filter.
3. Apply Residential Apartment filter.
4. Apply Ready To Move filter.
5. Apply Owner filter.
6. Apply Locality filter if available.
7. Apply RERA Approved filter if available.
8. Verify that filtered results are displayed.

Expected Result:

Filtered property results should be displayed after applying the filters.

### Test Case 4: Verify User Can Open Buy Property Details and Contact Owner

Objective:

To verify that the user can open a property from the filtered results and access the contact section.

Steps:

1. Open the Buy results page.
2. Apply core Buy filters.
3. Select the first property from the results.
4. Verify that the property details page is opened.
5. Click Shortlist.
6. Open Owner Details.
7. Click View Phone Number.
8. Verify that the contact section is displayed.
9. Capture property title and sale price.

Expected Result:

The property details page should open successfully, and the contact section should be visible.

## Screenshot Implementation

Screenshot capture was implemented using a reusable helper method. Screenshots are saved during important steps of the Buy module flow. Screenshots are also attached to the Allure report.

Screenshot examples include:

- Home page
- Buy location entered
- Buy results page
- 2 BHK filter applied
- Residential Apartment filter applied
- Ready To Move filter applied
- Owner filter applied
- Filtered results page
- Property details page
- Contact section

Screenshots are stored in:

```text
screenshots
```

## Test Data

Test data is stored in:

```text
test_data/search_data.xlsx
```

The Excel file contains data for both Rent and Buy modules, including mobile number, location, module name, city, property type, BHK, posted by, and expected heading.

Sample Buy data:

```text
Location: Hyderabad
Module: Buy
Property Type: Residential Apartment
BHK: 2 BHK
Posted By: Owner
Expected Heading: Property in Hyderabad for Sale
```

## How to Run Tests

Run all Buy module tests:

```powershell
python -m pytest -v -s tests\test_buy_module.py
```

Run tests with Allure result generation:

```powershell
python -m pytest -v -s tests\test_buy_module.py --alluredir=allure-results
```

Show Allure report:

```powershell
allure serve allure-results
```

## Allure Reporting

Allure reporting is used to generate a detailed test execution report. It helps display:

- Test case names
- Test status
- Execution steps
- Logs
- Screenshots
- Failure details

The Python package `allure-pytest` is required to generate Allure result files. The Allure commandline tool is required to view the report in the browser.

## Conclusion

The Buy module automation successfully validates the major positive user flows of the 99acres website. The implemented tests cover searching for buy properties, validating search results, applying filters, opening property details, and verifying owner contact information.

The framework is reusable and can be extended further for negative test cases, more locations, additional property filters, login validation, and cross-browser testing.
