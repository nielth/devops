import database
from selenium.webdriver.common.keys import Keys


# Check if Python is in the title of the website
def test_title(site):
    # Ask the browser to request the website under test
    site.get("https://work.ab-finance.wtf")

    assert "Example" in site.title
