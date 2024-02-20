# scraper libs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_argument("--headless") # no window to show
options.add_argument("--disable-dev-shm-usage")    
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)

mail_text = "Runtime error"
try:
    driver.get('https://www.crossfitreykjavik.is/')

    # wait on content
    _content = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="content"]'))
    )
    
    contents_lst = []
    contents = driver.find_elements(By.XPATH, '//*[contains(@class,"sos_wodify_section")]')
    for c in contents:
        for cc in c.find_elements(By.XPATH, "./child::*"):
            contents_lst.append(cc.text)
            contents_lst.append("")

    mail_text = "\n".join(contents_lst)
    
except Exception as e:
    print(e.message)

finally:
    # Close the driver
    driver.quit()




# email libs
import smtplib
from email.mime.text import MIMEText

sender = "thorthorssondk@gmail.com"
password = "weus urwo gnyz cyhk"

subject = "WOD CFR"
body = mail_text

recipients = [
	"thingimundarson@gmail.com",
    "ingibjorg.magnus@gmail.com"
]

def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    # print("Message sent!")


    
try:
    send_email(subject, body, sender, recipients, password)
except Exception as e:
    print(e.message)

finally:
    # Close the driver
    driver.quit()