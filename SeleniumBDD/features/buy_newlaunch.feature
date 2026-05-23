Feature: 99acres Buy new launch properties
  As a buyer
  I want to view new launch properties
  So that I can explore recently launched projects

  @buy @newlaunch @positive
  Scenario: View Buy new launch listings
    Given the user opens the 99acres Buy page
    When the user opens New Launch properties
    Then New Launch property listings should be displayed

  @buy @newlaunch @end_to_end
  Scenario: Open a New Launch property detail page
    Given the user opens the 99acres Buy page
    When the user opens New Launch properties
    And the user opens the first Buy property result
    Then the Buy property detail page should be displayed
