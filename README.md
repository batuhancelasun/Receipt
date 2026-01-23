# Receipt - AI-Powered Expense Tracker

A self-hosted income/expense tracking application with AI-powered receipt scanning using Gemini 2.0 Flash.

## Features

✨ **AI Receipt Scanning** - Automatically extract transaction data from receipt images using Gemini 2.0 Flash  
📊 **Analytics Dashboard** - Beautiful pie charts and statistics (daily/monthly/yearly)  
🌓 **Dark/Light Theme** - Premium glassmorphism UI with theme switching  
💱 **Multi-Currency** - Configurable currency symbols (€, $, £, ₺, ¥)  
🔒 **Secure Authentication** - JWT-based user authentication  
🐳 **Single Docker Image** - Easy deployment with docker-compose  
⚡ **Low Resource Usage** - Optimized for minimal system consumption  

## Tech Stack

- **Frontend**: Vue 3 + Vite + Tailwind CSS
- **Backend**: FastAPI (Python)
- **Database**: MongoDB
- **AI**: Google Gemini 2.0 Flash
- **Charts**: Chart.js
- **Deployment**: Docker + GitHub Actions

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Gemini API Key ([Get one here](https://makersuite.google.com/app/apikey))

### Deployment

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/receipt-tracker.git
   cd receipt-tracker
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env and set JWT_SECRET_KEY
   ```

3. **Run with Docker Compose**
   ```bash
   docker-compose up -d
   ```

4. **Access the application**
   - Open http://localhost:8000
   - Register a new account
   - Go to Settings and add your Gemini API key

### Using Pre-built Image from DockerHub

```bash
# Pull the latest image
docker pull batubaba619/receipt:latest

# Run with docker-compose
docker-compose up -d
```

## Configuration

### Gemini API Key

1. Navigate to Settings in the app
2. Enter your Gemini 2.0 Flash API key
3. Start scanning receipts!

### Currency

Change the default currency symbol in Settings. Supported:
- € Euro
- $ US Dollar
- £ Pound Sterling
- ₺ Turkish Lira
- ¥ Yen/Yuan

## Development

### Local Development

#### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Building Locally

```bash
# Build the Docker image
docker build -t receipt-tracker .

# Run locally
docker-compose up
```

## Architecture

The application uses a **unified single-image architecture**:

1. **Multi-stage Dockerfile**:
   - Stage 1: Build Vue.js frontend with Vite
   - Stage 2: Install Python dependencies
   - Stage 3: Combine into single production image

2. **FastAPI serves everything**:
   - `/` → Vue.js SPA
   - `/api/*` → REST API endpoints

3. **Only 2 Docker services**:
   - `app`: Unified Vue + FastAPI container
   - `mongodb`: Database

## API Endpoints

### Authentication
- `POST /api/auth/register` - Create account
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Get current user

### Receipts
- `POST /api/receipts/scan` - Scan receipt image
- `GET /api/receipts/` - List scanned receipts
- `GET /api/receipts/{id}` - Get receipt details

### Transactions
- `POST /api/transactions/` - Create transaction
- `GET /api/transactions/` - List transactions (with filters)
- `GET /api/transactions/{id}` - Get transaction
- `PUT /api/transactions/{id}` - Update transaction
- `DELETE /api/transactions/{id}` - Delete transaction
- `GET /api/transactions/analytics/{period}` - Get analytics

### Settings
- `GET /api/settings/` - Get user settings
- `PUT /api/settings/` - Update settings
- `GET /api/settings/categories` - List categories
- `POST /api/settings/categories` - Create category

## GitHub Actions CI/CD

The repository includes automated Docker builds:

1. Push code to `main` branch
2. GitHub Actions automatically builds the Docker image
3. Image is pushed to DockerHub as `batubaba619/receipt:latest`
4. Pull the updated image and restart containers

### Setup GitHub Actions

Add `DOCKERHUB_TOKEN` to your repository secrets:
1. Go to repository Settings → Secrets
2. Add `DOCKERHUB_TOKEN` with your DockerHub access token

## Resource Usage

The application is optimized for low resource consumption:
- **CPU Limit**: 1.0 cores
- **Memory Limit**: 512MB
- **CPU Reservation**: 0.25 cores
- **Memory Reservation**: 256MB

Perfect for running on small VPS or home servers!

## License

MIT License - feel free to use for personal or commercial projects.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues or questions, please open an issue on GitHub.

---

Made with ❤️ using Vue 3, FastAPI, and Gemini AI
