from flask import Blueprint, jsonify, request
import sys
from datetime import datetime

sys.path.append("../")

from Helper.Text_translator_helper import convert_to_english
from models.db_helper import retrieve_last_4_records, add_record
from Helper.Get_last_3_messages import get_three_messages
from Helper.Generate_response_for_text import generate_text_response
from Helper.CONSTANTS import SYSTEM_PROMPT

text_response_routes = Blueprint("text_response_routes", __name__)

user_contexts: dict = {}

now = datetime.now()


@text_response_routes.route("/text", methods=["POST"])
def res():
    print(request.json['user_id'])
    data = {"name": "rthrt"}
    return jsonify(data)


@text_response_routes.route("/text_res", methods=["POST"])
def process_request():

    if request.method == "POST":

        data = request.get_json()

        # Validate if user_id and question are provided
        if "user_id" not in data or "question" not in data:
            return jsonify({"error": "user_id and question are required."}), 400

        question = request.json["question"]

        # Translate the question into english
        question, language = convert_to_english(question, "en")
        user_id = request.json["user_id"]

        # Check if user_id exists in user_contexts
        if user_id not in user_contexts:
            # Retrieve last 4 records
            records = retrieve_last_4_records(user_id)
            # Create new key-value pair in user_contexts
            user_contexts[user_id] = records

        # Get Last three chat message history including Question and Answer
        last_3_message_chat_history = get_three_messages(
            user_id, user_contexts[user_id]
        )

        # Convert them into string
        last_messages_string = "\n".join(
            [
                f"{text['question']} {text['answer']}"
                for text in last_3_message_chat_history
            ]
        )

        # Pass it to gemini ai for getting response , First create the question string
        question = last_messages_string + SYSTEM_PROMPT + "<Question > :" + question

        answer = generate_text_response(question=question)

        # Save this question and answer to user_context dictionary
        user_contexts[user_id].append(
            {
                "question": question,
                "answer": "<Answer> :" + answer,
                "user_id": user_id,
                "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

        answer_translated, lang = convert_to_english(answer, language)

        add_record(question, "<Answer> : " + answer, user_id, None, language, lang)

        return jsonify({"answer": answer_translated})
