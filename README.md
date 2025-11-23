# TIBCO BW XPath to Plain Language Translator

A full-stack web application that converts complex TIBCO BusinessWorks XPath expressions into easy-to-understand plain language descriptions. Perfect for business analysts, technical writers, and anyone who needs to understand BW process logic without deep XPath knowledge.

![Application Demo](https://img.shields.io/badge/status-ready-brightgreen)
![Python](https://img.shields.io/badge/python-3.11-blue)
![React](https://img.shields.io/badge/react-18.2-blue)
![Docker](https://img.shields.io/badge/docker-ready-blue)

## 🌟 Features

- **📁 File Upload**: Support for TIBCO BW `.xml`, `.process`, and `.bwp` files
- **🔍 Smart Parsing**: Automatically extracts XPath expressions from process definitions
- **💬 Plain Language Translation**: Converts technical XPath to readable descriptions
- **📊 Step-by-Step Breakdown**: Shows detailed execution flow for complex expressions
- **🎯 Confidence Scoring**: Indicates translation accuracy (high/medium/low)
- **🔎 Search & Filter**: Quickly find specific expressions or activities
- **📄 Export Reports**: Generate Markdown documentation of all translations
- **🎨 Modern UI**: Clean, responsive interface with drag-and-drop file upload
- **🐳 Docker Ready**: One-command deployment with Docker Compose

## 🏗️ Architecture

```
┌─────────────────┐         ┌──────────────────┐
│   React         │ ◄─────► │   Flask API      │
│   Frontend      │  REST   │   Backend        │
│   (Port 3000)   │         │   (Port 5000)    │
└─────────────────┘         └──────────────────┘
                                      │
                            ┌─────────┴─────────┐
                            │                   │
                      ┌─────▼──────┐    ┌──────▼──────┐
                      │   XPath    │    │   XPath     │
                      │   Parser   │    │  Translator │
                      └────────────┘    └─────────────┘
```

**Backend Components:**
- **Flask API**: RESTful endpoints for file upload and translation
- **XPath Parser**: Extracts XPath expressions from TIBCO BW XML files
- **XPath Translator**: Converts expressions to plain language using rule-based logic

**Frontend Components:**
- **React SPA**: Modern single-page application
- **File Upload**: Drag-and-drop interface with validation
- **Results View**: Side-by-side XPath and plain language display
- **Export**: Generate downloadable Markdown reports

## 📋 Prerequisites

### Option 1: Docker (Recommended)
- Docker 20.10+
- Docker Compose 2.0+

### Option 2: Manual Setup
- Python 3.11+
- Node.js 18+
- npm or yarn

## 🚀 Quick Start with Docker

1. **Clone the repository**
```bash
cd /workspaces/my-first-project
```

2. **Start the application**
```bash
docker-compose up --build
```

3. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000/api/health

4. **Stop the application**
```bash
docker-compose down
```

## 🛠️ Manual Setup

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
python app.py
```

Backend will be available at http://localhost:5000

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

Frontend will be available at http://localhost:3000

## 📖 Usage Guide

### 1. Upload TIBCO BW File

- Drag and drop your `.xml`, `.process`, or `.bwp` file onto the upload zone
- Or click "Choose File" to browse for a file
- Maximum file size: 16MB

### 2. View Translations

Once uploaded, the application will:
- Parse the BW process file
- Extract all XPath expressions
- Translate each expression to plain language
- Display results in an organized grid

### 3. Understand Results

Each translation card shows:
- **XPath Expression**: Original technical expression
- **Plain Language**: Human-readable description
- **Location**: Where in the BW process it appears
- **Activity**: Associated BW activity name
- **Confidence**: Translation accuracy indicator
- **Steps**: Detailed breakdown (click to expand)

### 4. Search & Filter

Use the search bar to filter by:
- XPath expression content
- Plain language description
- Activity name

### 5. Export Report

Click "Export Report" to download a Markdown file containing:
- Process metadata
- All XPath expressions and translations
- Step-by-step breakdowns
- Confidence scores

## 🔌 API Documentation

### Health Check
```http
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "xpath-translator"
}
```

### Upload File
```http
POST /api/upload
Content-Type: multipart/form-data
```

**Request:**
- `file`: TIBCO BW file (.xml, .process, .bwp)

**Response:**
```json
{
  "file_id": "process_file.xml",
  "original_name": "MyProcess.process",
  "xpath_count": 15,
  "metadata": {
    "process_name": "OrderProcessing",
    "description": "Handles order workflow"
  }
}
```

### Parse & Translate
```http
GET /api/parse/{file_id}
```

**Response:**
```json
{
  "file_id": "process_file.xml",
  "metadata": { ... },
  "translations": [
    {
      "id": "uuid",
      "xpath": "//Order/Customer/@id",
      "plain_language": "Navigate to: order → customer → the id attribute",
      "location": "Mapper",
      "activity": "GetCustomerInfo",
      "steps": [
        "Step 1: Navigate to order",
        "Step 2: Navigate to customer",
        "Step 3: Access the id attribute"
      ],
      "confidence": "high"
    }
  ],
  "total_count": 15
}
```

### Translate Single XPath
```http
POST /api/translate
Content-Type: application/json
```

**Request:**
```json
{
  "xpath": "$orderData/Order/TotalAmount",
  "context": {
    "source": "ProcessData",
    "type": "variable"
  }
}
```

**Response:**
```json
{
  "xpath": "$orderData/Order/TotalAmount",
  "plain_language": "Get TotalAmount from variable 'orderData'",
  "steps": [...],
  "confidence": "high",
  "data_flow": {
    "source": "ProcessData",
    "target": "Unknown",
    "operation": "variable"
  }
}
```

## 📝 Example Translations

| XPath Expression | Plain Language Translation |
|------------------|----------------------------|
| `//Order/Customer/@id` | Navigate to: order → customer → the id attribute |
| `$var/Amount > 1000` | Check if amount from variable 'var' is greater than 1000 |
| `count(//Items/Item)` | Count the number of items item |
| `concat($firstName, ' ', $lastName)` | Combine: firstName + ' ' + lastName |
| `//Product[Price > 100]` | Navigate to: product where price is greater than 100 |

## 🧪 Testing

### Test with Sample XPath

```bash
curl -X POST http://localhost:5000/api/translate \
  -H "Content-Type: application/json" \
  -d '{
    "xpath": "//Customer[@type='premium']/Orders/Order[1]",
    "context": {}
  }'
```

### Run Backend Tests
```bash
cd backend
python -m pytest tests/
```

## 🔧 Configuration

### Environment Variables

**Backend (.env)**
```env
FLASK_ENV=development
FLASK_DEBUG=True
MAX_FILE_SIZE=16777216
UPLOAD_FOLDER=/tmp/uploads
```

**Frontend**
```env
REACT_APP_API_URL=http://localhost:5000
```

## 📦 Project Structure

```
my-first-project/
├── backend/
│   ├── app.py                 # Flask application
│   ├── xpath_parser.py        # BW file parser
│   ├── xpath_translator.py    # XPath to plain language
│   ├── requirements.txt       # Python dependencies
│   └── Dockerfile            # Backend container
├── frontend/
│   ├── src/
│   │   ├── App.js            # Main React component
│   │   ├── App.css           # Styling
│   │   └── index.js          # Entry point
│   ├── public/
│   │   └── index.html        # HTML template
│   ├── package.json          # Node dependencies
│   ├── Dockerfile            # Frontend container
│   └── nginx.conf            # Nginx configuration
├── docker-compose.yml        # Multi-container setup
└── README.md                 # This file
```

## 🎨 UI Features

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Drag & Drop**: Intuitive file upload
- **Real-time Search**: Instant filtering of results
- **Confidence Indicators**: Color-coded translation quality
- **Step-by-step Expansion**: Collapsible detailed breakdowns
- **Modern Aesthetics**: Gradient backgrounds, smooth animations
- **Dark Code Display**: Syntax-highlighted XPath expressions

## 🚀 Deployment

### Docker Compose (Production)

```bash
# Build and start in production mode
docker-compose up -d --build

# View logs
docker-compose logs -f

# Scale backend workers
docker-compose up -d --scale backend=3

# Stop services
docker-compose down
```

### Manual Production Deployment

**Backend:**
```bash
cd backend
gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 app:app
```

**Frontend:**
```bash
cd frontend
npm run build
# Serve the 'build' folder with nginx or any static server
```

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- Add support for more TIBCO BW versions
- Enhance XPath function translations
- Add support for other ESB platforms
- Implement AI-powered translations
- Add unit tests coverage
- Support for custom business terminology

## 📄 License

MIT License - feel free to use this project for personal or commercial purposes.

## 🐛 Troubleshooting

### Backend Issues

**Port 5000 already in use:**
```bash
# Find and kill the process
lsof -ti:5000 | xargs kill -9

# Or use a different port
docker-compose up -d --build -e BACKEND_PORT=5001
```

**File upload fails:**
- Check file size < 16MB
- Ensure file has correct extension (.xml, .process, .bwp)
- Verify `/tmp/uploads` directory has write permissions

### Frontend Issues

**Node modules error:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**API connection refused:**
- Verify backend is running on port 5000
- Check CORS settings in backend/app.py
- Ensure no firewall blocking

## 📞 Support

For issues or questions:
- Open an issue on GitHub
- Check existing documentation
- Review API response error messages

## 🎯 Future Enhancements

- [ ] AI-powered translation improvements
- [ ] Support for TIBCO BW6 processes
- [ ] Real-time collaboration features
- [ ] Integration with Confluence/SharePoint
- [ ] Custom business terminology dictionary
- [ ] Batch processing multiple files
- [ ] Visual process flow diagrams
- [ ] Translation confidence scoring ML model

---

**Built with ❤️ for making TIBCO BW processes understandable to everyone**
