# MirrorMind – Decision Advisor

MirrorMind is an AI-powered decision advisor application that helps users identify cognitive biases in their decisions and reflections. It uses OpenAI's GPT models to analyze user input, detect biases, simulate decision outcomes, and provide confidence scores.

## 🎯 Project Overview

MirrorMind is a web-based application that:
- Analyzes user decisions and reflections for cognitive biases
- Provides confidence scores based on bias detection
- Suggests reframing strategies to improve decision-making
- Maintains a history of all analyses in a SQLite database
- Offers a clean, intuitive user interface

---

## 📁 Folder Structure

```
MirrorMind/
├── backend/                          # Backend API and business logic
│   ├── main.py                      # FastAPI application entry point
│   ├── requirements.txt             # Python dependencies
│   └── mirrormind.db               # SQLite database (created at runtime)
│
├── frontend/                         # Frontend templates and static assets
│   └── templates/
│       ├── index.html              # Main application UI
│       └── history.html            # History page to view past analyses
│
├── .gitignore                       # Git ignore file
├── README.md                        # Project documentation
└── .env                            # Environment variables (not committed)
```

### Folder Details

- **backend/** - Contains the FastAPI server that handles API requests, interacts with OpenAI, and manages the SQLite database
- **frontend/templates/** - Contains HTML templates for the web interface
- **.venv/** - Virtual environment directory (created during setup, not tracked in git)
- **.env** - Environment file for storing API keys (create manually, never commit)

---

## 🛠️ Prerequisites

Before running the project, ensure you have:

- **Python 3.8+** installed on your system
- **pip** (Python package manager)
- **OpenAI API Key** - Get one from [OpenAI Platform](https://platform.openai.com/api-keys/)
- **Git** installed (for version control)

---

## 📋 Step-by-Step Setup and Run Guide

### Step 1: Clone the Repository

```bash
git clone https://github.com/gedizz/MirrorMind.git
cd MirrorMind
```

### Step 2: Create a Virtual Environment

Create a Python virtual environment to isolate project dependencies:

**On Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**On Windows (Command Prompt):**
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

**On macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

You should see `(.venv)` appear in your terminal prompt when activated.

### Step 3: Install Dependencies

```bash
pip install -r backend/requirements.txt
```

This installs all required packages:
- **fastapi** - Web framework for building the API
- **uvicorn** - ASGI server
- **python-dotenv** - Environment variable management
- **openai** - OpenAI API client

### Step 4: Set Up Environment Variables

Create a `.env` file in the project root directory:

**On macOS/Linux:**
```bash
touch .env
```

**On Windows PowerShell:**
```powershell
New-Item -Path .env -ItemType File
```

Open the `.env` file and add your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key_here
```

⚠️ **Important:** 
- Replace `your_openai_api_key_here` with your actual OpenAI API key
- Never commit the `.env` file to version control
- The `.env` file is listed in `.gitignore` for security

### Step 5: Run the Application

Start the FastAPI server:

```bash
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

#### Command Breakdown:
- `python -m uvicorn` - Runs the Uvicorn ASGI server
- `backend.main:app` - Points to the FastAPI app in backend/main.py
- `--reload` - Auto-restarts server when code changes (development only)
- `--host 0.0.0.0` - Allows access from any IP address
- `--port 8000` - Runs on port 8000

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started server process [XXXX]
INFO:     Waiting for application startup.
```

### Step 6: Access the Application

Open your web browser and navigate to:

```
http://localhost:8000
```

You should see the MirrorMind home page with the decision analysis form.

---

## 🎮 Using the Application

### Main Features

1. **Decision Analysis**
   - Enter a decision or reflection in the text field
   - Click "Analyze" to get bias detection and confidence scores
   - View detailed analysis including suggested reframing strategies

2. **History Page**
   - View all past analyses
   - See confidence scores and detected biases
   - Review simulation outcomes

3. **Database**
   - All analyses are automatically saved to `mirrormind.db`
   - Data persists between sessions

---

## 🔧 Troubleshooting

### Server Won't Start
- Ensure all dependencies are installed: `pip install -r backend/requirements.txt`
- Check that port 8000 is not in use
- Verify your Python version is 3.8+: `python --version`

### OpenAI API Key Error
- Verify your `.env` file exists in the project root
- Check that your API key is correctly set: `OPENAI_API_KEY=sk-...`
- Ensure your OpenAI account has API credits available

### Database Errors
- The `mirrormind.db` file is created automatically on first run
- If corrupted, delete it and restart the server to recreate it

### Port Already in Use
- Use a different port: `python -m uvicorn backend.main:app --reload --port 8001`

### Virtual Environment Issues
- On Windows, if you get an execution policy error, run: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned`
- Make sure you're in the project directory before activating venv

---

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| fastapi | Latest | Web framework for building the API |
| uvicorn | Latest | ASGI web server |
| python-dotenv | Latest | Load environment variables from .env |
| openai | Latest | OpenAI API client library |

---

## 🔐 Security Notes

- Never commit `.env` file to version control
- Keep your OpenAI API key secret
- In production, use environment variables or secure vaults instead of `.env` files
- Consider adding authentication for deployment
- Rotate API keys periodically

---

## 🚀 Deployment

For production deployment:

1. Set `--reload` to False
2. Use a production ASGI server like Gunicorn or Hypercorn
3. Set appropriate host and port
4. Use environment variables for configuration
5. Enable HTTPS/SSL certificates
6. Set up proper logging and monitoring

Example production command:
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## 📝 Database Structure

The SQLite database automatically creates a `history` table with the following columns:

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key (auto-increment) |
| timestamp | TEXT | When the analysis was performed |
| user_input | TEXT | The decision or reflection analyzed |
| analysis | TEXT | Detected biases and analysis |
| simulation | TEXT | Decision outcome simulation |
| confidence_score | REAL | Confidence score (0-100) |
| confidence_reason | TEXT | Explanation for confidence score |
| mood | TEXT | Detected mood/emotional state |

---

## 🤝 Contributing

To contribute to this project:

1. Create a new branch: `git checkout -b feature/your-feature`
2. Make your changes
3. Commit: `git commit -m "Add your feature"`
4. Push: `git push origin feature/your-feature`
5. Create a Pull Request on GitHub

---

## 📄 License

[Add your license information here]

---

## 📧 Support

For issues or questions, please create an issue in the GitHub repository:
https://github.com/gedizz/MirrorMind/issues

---

## 🎓 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Uvicorn Documentation](https://www.uvicorn.org/)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)

---

## ✨ Quick Reference

**Activate Virtual Environment:**
```bash
# Windows
.\.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate
```

**Start Server:**
```bash
python -m uvicorn backend.main:app --reload --port 8000
```

**Install Dependencies:**
```bash
pip install -r backend/requirements.txt
```

**Deactivate Virtual Environment:**
```bash
deactivate
```

---

**Happy Decision Making! 🧠✨**
