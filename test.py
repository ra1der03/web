from selenium.common import TimeoutException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import json
from selenium.common.exceptions import NoSuchElementException


def wait_element(browser, by=By.TAG_NAME, value=None):
    try:
        return WebDriverWait(browser, 2).until(ec.presence_of_element_located((by, value)))
    except TimeoutException:
        print()


path = ChromeDriverManager().install()
browser_service = Service(executable_path=path)
browser = Chrome(service=browser_service)

browser.get('''https://spb.hh.ru/search/vacancy?area=1&area=2&search_field=name&search_field=company_name&search_
field=description&text=python&enable_snippets=true''')
parsed_data = []

vacancies_list_tag = wait_element(browser, By.ID, 'a11y-main-content')
for vacancy in vacancies_list_tag.find_elements(By.CSS_SELECTOR, "[class='vacancy-serp-item__layout']"):
    df, flag = [], False
    name_tag = wait_element(vacancy, By.TAG_NAME, "h3")
    href_tag = wait_element(vacancy, By.TAG_NAME and By.CLASS_NAME, "a" and "bloko-link")
    df.append(wait_element(vacancy, By.CSS_SELECTOR, "[class='g-user-content']").text)

    for w in df[0].split():
        if ("django" in w.lower()) or ("flask" in w.lower()):
            flag = True
    if (not flag) and ("Django" not in name_tag.text and "Flask" not in name_tag.text):
        continue

    city_tag = wait_element(vacancy, By.CSS_SELECTOR, "[data-qa='vacancy-serp__vacancy-address']").text
    company_tag = wait_element(vacancy, By.CLASS_NAME, 'bloko-text').text

    try:
        salary_el = vacancy.find_element(By.CLASS_NAME, 'bloko-header-section-2').text.replace('\u202f', ' ')
    except NoSuchElementException:
        salary_el = None

    link_absolute = href_tag.get_attribute("href")
    new_data = {
        "company_name": company_tag,
        "link": link_absolute,
        "salary": salary_el,
        "city": city_tag}
    parsed_data.append(new_data)

with open('json_1.json', 'w', encoding="utf-8") as f:
    json.dump(parsed_data, f, ensure_ascii=False, indent=2)

