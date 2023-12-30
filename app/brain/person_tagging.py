from app.brain.utils import list_files, list_directories, write_dict_to_json, read_json_to_dict, copy_file, remove_file_extension
from app.brain.faces import extract_and_save_faces
from app.brain.face_similarity import calculate_face_similarity
import os
import json
from flask import current_app

def find_similar_person(folderpath):
	image_names = list_files(folderpath)
	image_paths = [os.path.join(folderpath, name) for name in image_names]
	for path in image_paths:
		extract_and_save_faces(path)

	cache = set()

	report = {}
	pictures = list_directories(current_app.config['TEMP_FOLDER_PATH'])
	for picture in pictures:
		picture_faces = list_files(os.path.join(current_app.config['TEMP_FOLDER_PATH'], picture))
		report[picture] = {}
		for picture_face in picture_faces:
			report[picture][picture_face] = {}
			other_pictures = [fldr for fldr in pictures if fldr != picture]
			for other_picture in other_pictures:
				report[picture][picture_face][other_picture] = {}
				other_picture_faces = list_files(os.path.join(current_app.config['TEMP_FOLDER_PATH'], other_picture))
				for other_picture_face in other_picture_faces:
					left_face = os.path.join(current_app.config['TEMP_FOLDER_PATH'], picture, picture_face)
					right_face = os.path.join(current_app.config['TEMP_FOLDER_PATH'], other_picture, other_picture_face)
					if left_face+right_face not in cache and right_face+left_face not in cache:
						report[picture][picture_face][other_picture][other_picture_face] = float(calculate_face_similarity(left_face, right_face))
						cache.add(left_face+right_face)
						cache.add(right_face+left_face)

	write_dict_to_json(report, "./_temp/report.json")			
	return report
	
def shake_similarity_report(report, threshhold=0.5):
	result = []
	for img, img_report in report.items():
			for face, face_report in img_report.items():
				for other, other_report in face_report.items():
					for other_face, other_face_score in other_report.items():
						if(other_face_score > threshhold):
							shaken_item = {}
							shaken_item[img] = {}
							shaken_item[img][face] = {}
							shaken_item[img][face][other] = {}
							shaken_item[img][face][other][other_face] = float(other_face_score)
							result.append(shaken_item)					
	return result



def tag_people_in(directory, threshhold=0.5):
	image_names = list_files(directory)
	image_paths = [os.path.join(directory, name) for name in image_names]
	for path in image_paths:
		extract_and_save_faces(path)

	result = {name: {"present": []} for name in image_names}
	known_faces_dir_path = os.path.join(current_app.config["BRAIN_PATH"], "known_faces")
	known_faces_data_path = os.path.join(current_app.config["BRAIN_PATH"], "known_faces.json")
	known_data = read_json_to_dict(known_faces_data_path)
	known_faces = list_files(known_faces_dir_path)
	for known_face in known_faces:
		other_images = list_directories(current_app.config['TEMP_FOLDER_PATH'])
		for other_image in other_images:
			other_faces = list_files(os.path.join(current_app.config['TEMP_FOLDER_PATH'], other_image))
			for other_face in other_faces:
				image_a = os.path.join(known_faces_dir_path, known_face)
				image_b = os.path.join(current_app.config['TEMP_FOLDER_PATH'], other_image, other_face)

				if(calculate_face_similarity(image_a, image_b) > threshhold):
					person_id = remove_file_extension(known_face)
					person_information = {"name": known_data[person_id]["name"], "personId": person_id}
					result[other_image + ".jpg"]["present"].append(person_information)
	return result



