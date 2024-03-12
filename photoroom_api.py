from PIL import Image
from bs4 import BeautifulSoup
import http.client
import urllib.parse
import io

conn = http.client.HTTPSConnection("beta-sdk.photoroom.com")

param = {
  'imageUrl': 'https://www.insiderstore.com.br/cdn/shop/files/BEGE-01.jpg?v=1702674245&width=1206',
  'prompt': 'a beach with some palm trees and a sunset in the background',
  'apiKey': '3789e45d1a2d65de9aac9a2dacacceb7c58fcf05'
}

params_encoded = urllib.parse.urlencode(param)

headers = {
  'Accept': "image/png, application/json",
  'x-api-key': '3789e45d1a2d65de9aac9a2dacacceb7c58fcf05',
  'Content-Type': 'application/json'
}

conn.request("GET", f"/v1/instant-backgrounds?{params_encoded}", headers=headers)

res = conn.getresponse()
data = res.read()

print(f"Status: {res.status}, Code: {res.getcode()}, Reason: {res.reason}")
if 'image' in res.getheader('Content-Type'):
    image = Image.open(io.BytesIO(data))
    image.save('output.png')
else:
    print('The response is not an image.')

print(data.decode("utf-8"))