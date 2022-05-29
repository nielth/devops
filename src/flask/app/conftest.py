# Fixtures stored in conftest.py are automatically loaded by pytest

import os
import time

import pytest
import docker
from selenium import webdriver
import requests

def waitForResourceAvailable(response, timeout, timewait):
    timer = 0
    while response.status_code != 204:
        sleep(timewait)
        timer += timewait
        if timer > timeout:
            break
        if response.status_code == 200:
            break


# This fixture starts Chrome and the website under test in a Docker container.
# The request parameter contains information about the current executing test.
@pytest.fixture
def site(request):
    driver = None
    chrome = None
    website = None

    try:
        # Get Docker client
        client = docker.from_env()
        assert client, 'Failed to get Docker client'

        # Start Chrome Docker image
        chrome = client.containers.run('selenium/standalone-chrome',
                                       ports={'4444/tcp': 4444},
                                       shm_size='2g', detach=True, init=True, auto_remove=True)
        assert chrome, 'Failed to start Chrome container'

        # Start website Docker image
        website = client.containers.run('website',
                                        shm_size='2g', detach=True, init=True, auto_remove=True)
        assert website, 'Failed to start website container'

        # Reload container information and get the container IP
        chrome.reload()
        chrome_ip = chrome.attrs['NetworkSettings']['IPAddress']
        website.reload()
        website_ip = website.attrs['NetworkSettings']['IPAddress']

        while True:
            try:
                response = requests.get(f"http://{chrome_ip}:4444")
                break
            except requests.exceptions.ConnectionError:
                time.sleep(5)



        # Selenium connect URL
        chrome_url = f'http://{chrome_ip}:4444/wd/hub'

        # Connect Selenium to the Chrome container
        driver = webdriver.Remote(chrome_url, webdriver.DesiredCapabilities.CHROME)
        assert driver, f'Failed to connect to Selenium. URL: {chrome_url}'

        # Add the base URL to the driver object so tests can access it
        driver.base_url = f'http://{website_ip}'

        # Yield returns a value to the current executing test. This is where the test itself runs.
        yield driver
    # This block runs after each test has finished, or after an exception
    finally:
        if driver:
            # Save screenshot
            if not os.path.isdir('screenshots'):
                os.mkdir('screenshots')
            driver.save_screenshot(f'screenshots/{request.node.name}.png')

            # Close connection to Chrome
            driver.close()

        # Remove Chrome container
        if chrome:
            chrome.remove(force=True)

        # Remove website container
        if website:
            website.remove(force=True)
