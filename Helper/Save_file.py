import os
import uuid


def save_file(file, upload_folder : str = "img/"):
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    filename = str(uuid.uuid4()) + "." + file.filename.split(".")[-1]
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)
    return file_path
