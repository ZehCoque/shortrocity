from PIL import Image
from bs4 import BeautifulSoup
import http.client
import urllib.parse
import io

def bg_generate(imageUrl, prompt, apiKey):
  conn = http.client.HTTPSConnection("beta-sdk.photoroom.com")

  param = {
    'imageUrl': imageUrl,
    'prompt': prompt,
    'apiKey': apiKey
  }

  params_encoded = urllib.parse.urlencode(param)

  headers = {
    'Accept': "image/png, application/json",
    'x-api-key': apiKey,
    'Content-Type': 'application/json'
  }

  conn.request("GET", f"/v1/instant-backgrounds?{params_encoded}", headers=headers)

  res = conn.getresponse()
  data = res.read()

  print(f"Status: {res.status}, Code: {res.getcode()}, Reason: {res.reason}")
  if 'image' in res.getheader('Content-Type'):
      image = Image.open(io.BytesIO(data))
      image.save('./images/output.png')
  else:
      print('The response is not an image.')

  print(data.decode("utf-8"))