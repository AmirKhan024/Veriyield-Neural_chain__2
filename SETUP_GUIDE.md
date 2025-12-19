# VeriYield Neural-Chain - Setup Instructions

## Quick Start Guide

### 1. Install Dependencies

```powershell
cd "C:\Users\Amir Khan\Desktop\GenAI\VeriYield-Neural-Chain"
pip install -r requirements.txt
```

### 2. Configure Environment Variables

The `.env.example` already contains your Groq API key. Copy it to `.env`:

```powershell
Copy-Item .env.example .env
```

**Note**: Only Groq API is required. The app automatically falls back to mock mode if the API fails.

### 3. Run the Application

```powershell
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Automatic Fallback Mode

The app automatically uses Groq API for vision analysis. If the API is unavailable or fails:
- It automatically falls back to mock mode
- Upload any image with keywords like "tomato", "blight", "wheat", "rust" in the filename
- The mock AI will provide realistic responses based on filename patterns

## Project Structure

```
VeriYield-Neural-Chain/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment template
├── data/
│   ├── mock_weather.json          # Mock weather data for Nashik
│   ├── mock_market.json           # Mock market prices
│   └── treatment_docs/
│       ├── tomato_early_blight.txt
│       ├── tomato_late_blight.txt
│       └── wheat_rust.txt
├── sample_images/                  # Sample disease images
├── utils/
│   ├── vision_ai.py               # GPT-4o vision integration
│   ├── rag_system.py              # RAG for treatment retrieval
│   └── blockchain.py              # Polygon blockchain integration
└── README.md
```

## Features Implemented (Day 1)

✅ **Basic Setup**
- Project structure created
- Minimal dependencies (Streamlit, Groq, Pillow)
- Mock data prepared

✅ **Core AI Vision**
- Groq Llama-3.2 Vision (90B) for disease detection
- Automatic fallback to mock mode
- Multi-language support (English, Hindi, Marathi)

✅ **Streamlit UI**
- Farmer Dashboard with image upload
- Buyer Dashboard with supply chain overview
- Weather forecast display (5-day)
- Market prices display (Vashi APMC)
- Weather alerts

✅ **RAG System**
- Treatment document retrieval
- Immediate action extraction
- Structured treatment display for 3 diseases

## Testing the App

### Test Scenario 1: Disease Detection
1. Go to Farmer Dashboard
2. Upload an image (any image works, or use filename like "tomato_blight.jpg")
3. Click "Analyze Disease"
4. View AI analysis results
5. See treatment recommendations from RAG system

### Test Scenario 2: Supply Chain View
1. Go to Buyer Dashboard
2. View supply chain routes (Nashik → Vashi APMC)
3. See market insights and price trends
4. Check analysis history

## Next Steps (Day 2)

- [ ] Integrate Groq (Llama-3) for smart recommendations
- [ ] Add weather-based advice generation
- [ ] Implement route optimization logic
- [ ] Create supply chain dashboard with maps

## Troubleshooting

### Import Errors
```powershell
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Streamlit Not Found
```powershell
pip install streamlit
```

### Port Already in Use
```powershell
streamlit run app.py --server.port 8502
```

## Tips for Hackathon Demo

1. **Pre-load everything**: Test all features before demo
2. **Use Demo Mode**: Reduces API failures during presentation
3. **Prepare "Happy Path"**: Know exactly which buttons to click
4. **Have backup screenshots**: In case app crashes
5. **Practice the pitch**: Focus on the 3 pillars (Vision, AI, Blockchain)

## Support

For issues or questions:
- Check the code comments
- Review error messages in terminal
- Test with Demo Mode first
- Verify all dependencies are installed
