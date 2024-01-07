import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_homepage_title(browser):   # Navigate to the homepage URL
    browser.get("http://localhost:8000")
    assert "Home" in browser.title

def test_watches_slider(browser):
    browser.get("http://localhost:8000")
    slider = browser.find_element(By.ID, "slider1")
    items = slider.find_elements(By.CLASS_NAME, "item")
    assert len(items) > 0

def test_mobiles_slider(browser):
    browser.get("http://localhost:8000")
    slider = browser.find_element(By.ID, "slider2")
    items = slider.find_elements(By.CLASS_NAME, "item")
    assert len(items) > 0

def test_headphones_slider(browser):
    browser.get("http://localhost:8000")
    slider = browser.find_element(By.ID, "slider3")
    items = slider.find_elements(By.CLASS_NAME, "item")
    assert len(items) > 0
    
# to run pytest homepage.py or just pytest