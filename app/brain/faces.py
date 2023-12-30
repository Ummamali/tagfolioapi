import cv2
from mtcnn.mtcnn import MTCNN
import os

from flask import current_app

from app.brain.utils import extract_filename_without_extension

def extract_and_save_faces(image_path, result_folder_name=None):
    output_dir = extract_filename_without_extension(image_path)
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Unable to read the image from {image_path}")
        return
    # Create the output directory if it doesn't exist
    os.makedirs(current_app.config['TEMP_FOLDER_PATH'], exist_ok=True)
    os.makedirs(os.path.join(current_app.config['TEMP_FOLDER_PATH'], output_dir), exist_ok=True)

    # Initialize the MTCNN face detection model with tuned parameters
    detector = MTCNN(min_face_size=20, scale_factor=0.72)

    # Detect faces in the image
    faces = detector.detect_faces(image)

    # Extract and save each detected face
    for i, face in enumerate(faces):
        x, y, width, height = face['box']
        face_image = image[y:y+height, x:x+width]

        # Save the face image to the output directory
        face_filename = os.path.join(current_app.config['TEMP_FOLDER_PATH'], output_dir, f"face_{i+1}.jpg")
        cv2.imwrite(face_filename, face_image)
        print(f"Face {i+1} saved to {face_filename}")


