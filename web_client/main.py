# This is a sample Python script.
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import traceback

def main():
    try:
        print("test http request")
        get()
        post()

    except requests.exceptions.HTTPError as errh:
        print(errh)
    except requests.exceptions.ConnectionError as errc:
        print(errc)
    except requests.exceptions.Timeout as errt:
        print(errt)
    except requests.exceptions.RequestException as err:
        print(err)

    print("test web scraping")
    scrap()


def get():
    endpoint = "http://api.open-notify.org/astros.json"
    response = requests.get(endpoint, timeout=5)
    response.raise_for_status()
    print("GET=>" + str(response.json()))


def post():
    endpoint = "https://jsonplaceholder.typicode.com/posts"

    data = {'Alias': '',
            'HtmlBody': '',
            'Name': '',
            'Subject': '',
            'TextBody': ''}
    response = requests.post(url=endpoint, data=data)
    response.raise_for_status()
    print("POST=>" + str(response.json()))


def scrap():
    service = Service("/Users/chienchang.a.huang/temp/python-web-client/chromedriver")

    browser = webdriver.Chrome(service=service)
    browser.get("http://www.google.com")
    input_element = browser.find_element(By.CLASS_NAME, "gLFyf.gsfi")
    input_element.send_keys("Selenium Python")
    input_element.submit()

    try:
        WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "LC20lb.DKV0Md")))

        page1_results = browser.find_elements(By.CLASS_NAME, "LC20lb.DKV0Md")

        for i in range(len(page1_results)):
            print("{} => {}".format(i, page1_results[i].text))

    except TimeoutException:
        print(traceback.format_exc())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
