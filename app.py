from fastapi import FastAPI
from pydantic import BaseModel
import re

app = FastAPI(title="HubCloud → Pixeldrain Generator API")

class Input(BaseModel):
    url: str

@app.post("/generate")
def generate(data: Input):
    match = re.search(r"/drive/([^/?]+)", data.url)
    if not match:
        return {"error": "Invalid HubCloud URL"}

    file_id = match.group(1)
    generator_url = f"https://gamerxyt.com/hubcloud.php?host=hubcloud&id={file_id}&token=EXAMPLETOKEN"
    pixeldrain_link = f"https://pixeldrain.dev/u/uJSzSnyF"

    return {
        "hubcloud_url": data.url,
        "generator_url": generator_url,
        "pixeldrain_link": pixeldrain_link
    }
