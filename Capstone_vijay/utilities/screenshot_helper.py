import os
import re
from datetime import datetime

import allure
from selenium.common.exceptions import WebDriverException


def _safe_file_part(value):

    value = re.sub(r"[^A-Za-z0-9_-]+", "_", value.strip())

    return value.strip("_").lower()


def take_screenshot(driver, test_name, step_name):

    screenshots_dir = "screenshots"

    os.makedirs(screenshots_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    file_name = (
        f"{_safe_file_part(test_name)}_"
        f"{timestamp}_"
        f"{_safe_file_part(step_name)}.png"
    )

    file_path = os.path.join(
        screenshots_dir,
        file_name
    )

    try:
        driver.save_screenshot(file_path)

        with open(file_path, "rb") as screenshot_file:
            allure.attach(
                screenshot_file.read(),
                name=step_name,
                attachment_type=allure.attachment_type.PNG
            )

        print(f"Screenshot saved: {file_path}")

        return file_path

    except WebDriverException as error:
        print(f"Screenshot could not be saved: {error}")

        return None
