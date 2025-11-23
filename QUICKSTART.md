# TIBCO BW XPath Translator - Quick Reference

## 🚀 Quick Start

### Option 1: Docker (Fastest)
```bash
docker-compose up --build
```
Access: http://localhost:3000

### Option 2: Quick Start Script
```bash
./start.sh
```

### Option 3: Manual Setup
```bash
# Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py

# Frontend (new terminal)
cd frontend
npm install
npm start
```

## 📝 Usage

1. **Upload** your TIBCO BW file (.xml, .process, .bwp)
2. **View** automatic translations in the UI
3. **Search** to find specific expressions
4. **Export** report as Markdown

## 🔌 API Examples

### Translate XPath
```bash
curl -X POST http://localhost:5000/api/translate \
  -H "Content-Type: application/json" \
  -d '{"xpath": "//Order/Customer/@id"}'
```

### Upload File
```bash
curl -X POST http://localhost:5000/api/upload \
  -F "file=@your_process.xml"
```

## 📊 Sample Translations

| XPath | Plain Language |
|-------|----------------|
| `//Order/Customer/@id` | Navigate to: order → customer → the id attribute |
| `count(//Items)` | Count the number of items |
| `$var/Amount > 1000` | Check if amount from variable 'var' is greater than 1000 |

## 🛠️ Development

### Run Tests
```bash
cd backend
python3 test_api.py
```

### Build Docker Images
```bash
docker-compose build
```

### View Logs
```bash
docker-compose logs -f
```

## 🐛 Troubleshooting

**Port 5000 in use?**
```bash
lsof -ti:5000 | xargs kill -9
```

**Frontend won't start?**
```bash
cd frontend
rm -rf node_modules
npm install
```

**Backend errors?**
```bash
cd backend
pip install -r requirements.txt
```

## 📁 Project Structure

```
my-first-project/
├── backend/          # Flask API
│   ├── app.py       # Main API
│   ├── xpath_parser.py
│   └── xpath_translator.py
├── frontend/         # React UI
│   └── src/
│       ├── App.js
│       └── App.css
└── docker-compose.yml
```

## 🌟 Features

- ✅ Drag & drop file upload
- ✅ Automatic XPath extraction
- ✅ Plain language translation
- ✅ Step-by-step breakdowns
- ✅ Confidence scoring
- ✅ Search & filter
- ✅ Markdown export
- ✅ Docker support

## 📧 Need Help?

Check the full README.md for detailed documentation!
