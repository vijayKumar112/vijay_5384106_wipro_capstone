# 99acres Buy Module BDD Project

This is a Behave BDD automation project for the 99acres Buy module using Selenium WebDriver.

## Project Structure

```text
SeleniumBDD/
  behave.ini
  requirements.txt
  config/
    config.ini
    config_reader.py
  features/
    environment.py
    buy_end_to_end.feature
    buy_newlaunch.feature
    buy_positive_negative.feature
    steps/
      buy_steps.py
  pages/
    base_page.py
    buy_page.py
  test_data/
    search_data.csv
  utilities/
    bdd_logger.py
    data_reader.py
  allure-results/
  logs/
  screenshots/
```

## Run Project

```powershell
cd C:\Users\intel\Downloads\SeleniumBDD
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m behave
```

## Run With Allure Results

```powershell
python -m behave -f allure_behave.formatter:AllureFormatter -o allure-results
```

## Run Specific Tags

```powershell
python -m behave --tags=@positive
python -m behave --tags=@negative
python -m behave --tags=@end_to_end
python -m behave --tags=@newlaunch
```
