import os
import json
import shutil

def extract_filename_without_extension(file_path):
    # Use os.path.basename to get the filename with extension
    file_name_with_extension = os.path.basename(file_path)

    # Use os.path.splitext to split the filename and extension
    file_name, file_extension = os.path.splitext(file_name_with_extension)

    return file_name





def list_files(directory):
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]




def list_directories(directory):
    return [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]



def write_dict_to_json(data_dict, file_path):
    try:
        with open(file_path, 'w') as json_file:
            json.dump(data_dict, json_file, indent=4)
        print(f"Dictionary written to {file_path} successfully.")
    except Exception as e:
        print(f"Error writing dictionary to {file_path}: {e}")


def read_json_to_dict(file_path):
    try:
        with open(file_path, 'r') as json_file:
            data_dict = json.load(json_file)
            return data_dict
    except Exception as e:
        print(f"Error reading dictionary from {file_path}: {e}")
        return None



def copy_file(source_path, destination_path):
    try:
        shutil.copy(source_path, destination_path)
        print(f"File copied from {source_path} to {destination_path} successfully.")
    except Exception as e:
        print(f"Error copying file from {source_path} to {destination_path}: {e}")


def remove_file_extension(file_path):
    filename, file_extension = os.path.splitext(file_path)
    return filename




def delete_files_in_directory(directory_path):
    try:
        # Get the list of files in the directory
        file_list = os.listdir(directory_path)

        # Iterate over the files and delete each one
        for file_name in file_list:
            file_path = os.path.join(directory_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted: {file_path}")

        print(f"All files in {directory_path} have been deleted.")
    except Exception as e:
        print(f"Error: {e}")


def delete_items_in_directory(directory_path, delete_files=True, delete_folders=True):
    try:
        # Get the list of items in the directory
        items_list = os.listdir(directory_path)

        # Iterate over the items and delete each based on the specified criteria
        for item_name in items_list:
            item_path = os.path.join(directory_path, item_name)

            if delete_files and os.path.isfile(item_path):
                os.remove(item_path)
                print(f"Deleted file: {item_path}")

            if delete_folders and os.path.isdir(item_path):
                shutil.rmtree(item_path)
                print(f"Deleted folder: {item_path}")

        print(f"All items in {directory_path} have been deleted.")
    except Exception as e:
        print(f"Error: {e}")
