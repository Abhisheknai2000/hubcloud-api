from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Input(BaseModel):
    url: str

@app.post("/generate")
def generate(data: Input):
    # Example: extract HubCloud ID
    import re
    m = re.search(r"/drive/([^/?]+)", data.url)
    if not m:
        return {"error": "Invalid HubCloud URL"}
    
    file_id = m.group(1)
    generator_url = f"https://gamerxyt.com/hubcloud.php?host=hubcloud&id={file_id}&token=EXAMPLETOKEN"
    pixeldrain_link = f"https://pixeldrain.dev/u/uJSzSnyF"  # Example link
    
    return {
        "hubcloud_url": data.url,
        "generator_url": generator_url,
        "pixeldrain_link": pixeldrain_link
    }

