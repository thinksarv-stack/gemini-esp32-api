from flask import Flask, request, jsonify
import google.generativeai as genai
import os

# Configure the API key from environment variable (for deployment)
API_KEY = os.environ.get('GEMINI_API_KEY', 'YOUR_API_KEY_HERE')
genai.configure(api_key=API_KEY)

# Initialize the model
model = genai.GenerativeModel('models/gemini-2.5-flash')

# Create Flask app
app = Flask(__name__)

# Route to check if server is running
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'status': 'online',
        'message': 'Gemini Flask API is running!',
        'endpoints': {
            '/ask': 'POST - Send question to get AI response'
        }
    })

# Route to ask questions
@app.route('/ask', methods=['POST'])
def ask_question():
    try:
        # Get question from request
        data = request.get_json()
        
        if not data or 'question' not in data:
            return jsonify({
                'success': False,
                'error': 'No question provided. Send JSON with "question" field.'
            }), 400
        
        question = data['question']
        print(f"\n[Question received]: {question}")
        
        # Generate response from Gemini
        response = model.generate_content(question)
        answer = response.text
        
        print(f"[Answer generated]: {answer[:100]}...")  # Print first 100 chars
        
        # Return response
        return jsonify({
            'success': True,
            'question': question,
            'answer': answer
        })
        
    except Exception as e:
        print(f"[Error]: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Run the server
if __name__ == '__main__':
    import socket
    
    # Get server's IP address (for local testing)
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        print(f"\n🌐 Local IP: {local_ip}")
    except:
        local_ip = "localhost"
    
    print("=" * 60)
    print("Starting Gemini Flask API Server...")
    print("=" * 60)
    print(f"📱 ESP32 should connect to: http://{local_ip}:5000/ask")
    print("\nEndpoints:")
    print("  GET  /        - Check server status")
    print("  POST /ask     - Ask a question")
    print("\n" + "=" * 60)
    
    # Get port from environment variable (for deployment) or use 5000
    port = int(os.environ.get('PORT', 5000))
    
    # Run on all network interfaces so ESP32 can access it
    app.run(host='0.0.0.0', port=port, debug=False)