import pyproj
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    image: str
    epsg: int

@app.get("/")
def index():
    return {"text": "Welcome to our EPSG projection application!"}

@app.post("/project")
def project(item: Item):
    return {
        "image": item.image,
        "epsg": item.epsg
        }

@app.get("/list_projections")
def list_projections():
    codes = pyproj.get_codes("EPSG", "CRS")
    projections = [code for code in codes if pyproj.CRS.from_epsg(code).type_name == "Derived Projected CRS"]

    return projections


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
