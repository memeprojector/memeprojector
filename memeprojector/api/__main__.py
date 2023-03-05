import numpy as np
import pyproj
import uvicorn
from fastapi import FastAPI
from PIL import Image
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    image: list
    epsg: int


@app.get("/")
def index():
    return {"text": "Welcome to our EPSG projection application!"}


@app.post("/project")
def project_image(item: Item):
    array = np.array(item.image)
    rgb_array = (array * 255).astype(np.uint8)
    image = Image.fromarray(rgb_array)
    image.save("output_image.png")

    return {
        "image": item.image,
        "epsg": item.epsg,
    }


@app.get("/list_projections")
def list_projections():
    codes = pyproj.get_codes("EPSG", "CRS")
    projections = [code for code in codes if pyproj.CRS.from_epsg(code).type_name == "Derived Projected CRS"]

    return projections


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
