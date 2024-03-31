# TODO(developer): Vertex AI SDK - uncomment below & run
# pip3 install --upgrade --user google-cloud-aiplatform
# gcloud auth application-default login
from flask import Flask, request, jsonify, render_template, send_from_directory
import vertexai
from vertexai.generative_models import GenerativeModel, Part

app = Flask(__name__, template_folder='../frontend', static_folder='../frontend')

languageGlobal = None
@app.route('/generate_language', methods=['POST'])
def generate_language():
    global languageGlobal
    data = request.get_json()
    languageGlobal = data.get('language')
    # Logic to handle the language data
    # For example, you might want to save it or process it in some way

    return jsonify({"message": "Language received", "language": languageGlobal})

@app.route('/')
def home():
    # Serve the index.html file
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_text():
    global languageGlobal
    paragraph = request.form['paragraph']
    language = request.form.get('language', 'en')  # Optional: Handle language if needed

    # Initialize Vertex AI (ensure this matches your actual initialization requirements)
    vertexai.init(project="genaigenisis-2024", location="asia-southeast1")

    # Load the model
    multimodal_model = GenerativeModel("gemini-1.0-pro-vision")

    # Query the model with the paragraph
    instruction = "Translate this to "
    full_prompt = instruction + languageGlobal + ":" + paragraph  # Ensure paragraph is a straing
    response = multimodal_model.generate_content([full_prompt])


    # Send the model's response back to the frontend
    return jsonify({"response": response.text})

@app.route('/generate_emo', methods=['POST'])
def generate_text_emo():
    global languageGlobal
    paragraph = request.form['paragraph']
    language = request.form.get('language', 'en')  # Optional: Handle language if needed

    # Initialize Vertex AI (ensure this matches your actual initialization requirements)
    vertexai.init(project="genaigenisis-2024", location="asia-southeast1")

    # Load the model
    multimodal_model = GenerativeModel("gemini-1.0-pro-vision")

    # Query the model with the paragraph
    constraint = ", please do not bold any word!"
    instruction = "describe 3 emotions and tones (with explanation) insinuated in this expression : "
    full_prompt = "In" + languageGlobal + instruction + paragraph + constraint # Ensure paragraph is a straing
    response_emo = multimodal_model.generate_content([full_prompt])


    # Send the model's response back to the frontend
    # Corrected return statement for /generate_emo
    return jsonify({"response": response_emo.text})


# Route to serve static files (e.g., style.css)
@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == "__main__":
    app.run(debug=True)
