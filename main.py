#!/usr/bin/env python3

from openai import OpenAI
import time
import json
import sys
import os

import narration
import video
import photoroom_api

client = OpenAI()

if len(sys.argv) < 2:
    print(f"USAGE: {sys.argv[0]} SOURCE_FILENAME")
    sys.exit(1)

with open(sys.argv[1]) as f:
    source_material = f.read()

imageDir = os.path.join("removeBg")

short_id = str(int(time.time()))
output_file = "short.avi"

basedir = os.path.join("shorts", short_id)
if not os.path.exists(basedir):
    os.makedirs(basedir)

print("Generating script...")

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {
            "role": "system",
            "content": """You are a YouTube short narration generator. You generate 30 seconds to 1 minute of narration. The shorts you create have an image of a product that will be used to comercialize this product.

Create a narration thinking about selling the product, using excited intonations and convincing the buyer that they need our product. Create a narration DO NOT IN ANY CIRCUMSTANCES use names of celebrities or people.

You are however allowed to use any content, including real names in the narration.

Note that the narration will be fed into a text-to-speech engine, so don't use special characters.

Respond with the narration on the format that follows:

###

Narrator: "One sentence of narration"

Narrator: "One sentence of narration"

Narrator: "One sentence of narration"

###

The short should be 6 sentences maximum.

"""
        },
        {
            "role": "user",
            "content": f"Create a YouTube short narration based on the following source material:\n\n{source_material}"
        }
    ]
)

response_text = response.choices[0].message.content
response_text.replace("’", "'").replace("`", "'").replace("…", "...").replace("“", '"').replace("”", '"')

with open(os.path.join(basedir, "response.txt"), "w") as f:
    f.write(response_text)

data, narrations = narration.parse(response_text)
with open(os.path.join(basedir, "data.json"), "w") as f:
    json.dump(data, f, ensure_ascii=False)

print(f"Generating narration...")
narration.create(data, os.path.join(basedir, "narrations"))

print(f"Removing background...")
output_image_path, filename = photoroom_api.bg_remove(os.path.join("removeBg", "input.png"))

print(f"Generating Image...")
photoroom_api.bg_generate(os.path.join(basedir, "image"), 'An glass table with a mountain view in the background with an sunset', output_image_path, filename)

print("Generating video...")
video.create(narrations, basedir, output_file)

print(f"DONE! Here's your video: {os.path.join(basedir, output_file)}")
