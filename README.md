# 🤖 Gemini ESP32 API

A Flask API server that enables ESP32 microcontrollers to communicate with Google's Gemini AI and other large language models. Perfect for IoT applications requiring intelligent processing without on-device AI inference.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Overview

This project provides a lightweight Flask API that acts as a bridge between ESP32 devices and AI services. It supports:

- **Gemini Vision AI** - Image classification and analysis (medical waste classification, etc.)
- **Groq LLM** - Fast language model inference for Q&A
- **REST API** - Simple JSON endpoints for ESP32 devices
- **PDF Report Generation** - Export analysis results as PDF documents
- **CORS Support** - Cross-origin requests enabled for IoT devices

---

## ✨ Features

- ✅ **Multi-Model Support**: Integrates with both Gemini Vision and Groq LLM APIs
- ✅ **Image Analysis**: Classify and analyze images using Gemini AI
- ✅ **Question-Answering**: Ask natural language questions to Groq LLM
- ✅ **PDF Export**: Generate formatted PDF reports from analysis results
- ✅ **Production Ready**: Includes Gunicorn WSGI server configuration
- ✅ **Secure**: API keys loaded from environment variables
- ✅ **Easy Integration**: Simple REST endpoints for IoT devices

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key ([Get it here](https://ai.google.dev/))
- Groq API key ([Get it here](https://console.groq.com))
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/thinksarv-stack/gemini-esp32-api.git
   cd gemini-esp32-api
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   export GEMINI_API_KEY="your-gemini-api-key-here"
   export GROQ_API_KEY="your-groq-api-key-here"
   export PORT=5000
   ```
   
   Or create a `.env` file (make sure to add it to `.gitignore`):
   ```
   GEMINI_API_KEY=your-gemini-api-key-here
   GROQ_API_KEY=your-groq-api-key-here
   PORT=5000
   ```

5. **Run the server**
   ```bash
   python flask_server.py
   ```
   
   Server will start at `http://localhost:5000`

---

## 📡 API Endpoints

### 1. Health Check
**Endpoint:** `GET /`

Check if the server is running and see available endpoints.

**Response:**
```json
{
  "status": "online",
  "message": "Gemini Flask API is running!",
  "endpoints": {
    "/ask": "POST - Send question to get AI response"
  }
}
```

### 2. Ask Question (Groq LLM)
**Endpoint:** `POST /ask`

Send a question to the Groq LLM for natural language responses.

**Request:**
```json
{
  "question": "What is machine learning?"
}
```

**Response:**
```json
{
  "success": true,
  "question": "What is machine learning?",
  "answer": "Machine learning is a subset of artificial intelligence..."
}
```

### 3. Analyze Image (Gemini Vision)
**Endpoint:** `POST /` (with file upload in web interface)

Analyzes images using Gemini Vision AI. The web interface allows image upload and classification.

---

## 🏗️ Project Structure

```
gemini-esp32-api/
├── app.py                 # Gemini Vision API with web UI (image classification)
├── flask_server.py        # Main Groq LLM API server for ESP32 integration
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Web interface for image analysis
└── README.md             # This file
```

### File Descriptions

| File | Purpose |
|------|---------|
| **flask_server.py** | Main API server with `/ask` endpoint for LLM integration |
| **app.py** | Vision-focused Flask app with Gemini image classification and PDF export |
| **requirements.txt** | All Python package dependencies |

---

## 💻 Usage Examples

### Python Example (with requests)

```python
import requests

# Ask a question
response = requests.post(
    "http://localhost:5000/ask",
    json={"question": "How do I use ESP32 with AI?"}
)

print(response.json())
```

### ESP32 Example (Arduino C++)

```cpp
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

void askQuestion(const char* question) {
  HTTPClient http;
  http.begin("http://YOUR_SERVER_IP:5000/ask");
  http.addHeader("Content-Type", "application/json");
  
  String payload = "{\"question\":\"" + String(question) + "\"}";
  int httpCode = http.POST(payload);
  
  if (httpCode == HTTP_CODE_OK) {
    String response = http.getString();
    StaticJsonDocument<1024> doc;
    deserializeJson(doc, response);
    
    Serial.println("Answer: " + String((const char*)doc["answer"]));
  }
  
  http.end();
}
```

### cURL Example

```bash
curl -X POST http://localhost:5000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is IoT?"}'
```

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Google Gemini API key | Required |
| `GROQ_API_KEY` | Groq API key | Required |
| `PORT` | Server port | 5000 |
| `FLASK_ENV` | Development or production | development |

### Deployment with Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:5000 flask_server:app
```

### Docker Support (Optional)

Create a `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV GEMINI_API_KEY=""
ENV GROQ_API_KEY=""
ENV PORT=5000

EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "flask_server:app"]
```

Build and run:
```bash
docker build -t gemini-esp32-api .
docker run -e GROQ_API_KEY=your_key -p 5000:5000 gemini-esp32-api
```

---

## 📦 Dependencies

- **Flask 3.0.0** - Web framework
- **Groq** - LLM API client
- **Google Generative AI** - Gemini API integration
- **Gunicorn 21.2.0** - WSGI HTTP server for production
- **httpx 0.27.0** - HTTP client library
- **Pillow** - Image processing
- **ReportLab** - PDF generation
- **Flask-CORS** - Cross-Origin Resource Sharing support

---

## 🔐 Security Considerations

- ✅ API keys are loaded from environment variables (never hardcoded)
- ✅ Input validation on requests
- ✅ Error handling without exposing sensitive info
- ⚠️ Use HTTPS in production
- ⚠️ Rate limit the API to prevent abuse
- ⚠️ Never commit `.env` files or API keys to version control

---

## 🐛 Troubleshooting

### "GEMINI_API_KEY environment variable is not set!"

**Solution:** Make sure the environment variable is properly exported:
```bash
export GEMINI_API_KEY="your-key-here"
python flask_server.py
```

### Connection Refused (ESP32 can't reach server)

- Ensure server is running: `python flask_server.py`
- Check ESP32 and server are on the same network
- Use the correct server IP address (see output when server starts)
- Verify firewall isn't blocking port 5000

### "Failed to initialize Gemini Client"

- Verify API key is valid
- Check Gemini API is enabled in Google Cloud Console
- Ensure you have quota remaining

### "ModuleNotFoundError: No module named 'flask'"

**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

---

## 📚 Learning Resources

- [Gemini API Docs](https://ai.google.dev/)
- [Groq API Documentation](https://console.groq.com/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [ESP32 Documentation](https://docs.espressif.com/projects/esp-idf/en/latest/)

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

---

## 📄 License

This project is open source and available under the MIT License.

---

## 📧 Support

For issues and questions:
- Open an issue on [GitHub](https://github.com/thinksarv-stack/gemini-esp32-api/issues)
- Check existing issues for similar problems
- Provide detailed error messages and steps to reproduce

---

## 🌟 Acknowledgments

- Google Gemini AI for powerful vision and language models
- Groq for fast LLM inference
- Flask community for excellent documentation
- Espressif for the amazing ESP32 platform

---

**Happy coding!** 🚀
