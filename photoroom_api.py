from PIL import Image
from bs4 import BeautifulSoup
import http.client
import urllib.parse
import io
import os
import mimetypes
import base64

# def bg_remove():
#   conn = http.client.HTTPSConnection("sdk.photoroom.com")

#   image_path = "./removeBg/input.png"

#   mime_type = mimetypes.guess_type(image_path)[0]

#   with open(image_path, "rb") as image_file:
#       image_data = image_file.read()
  

#   image_data_base64 = base64.b64encode(image_data).decode()

#   payload = f"""
#   -----011000010111000001101001
#   Content-Disposition: form-data; name="image_file"

#   {image_data_base64}
#   -----011000010111000001101001--
#   """

#   headers = {
#     'Content-Type': "multipart/form-data; boundary=---011000010111000001101001",
#     'Accept': "image/png, application/json",
#     'x-api-key': os.getenv("PHOTOROOM_API_KEY")
#   }

#   conn.request('POST', '/v1/segment', payload, headers)

#   res = conn.getresponse()
#   data = res.read()

#   print(f"Status: {res.status}, Code: {res.getcode()}, Reason: {res.reason}, Data: {data}")
#   if 'image' in res.getheader('Content-Type'):
#       image = Image.open(io.BytesIO(data))
#       image.save('./removeBg/output.png')
#   else:
#      print('The response is not an image.')

   

def bg_generate(imageUrl, output_dir, prompt):
  if not os.path.exists(output_dir):
        os.makedirs(output_dir)

  image_path = os.path.join(output_dir, "input.png")

  conn = http.client.HTTPSConnection("beta-sdk.photoroom.com")

  param = {
    'imageUrl': imageUrl,
    'prompt': prompt,
    'apiKey': os.getenv("PHOTOROOM_API_KEY")
  }

  params_encoded = urllib.parse.urlencode(param)

  headers = {
    'Accept': "image/png, application/json",
    'x-api-key': os.getenv("PHOTOROOM_API_KEY"),
    'Content-Type': 'application/json'
  }

  conn.request("GET", f"/v1/instant-backgrounds?{params_encoded}", headers=headers)

  res = conn.getresponse()
  data = res.read()

  print(f"Status: {res.status}, Code: {res.getcode()}, Reason: {res.reason}")
  if 'image' in res.getheader('Content-Type'):
      image = Image.open(io.BytesIO(data))
      image.save(image_path)
  else:
      print('The response is not an image.')