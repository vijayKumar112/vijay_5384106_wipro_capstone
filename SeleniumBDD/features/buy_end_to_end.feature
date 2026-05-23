Feature: 99acres Buy module end-to-end flow
  As a buyer
  I want to complete a full Buy search journey
  So that I can verify the main customer path

  @buy @end_to_end
  Scenario: Complete Buy search journey from home page to property details
    Given the user opens the 99acres home page
    When the user selects the Buy module
    And the user searches for properties using test data row "valid_buy_search"
    And the user applies the property type from test data
    And the user applies the budget range from test data
    And the user applies the bedroom preference from test data
    And the user opens the first Buy property result
    Then the Buy property detail page should be displayed

