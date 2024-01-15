from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import sys
import m3u8_To_MP4
import download

filmsearch = input("Film name : ")


chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(options=chrome_options)

url = "https://kidraz.com/saby1jy/home/kidraz"
driver.get(url)
filename = ""

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'inputbox')))
search = driver.find_element(By.CLASS_NAME, "inputbox")
search.send_keys(f"{filmsearch}")
search.send_keys(Keys.ENTER)

films = driver.find_elements(By.ID, "hann")
for i, film in enumerate(films):
    link = film.find_element(By.TAG_NAME, "a").get_attribute("href")
    name = film.text
    print(f"[{i}]  : {name} - {link}")

filmchoice = int(input("Enter number of film : "))
filmlink = films[filmchoice].find_element(By.TAG_NAME, "a")
filename = films[filmchoice].text
print(filmlink)
filmlink.click()

iframe = driver.find_element(By.TAG_NAME, "iframe")
src = iframe.get_attribute("src")
driver.get(src)
code = driver.page_source

videolink = ""

for line in code.split("\n"):
    if "m3u8" in line:
        videolink = line
        break
    else:
        print("No")

print(videolink)
videolink = videolink.split('"')[1]

filename = filename.replace(" ", "")
print(f"Name : {filename}")

m3u8_To_MP4.multithread_download(videolink, mp4_file_name=filename+".mp4")
# download.download(videolink)