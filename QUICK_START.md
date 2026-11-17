# DecisionMirror - Quick Start Guide

## 🚀 Get Started in 3 Minutes

### Prerequisites
- ✅ Docker Desktop (running)
- ✅ Git

---

## Step 1: Start the Application

```powershell
# Windows PowerShell:
.\scripts\setup.ps1

# Or manually:
docker-compose up -d
```

**Wait ~30 seconds for services to start**

---

## Step 2: Access the Application

Open your browser:

### 🌐 Frontend
http://localhost:5173

### 🔌 API
http://localhost:8000

### 📚 API Documentation
http://localhost:8000/docs

---

## Step 3: Try It Out!

1. Go to http://localhost:5173
2. Click **"Start a Decision"**
3. Fill in the decision form
4. Create your first decision!

---

## ✅ Verify Everything Works

```powershell
# Check containers
docker ps

# Should show 3 running containers:
# - decisionmirror-frontend (port 5173)
# - decisionmirror-api (port 8000)
# - decisionmirror-db (port 5432)

# Test API health
curl http://localhost:8000/api/v1/health

# Expected: {"status":"healthy","database":"connected"}
```

---

## 📝 Common Commands

```powershell
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Restart a service
docker-compose restart api

# Check database
docker-compose exec db psql -U decisionmirror -d decisionmirror
```

---

## 🛠️ Development Mode

### Backend Development
```powershell
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Development
```powershell
cd frontend
npm install
npm run dev
```

---

## 📚 Documentation

- **README.md** - Full project documentation
- **IMPLEMENTATION_SUMMARY.md** - What was built
- **NEXT_STEPS.md** - Continue development guide
- **SELF_TEST_RESULTS.md** - Test results
- **docs/GETTING_STARTED.md** - Detailed setup guide

---

## 🐛 Troubleshooting

### Ports Already in Use
```powershell
# Stop conflicting services or change ports in docker-compose.yml
```

### Docker Not Running
```powershell
# Start Docker Desktop first
```

### Database Connection Error
```powershell
# Wait a few seconds for PostgreSQL to initialize
docker-compose logs db
```

---

## 🎯 What's Next?

After setup, implement:

1. **Reasoning Engine** - Graph validator & claim evaluator
2. **LLM Integration** - AI decomposition
3. **Graph Visualization** - React Flow
4. **Scenario Testing** - Stress test assumptions

See **NEXT_STEPS.md** for detailed roadmap.

---

## 🆘 Need Help?

- Check `docs/` for detailed guides
- Review `SELF_TEST_RESULTS.md` for known issues
- See error logs: `docker-compose logs -f`

---

**That's it! You're ready to build DecisionMirror! 🎉**

*Built with Kiro for Kiroween 2026* 🎃
