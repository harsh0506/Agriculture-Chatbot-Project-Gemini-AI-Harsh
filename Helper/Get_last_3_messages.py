

def get_three_messages(user_id, messages):
    # Filter messages by user_id and sort by timestamp in descending order
    user_messages = sorted(
        [msg for msg in messages if msg["user_id"] == user_id],
        key=lambda x: x["timestamp"],
        reverse=True,
    )

    # Get the last three messages
    last_three_messages = user_messages[:3]

    return last_three_messages[::-1]