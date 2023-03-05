import numpy as np
import requests

array = np.linspace(0, 255, 256, dtype=np.uint8)
array = np.repeat(array, 256).reshape((256, 256))

array_list = array.tolist()

url = "http://localhost:8000/project"
data = {"image": array_list, "epsg": 1234}

response = requests.post(url, json=data)

print(response.status_code)
print(response.content)
