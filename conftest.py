import logging
import os
import time

import requests
from urllib.parse import urlencode
import base64
from selene.support.shared import browser
from selene import be
import config
from selenium import webdriver
import pytest


@pytest.fixture(scope='session', autouse=True)
def browser_management():
    browser.config.base_url = config.config.base_url
    browser.config.driver_name = config.config.driver_name
    browser.config.hold_driver_at_exit = config.config.hold_driver_at_exit
    browser.config.window_width = config.config.window_width
    browser.config.window_height = config.config.window_height
    browser.config.timeout = config.config.timeout

    driver_options = (
        webdriver.ChromeOptions() if config.config.driver_name == 'chrome' else webdriver.FirefoxOptions()
        )
    browser.config.driver_options = driver_options

    yield

    browser.quit()


@pytest.fixture(scope='session', autouse=True)
def obtain_user_token(browser_management):
    client_id = os.getenv('client_id')
    client_secret = os.getenv('client_secret')
    user_mail = os.getenv('user_mail')
    user_password = os.getenv('user_password')
    callback_url = os.getenv('callback_url')
    auth_headers = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": callback_url,
        "scope": config.config.permission_list
    }
    browser.open("/authorize?" + urlencode(auth_headers))

    browser.element('#login-username').type(user_mail)
    browser.element('#login-password').type(user_password)
    browser.element('#login-button').click()
    time.sleep(5)
    if browser.element('[data-testid="auth-accept"]').matching(be.visible):
        browser.element('[data-testid="auth-accept"]').click()
    browser.switch_to_next_tab()
    time.sleep(5)
    current_url = browser.driver.current_url
    part = current_url.split('=')[1]

    encoded_credentials = base64.b64encode(client_id.encode() + b':' + client_secret.encode()).decode("utf-8")

    token_headers = {
        "Authorization": "Basic " + encoded_credentials,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    token_data = {
        "grant_type": "authorization_code",
        "code": part,
        "redirect_uri": "http://localhost:7777/callback"
    }

    r = requests.post("https://accounts.spotify.com/api/token", data=token_data, headers=token_headers)
    #logging.info(r.json())
    token = r.json()["access_token"]

    yield token
