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
MIT
