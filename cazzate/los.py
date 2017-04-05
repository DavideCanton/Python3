import time
from urllib.parse import quote_plus

from selenium import webdriver

query = quote_plus("the big bang theory")
url = "http://www.thelordofstreaming.it/?s={}&submit=Cerca".format(query)
phantom_js_path = r"C:\Users\Davide\AppData\Roaming\npm\phantomjs.cmd"

driver = webdriver.PhantomJS(phantom_js_path)  # or add to your PATH
driver.set_window_size(1024, 768)  # optional
driver.get(url)
links = list(driver.find_elements_by_css_selector(".entry-title a"))
links = list(links)

for i, link in enumerate(links, start=1):
    print("[{}] - {}".format(i, link.text))

choice = int(input("Scelta>"))
link = links[choice - 1].get_attribute("href")

driver.get(link)

links = list(driver.find_elements_by_css_selector(".entry-content a.external"))

print()
for i, link in enumerate(reversed(links), start=1):
    print("[{}] - {}".format(i, link.text))
choice = int(input("Scelta>") or 1)

driver.get(links[choice - 1].get_attribute("href"))

try:
    rc = driver.find_element_by_css_selector(".recaptcha-checkbox")
    rc.click()
    time.sleep(3)
    btn = driver.find_element_by_css_selector("input[name=sub]")
    btn.click()
except Exception as e:
    pass

time.sleep(6)

link = driver.find_element_by_css_selector("#header #link")

link.click()

driver.save_screenshot('a.png')
