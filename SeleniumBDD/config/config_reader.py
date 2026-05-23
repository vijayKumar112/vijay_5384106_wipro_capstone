import configparser
import os
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
CONFIG_FILE = ROOT_DIR / "config" / "config.ini"


class ConfigReader:
    def __init__(self, config_file=CONFIG_FILE):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

    def get(self, section, option, fallback=None):
        return self.config.get(section, option, fallback=fallback)

    def get_int(self, section, option, fallback=0):
        return self.config.getint(section, option, fallback=fallback)

    def get_bool(self, section, option, fallback=False):
        return self.config.getboolean(section, option, fallback=fallback)

    @property
    def base_url(self):
        return self.get("application", "base_url")

    @property
    def buy_url(self):
        return self.get("application", "buy_url")

    @property
    def browser_name(self):
        return os.getenv(
            "BROWSER",
            self.get("browser", "browser_name", fallback="chrome"),
        ).strip().lower()

    @property
    def headless(self):
        env_value = os.getenv("HEADLESS")
        if env_value is not None:
            return env_value.strip().lower() not in {"0", "false", "no"}
        return self.get_bool("browser", "headless", fallback=True)

    @property
    def explicit_wait(self):
        return self.get_int("browser", "explicit_wait", fallback=15)

    @property
    def screenshot_dir(self):
        return ROOT_DIR / self.get("reports", "screenshot_dir", fallback="screenshots")

    @property
    def log_dir(self):
        return ROOT_DIR / self.get("reports", "log_dir", fallback="logs")

    @property
    def search_data_file(self):
        return ROOT_DIR / self.get("testdata", "search_data")


config = ConfigReader()

