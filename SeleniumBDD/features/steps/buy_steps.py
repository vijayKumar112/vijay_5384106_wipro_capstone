from behave import given, then, when

from pages.buy_page import BuyPage
from utilities.data_reader import get_search_data


@given("the user opens the 99acres home page")
def step_open_home_page(context):
    context.buy_page = BuyPage(context.driver)
    context.buy_page.open_home_page()


@given("the user opens the 99acres Buy page")
def step_open_buy_page(context):
    context.buy_page = BuyPage(context.driver)
    context.buy_page.open_buy_page()


@when("the user selects the Buy module")
def step_select_buy_module(context):
    context.buy_page.select_buy_module()


@when('the user searches for properties using test data row "{row_name}"')
def step_search_using_test_data(context, row_name):
    context.search_data = get_search_data(row_name)
    context.buy_page.search_location(context.search_data["location"])


@when("the user applies the property type from test data")
def step_apply_property_type(context):
    context.buy_page.apply_property_type(context.search_data["property_type"])


@when("the user applies the budget range from test data")
def step_apply_budget(context):
    context.buy_page.apply_budget(
        context.search_data["min_budget"],
        context.search_data["max_budget"],
    )


@when("the user applies the bedroom preference from test data")
def step_apply_bedrooms(context):
    context.buy_page.apply_bedrooms(context.search_data["bedrooms"])


@when("the user opens the first Buy property result")
def step_open_first_result(context):
    context.buy_page.open_first_property_result()


@when("the user opens New Launch properties")
def step_open_new_launch_properties(context):
    context.buy_page.open_new_launch_properties()


@then("Buy search results should be displayed for the selected location")
def step_verify_results(context):
    location = context.search_data["partial_location"]
    assert context.buy_page.has_search_results(location), (
        f"Expected Buy results for location containing '{location}'."
    )


@then("a location validation message should be displayed")
def step_verify_location_validation(context):
    assert context.buy_page.has_location_validation_message(), (
        "Expected validation message for invalid location."
    )


@then("New Launch property listings should be displayed")
def step_verify_new_launch_listings(context):
    assert context.buy_page.has_new_launch_results(), (
        "Expected New Launch property listings."
    )


@then("the Buy property detail page should be displayed")
def step_verify_detail_page(context):
    assert context.buy_page.is_property_detail_page(), (
        "Expected a 99acres Buy property detail page."
    )
