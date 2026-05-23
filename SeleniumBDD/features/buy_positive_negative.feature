Feature: 99acres Buy property search
  As a property buyer
  I want to search and filter Buy listings on 99acres
  So that I can find suitable properties

  @buy @positive
  Scenario: Search Buy properties with valid city and filters
    Given the user opens the 99acres Buy page
    When the user searches for properties using test data row "valid_buy_search"
    And the user applies the property type from test data
    And the user applies the budget range from test data
    And the user applies the bedroom preference from test data
    Then Buy search results should be displayed for the selected location

  @buy @negative
  Scenario: Search Buy properties with invalid location
    Given the user opens the 99acres Buy page
    When the user searches for properties using test data row "invalid_location_search"
    Then a location validation message should be displayed

  @buy @positive
  Scenario: Open a Buy listing from search results
    Given the user opens the 99acres Buy page
    When the user searches for properties using test data row "valid_buy_search"
    And the user opens the first Buy property result
    Then the Buy property detail page should be displayed

