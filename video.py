from pydub import AudioSegment
import numpy as np
import math
import cv2
import os

import text

def get_audio_duration(audio_file):
    return len(AudioSegment.from_file(audio_file))

def resize_image(image, width, height, padding=250):
    image_with_border = cv2.copyMakeBorder(image, padding, padding, padding, padding, cv2.BORDER_CONSTANT, value=[0, 0, 0])

    # Calculate the aspect ratio of the original image
    aspect_ratio = image_with_border.shape[1] / image_with_border.shape[0]

    # Calculate the new dimensions to fit within the desired size while preserving aspect ratio
    new_height = height + 2 * padding
    new_width = int(new_height * aspect_ratio)

    # Resize the image to the new dimensions without distorting it
    resized_image = cv2.resize(image_with_border, (new_width, new_height))

    # If the resized image is wider than the desired width, crop it
    if new_width > width or new_height > height:
        start_x = (new_width - width) // 2
        start_y = (new_height - height) // 2
        cropped_image = resized_image[start_y:start_y + height, start_x:start_x + width]
        return cropped_image

    return resized_image

    # Resize the image to the new dimensions without distorting it
    return cv2.resize(image, (new_width, new_height))

def create(narrations, output_dir, output_filename):
    # Define the dimensions and frame rate of the video
    width, height = 1080, 1920  # Change as needed for your vertical video
    frame_rate = 30  # Adjust as needed

    # Create a VideoWriter object to save the video
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # You can change the codec as needed
    temp_video = os.path.join(output_dir, "temp_video.avi")  # Output video file name
    out = cv2.VideoWriter(temp_video, fourcc, frame_rate, (width, height))

    # List of image file paths to use in the video
    image = cv2.imread(os.path.join(output_dir, "image", "input.png"))  # Replace with your image paths
    image = resize_image(image, width, height)

    narration = os.path.join(output_dir, "narrations", "narration_1.mp3")
    duration = get_audio_duration(narration)

    for _ in range(math.floor(duration/1000*30)):
        vertical_video_frame = np.zeros((height, width, 3), dtype=np.uint8)
        vertical_video_frame[:image.shape[0], :] = image

        out.write(vertical_video_frame)

    # Release the VideoWriter and close the window if any
    out.release()
    cv2.destroyAllWindows()

    text.add_narration_to_video(narrations, temp_video, output_dir, output_filename)

    os.remove(temp_video)
