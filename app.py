from fastapi import FastAPI
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

app = FastAPI()

class Input(BaseModel):
    url: str

@app.post("/generate")
def generate(data: Input):
    hubcloud_url = data.url

    # Extract HubCloud ID
    m = re.search(r"/drive/([^/?]+)", hubcloud_url)
    if not m:
        return {"error": "Invalid HubCloud URL"}
    file_id = m.group(1)

    # Selenium Chrome options (headless for server)
    options = Options()
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--remote-debugging-port=9222")

    # Initialize Chrome WebDriver
    driver = webdriver.Chrome(options=options)

    pixeldrain_link = None
    try:
        # Generator URL
        generator_url = f"https://gamerxyt.com/hubcloud.php?host=hubcloud&id={file_id}"
        driver.get(generator_url)

        # Wait for link to appear (adjust selector if needed)
        wait = WebDriverWait(driver, 10)
        link_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "a")))
        pixeldrain_link = link_element.get_attribute("href")
    except Exception as e:
        print("Error:", e)
    finally:
        driver.quit()

    if not pixeldrain_link:
        return {"error": "Pixeldrain link not found"}

    return {
        "hubcloud_url": hubcloud_url,
        "generator_url": generator_url,
        "pixeldrain_link": pixeldrain_link
    }
