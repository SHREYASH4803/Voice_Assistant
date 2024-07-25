from flask import Flask, request, jsonify, render_template
import os
import csv
from dotenv import load_dotenv
from groq import Groq

app = Flask(__name__)

load_dotenv()

client = Groq()

data = {}


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    target_language = request.json.get('language')

    try:
    
        response_text = process_query(user_input)
        
        if not response_text:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": user_input,
                    }
                ],
                model="gemma2-9b-it",
            )
            response_text = chat_completion.choices[0].message.content
                        
            if not response_text.strip():
                response_text = "Sorry, I don't have a response for that."
        
        
        if target_language != 'en':
            translation = translate_text(response_text, target_language)
            response_text = translation
        
        return jsonify({'response': response_text})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def process_query(input_text):
    max_query_length = 500  
    responses = []

    while input_text:
        query_chunk = input_text[:max_query_length]
        input_text = input_text[max_query_length:]
        
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": query_chunk}],
            model="gemma2-9b-it"
        )
        response_text = chat_completion.choices[0].message.content
        responses.append(response_text)

    return ' '.join(responses)

def translate_text(text, target_language):
    
    return text

if __name__ == '__main__':
    app.run(debug=True)
