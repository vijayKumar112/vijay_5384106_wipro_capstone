# 99acres Buy Module Analysis

## Real 99acres Buy Flow

The current 99acres homepage has these main property modules:

- Buy
- Rent
- New Launch
- Commercial
- Plots/Land
- Projects

For the buy module, the real search results URL uses a sale preference:

```text
https://www.99acres.com/search/property/buy/hyderabad?city=269&keyword=Hyderabad&preference=S&res_com=R
```

The buy results page heading appears as:

```text
Property in Hyderabad for Sale
```

Common buy filters visible on the real site include:

- Verified properties
- Budget
- Type of property
- No. of Bedrooms
- Construction Status
- Posted by
- Area
- Localities
- New Projects / Societies
- Purchase type
- Amenities
- Properties with photos
- Properties with videos
- Furnishing status
- RERA Approved

Buy result cards show sale prices such as `Rs. 84.95 Lac`, `Rs. 1.61 Cr`, or similar values. Rent result cards show `/month` and deposit text, so the buy module should validate sale-style price text instead of rent-style monthly price text.

## Automation Changes

The rent module is kept intact. A separate buy module test was added:

```text
tests/test_buy_module.py
```

The buy module test covers:

- Open 99acres
- Click Buy tab
- Search for Hyderabad
- Verify sale/buy results page
- Apply 2 BHK filter
- Apply Residential Apartment filter
- Apply Ready To Move filter
- Apply Owner filter
- Apply Locality filter when available
- Apply RERA Approved filter when available
- Open the first filtered result
- Shortlist the property
- Open owner/contact details
- Verify contact section
- Capture property title and sale price

## Page Object Updates

Updated files:

- `pages/home_page.py`
- `pages/search_results_page.py`
- `pages/filters_page.py`
- `pages/property_details_page.py`

These changes add buy-specific locators and validations without removing the existing rent flow.
