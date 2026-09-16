from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
import tabula
import io
import os

app = FastAPI(title="Indian Tax Optimizer PDF Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health():
    return {"status": "ok", "service": "pdf-extraction"}

@app.post("/extract")
async def extract_pdf(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        pdf_file = io.BytesIO(contents)
        
        text_content = ""
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    text_content += text + "\n"
                    
        tables = []
        try:
            pdf_file.seek(0)
            tables = tabula.read_pdf(pdf_file, pages='all', multiple_tables=True)
            tables = [df.to_dict('records') for df in tables]
        except Exception:
            tables = []
            
        doc_type = "unknown"
        if "Form 16" in text_content:
            doc_type = "form16"
        elif "AIS" in text_content:
            doc_type = "ais"
            
        return {
            "success": True,
            "docType": doc_type,
            "textContent": text_content[:10000],
            "tables": tables[:10],
            "confidence": 0.7,
            "warnings": ["Full extraction logic to be implemented"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
.python-version (Required for Streamlit Cloud compatibility)
If you deploy on Streamlit Cloud, create a file named .python-version in the root folder with this single line:
3.10
Quick Shell Script to Auto-Generate Files
Run this in your local terminal inside your repository directory
:
cat > README.md << 'EOF'
# Indian Tax Optimizer
Household balance-sheet tax optimization engine for India (Old vs New regime, HUF routing, tax-loss harvesting, 54F/54EC rollovers).

## Architecture
- **Frontend**: Next.js (TypeScript) → GitHub Pages
- **API**: Cloudflare Workers (Hono)
- **PDF Service**: Python (FastAPI) on Render
- **Database**: MongoDB Atlas M0
- **Auth**: Email magic link

## Quick Start
### 1. MongoDB Atlas
- Create M0 cluster at https://cloud.mongodb.com
- Get connection string: `mongodb+srv://...`
- Create database: `taxopt`

### 2. Cloudflare Workers
```bash
cd worker
npm install
wrangler login
npm run deploy
3. PDF Service (Render)
Deploy pdf-service/ to Render
Build: pip install -r requirements.txt
Start: uvicorn app:app --host 0.0.0.0 --port $PORT
4. Frontend (GitHub Pages)
cd frontend
npm install
npm run build
# Deploy dist/ to gh-pages
Docs
docs/SETUP.md - Detailed setup guide
docs/SAMPLE_PAYLOADS.json - Example payloads
License
MIT EOF
cat > requirements.txt << 'EOF' fastapi==0.111.1 uvicorn[standard]==0.30.1 python-multipart==0.0.9 pymongo==4.8.0 pdfplumber==0.11.2 tabula-py==2.9.3 camelot-py[cv]==0.11.0 pandas==2.2.2 EOF
cat > .python-version << 'EOF' 3.10 EOF
cat > app.py << 'EOF' from fastapi import FastAPI, File, UploadFile, HTTPException from fastapi.middleware.cors import CORSMiddleware import pdfplumber import tabula import io import os
app = FastAPI(title="Indian Tax Optimizer PDF Service")
app.add_middleware( CORSMiddleware, allow_origins=[""], allow_credentials=True, allow_methods=[""], allow_headers=["*"], )
@app.get("/") def health(): return {"status": "ok", "service": "pdf-extraction"}
@app.post("/extract") async def extract_pdf(file: UploadFile = File(...)): try: contents = await file.read() pdf_file = io.BytesIO(contents)
    text_content = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                text_content += text + "\n"
                
    tables = []
    try:
        pdf_file.seek(0)
        tables = tabula.read_pdf(pdf_file, pages='all', multiple_tables=True)
        tables = [df.to_dict('records') for df in tables]
    except Exception:
        tables = []
        
    doc_type = "unknown"
    if "Form 16" in text_content:
        doc_type = "form16"
    elif "AIS" in text_content:
        doc_type = "ais"
        
    return {
        "success": True,
        "docType": doc_type,
        "textContent": text_content[:10000],
        "tables": tables[:10],
        "confidence": 0.7,
        "warnings": ["Full extraction logic to be implemented"]
    }
except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
if name == "main": import uvicorn port = int(os.getenv("PORT", 8000)) uvicorn.run(app, host="0.0.0.0", port=port) EOF
git add . git commit -m "Fix requirements formatting, app syntax, and python ABI version" git push origin main