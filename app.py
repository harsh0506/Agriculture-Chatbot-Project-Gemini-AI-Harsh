# Import necessary modules
from flask import Flask
from dotenv import load_dotenv
from flask_cors import CORS
from routes.TextResponse import text_response_routes
from routes.ImageRespose import image_response_routes

# Load environment variables from a .env file
load_dotenv()

# Create a Flask app instance
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS) to allow requests from other origins
CORS(app)

# Register blueprints for text response routes
app.register_blueprint(text_response_routes)

# Register blueprints for image response routes
app.register_blueprint(image_response_routes)

# This block ensures that the Flask app only runs if this script is executed directly
if __name__ == "__main__":
    # Run the Flask app in debug mode
    app.run(debug=True)
