from flask import Blueprint, jsonify , request
import sys
from datetime import datetime
from PIL import Image
sys.path.append('../')

from models.db_helper import  add_record
from Helper.Generate_response_for_image import generate_text_response
from Helper.Save_file import save_file

image_response_routes = Blueprint('image_response_routes', __name__)

user_contexts : dict = {}

now = datetime.now()

@image_response_routes.route('/img_res', methods=['POST'])
def process_request():
    
    if request.method == "POST":
        # Check if the post request has the file part
        if "image" not in request.files:
            return jsonify({"msg": "No file part"}), 400
        
        file = request.files["image"]
        
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == "":
            return jsonify({"msg": "No selected file"}), 400
        
        user_id = request.form["user_id"]
        
        if file:

            # Set the question
            question = """<Question> : Identify the disease or plant or fruit or vegetable present in it ,explain what it is in clear.If it's a disease then explain it and provide medicine on it."""

            # Check if user id present in a user_contexts
            if user_id not in user_contexts:
                user_contexts[user_id] = []

            # Read the image via file.stream
            img = Image.open(file.stream)

            saved_file_path = save_file(file)
            file_url = request.url_root + saved_file_path

            # Get response from the gemini ai
            response = generate_text_response(img)
            answer = response

            # Save this question and answer to user_context dictionary
            user_contexts[user_id].append(
                {
                    "question": question,
                    "answer": "<Answer> :" + answer,
                    "user_id": user_id,
                    "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
                }
            )

            add_record(question, "<Answer> : " + answer, user_id, file_url, "en", "en")
            
            # You can now process the image as needed
            # For example, return the image size
            return (
                jsonify({"msg": "success", "response": answer, "img_url": file_url}),
                200,
            )
        