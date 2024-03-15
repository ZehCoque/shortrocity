from PIL import Image
from bs4 import BeautifulSoup
import http.client
import uuid
import io
import os
import mimetypes

def resize_image(image, width, height):
    aspect_ratio = image.width / image.height
    new_height = height
    new_width = int(new_height * aspect_ratio)

    resized_image = image.resize((new_width, new_height))

    return resized_image

def bg_remove(path_to_file):
  conn = http.client.HTTPSConnection("sdk.photoroom.com")

  image_path = path_to_file

  mime_type = mimetypes.guess_type(image_path)[0]

  with open(image_path, "rb") as image_file:
      image_data = image_file.read()
  
  boundary = '---011000010111000001101001'
  payload = f"--{boundary}\r\nContent-Disposition: form-data; name=\"image_file\"; filename=\"input.png\"\r\nContent-Type: {mime_type}\r\n\r\n"
  payload = payload.encode() + image_data + f"\r\n--{boundary}--\r\n".encode()

  headers = {
    'Content-Type': "multipart/form-data; boundary=---011000010111000001101001",
    'Accept': "image/png, application/json",
    'x-api-key': os.getenv("PHOTOROOM_API_KEY")
  }

  conn.request('POST', '/v1/segment', payload, headers)

  res = conn.getresponse()
  data = res.read()

  randomId = uuid.uuid4()

  filename = f'output_{randomId}.png'
  output_image_path = f'./removeBg/output_{randomId}.png'
  print(f"Status: {res.status}, Code: {res.getcode()}, Reason: {res.reason}")
  if 'image' in res.getheader('Content-Type'):
      image = Image.open(io.BytesIO(data))

      resized_image = resize_image(image, 3840, 2160)
      resized_image.save(f'./removeBg/output_{randomId}.png')
  else:
     print('The response is not an image.')

  return output_image_path, filename
   
def bg_generate(output_dir, prompt, input_image_path, filename):
  if not os.path.exists(output_dir):
        os.makedirs(output_dir)

  image_path = os.path.join(output_dir, "input.png")

  conn = http.client.HTTPSConnection("beta-sdk.photoroom.com")

  mime_type = mimetypes.guess_type(input_image_path)[0]

  with open(input_image_path, "rb") as image_file:
      image_data = image_file.read()

  boundary = '---011000010111000001101001'
  payload = f"-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"prompt\"\r\n\r\n{prompt}\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"imageFile\"; filename=\"{filename}\"\r\nContent-Type: image/png\r\n\r\n"
  payload = payload.encode() + image_data + f"\r\n--{boundary}--\r\n".encode()

  headers = {
    'Content-Type': 'multipart/form-data; boundary=---011000010111000001101001',
    'Accept': "image/png, application/json",
    'x-api-key': os.getenv("PHOTOROOM_API_KEY"),
  }

  conn.request("POST", "/v1/instant-backgrounds", payload, headers)

  res = conn.getresponse()
  data = res.read()

  print(f"Status: {res.status}, Code: {res.getcode()}, Reason: {res.reason}")
  if 'image' in res.getheader('Content-Type'):
      image = Image.open(io.BytesIO(data))
      image.save(image_path)
  else:
      print('The response is not an image.')
     