from fastapi import FastAPI
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

app = FastAPI()

class Input(BaseModel):
    url: str

@app.post("/generate")
def generate(data: Input):
    # Selenium headless Chrome setup
    options = Options()
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get(data.url)
        time.sleep(2)  # wait for page JS to load

        # Adjust the selector based on the HubCloud page structure
        link_elem = driver.find_element(By.CSS_SELECTOR, "a.pixeldrain")  
        pixeldrain_link = link_elem.get_attribute("href")
    except Exception as e:
        pixeldrain_link = None
    finally:
        driver.quit()
    
    if not pixeldrain_link:
        return {"error": "Pixeldrain link not found on this HubCloud page"}
    
    return {
        "hubcloud_url": data.url,
        "pixeldrain_link": pixeldrain_link
    }
