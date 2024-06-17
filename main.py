import logging
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from parsel import Selector
from time import sleep
import random
import pandas as pd

# start webdriver:
def start_driver():
    options = Options()
    LOGGER.setLevel(logging.WARNING)
    # add arguments to options variable:
    arguments = ['--lang=pt-BR', '--window-size=1920,1080'] #'--headless'
    for argument in arguments:
        options.add_argument(argument)

    driver = webdriver.Chrome(options=options)

    wait = WebDriverWait(
        driver,
        10,
        poll_frequency=1,
        ignored_exceptions=[
            NoSuchElementException,
            ElementNotVisibleException,
            ElementNotSelectableException
        ]
    )
    return driver, wait

def get_page(site, driver, wait):
    driver.get(site)
    wait.until(
        expected_conditions.visibility_of_all_elements_located(
            (By.XPATH, "//input[@id='text-input-what']")
        )
    )    

def scrape(driver, base_url):
    response = Selector(text=driver.page_source)
    for vaga in response.xpath("//td[@class='resultContent css-1qwrrf0 eu4oa1w0']"):
        yield {
            "Cargo" : vaga.xpath("./div/h2/a/span/text()").get(),
            "Empresa" : vaga.xpath("./div[@class='company_location css-17fky0v e37uo190']//span[@data-testid='company-name']/text()").get(),
            "Local" : vaga.xpath("./div[@class='company_location css-17fky0v e37uo190']/div/div[@data-testid='text-location']/text()").get(),
            "Link" : base_url + vaga.xpath("./div/h2/a/@href").get()
        }

def next_page(driver, wait):
    next_btn = driver.find_element(By.XPATH, "//a[@aria-label='Next Page']")
    driver.execute_script("arguments[0].scrollIntoView();", next_btn)
    next_btn.click()
    wait.until(
        expected_conditions.element_to_be_clickable(
            (By.XPATH, "//td[@class='resultContent css-1qwrrf0 eu4oa1w0']")
        )
    )

def main():
    base_url = "https://br.indeed.com"
    url = "https://br.indeed.com/jobs?q=python&l=Belo+Horizonte%2C+MG&vjk=f0f0b60f99b7badf"
    data = []
    driver, wait = start_driver()
    get_page(url, driver, wait)
    # iniciando o scraping...
    while True:
        page_data = scrape(driver, base_url)
        data.extend(page_data)
        # pagination:
        try:
            next_page(driver, wait)
        except ElementClickInterceptedException:
            driver.refresh()
        except:
            break
    # salvando os dados:
    df = pd.DataFrame(data)
    df.to_json("vagas.json", orient='records', index=False)  

if __name__ == "__main__":
    main()
