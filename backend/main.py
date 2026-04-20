import os
import sqlite3
from datetime import datetime
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from openai import OpenAI, OpenAIError
from dotenv import load_dotenv
import json

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

app = FastAPI()
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../frontend/templates"))
templates = Jinja2Templates(directory=template_dir)

DB_PATH = "mirrormind.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            user_input TEXT,
            analysis TEXT,
            simulation TEXT,
            confidence_score REAL,
            confidence_reason TEXT,
            mood TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Helper functions

def detect_bias_and_confidence(user_input: str) -> dict:
    prompt = f"""
    Analyze the following decision or reflection:

    "{user_input}"

    1. Identify any cognitive biases.
    2. Give a short explanation.
    3. Suggest a nudge to reframe thinking.
    4. Estimate a confidence score (0-100) for how strongly you detect these biases.
    5. Explain why you gave this confidence score.
    6. Classify the overall mood (Positive, Negative, Neutral) of the statement.

    Respond in JSON with keys: biases, explanation, suggestion, confidence, confidence_reason, mood.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
    except OpenAIError as e:
        return {"error": f"OpenAI error: {str(e)}"}
    except Exception as e:
        return {"error": f"OpenAI request failed: {str(e)}"}

    try:
        return json.loads(response.choices[0].message.content)
    except Exception:
        return {
            "biases": ["Parsing Error"],
            "explanation": "Could not parse GPT output.",
            "suggestion": "",
            "confidence": 0,
            "confidence_reason": "Parsing error, no explanation.",
            "mood": "Unknown"
        }

def simulate_decision(user_input: str) -> dict:
    prompt = f"""
    A user described the following decision: "{user_input}"

    Simulate:
    - Biased Decision Path
    - Unbiased Decision Path
    - Insight

    Respond in JSON with keys: biased_path, unbiased_path, insight.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
    except OpenAIError as e:
        return {"error": f"OpenAI error: {str(e)}"}
    except Exception as e:
        return {"error": f"OpenAI request failed: {str(e)}"}

    try:
        return json.loads(response.choices[0].message.content)
    except Exception:
        return {
            "biased_path": "Error parsing simulation.",
            "unbiased_path": "",
            "insight": ""
        }

def predict_advice_outcome(user_input: str) -> dict:
    prompt = f"""
    The user has just taken this advice related to their decision:

    "{user_input}"

    Predict the expected improvement, new confidence score (0-100), and explain why.

    Respond in JSON with keys: expected_improvement, new_confidence, reasoning.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
    except OpenAIError as e:
        return {"error": f"OpenAI error: {str(e)}"}
    except Exception as e:
        return {"error": f"OpenAI request failed: {str(e)}"}

    try:
        return json.loads(response.choices[0].message.content)
    except Exception:
        return {
            "expected_improvement": "Prediction parsing error.",
            "new_confidence": 0,
            "reasoning": "Parsing error, no reasoning."
        }

def save_history(user_input: str, analysis: str, simulation: str, confidence: float, confidence_reason: str, mood: str):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        INSERT INTO history (timestamp, user_input, analysis, simulation, confidence_score, confidence_reason, mood)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (datetime.now().isoformat(), user_input, analysis, simulation, confidence, confidence_reason, mood))
    conn.commit()
    conn.close()

def get_mood_trend() -> str:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT mood FROM history ORDER BY timestamp DESC LIMIT 10")
    moods = [row[0] for row in cur.fetchall()]
    conn.close()

    from collections import Counter
    mood_count = Counter(moods)
    if not moods:
        return "No data yet"
    most_common = mood_count.most_common(1)[0][0]
    return f"Recent mood trend: {most_common} ({mood_count[most_common]} of last {len(moods)})"

# Routes

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/analyze")
async def api_analyze(data: dict):
    user_input = data.get("user_input", "").strip()
    if not user_input:
        return JSONResponse({"error": "Input is empty"}, status_code=400)

    analysis_data = detect_bias_and_confidence(user_input)
    if analysis_data.get("error"):
        return JSONResponse({"error": analysis_data["error"]}, status_code=502)

    save_history(
        user_input=user_input,
        analysis=json.dumps(analysis_data, ensure_ascii=False),
        simulation="",
        confidence=analysis_data.get("confidence", 0),
        confidence_reason=analysis_data.get("confidence_reason", ""),
        mood=analysis_data.get("mood", "Unknown")
    )
    return {
        "analysis": analysis_data,
        "mood_trend": get_mood_trend()
    }

@app.post("/api/simulate")
async def api_simulate(data: dict):
    user_input = data.get("user_input", "").strip()
    if not user_input:
        return JSONResponse({"error": "Input is empty"}, status_code=400)

    sim_data = simulate_decision(user_input)
    if sim_data.get("error"):
        return JSONResponse({"error": sim_data["error"]}, status_code=502)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id FROM history ORDER BY id DESC LIMIT 1")
    last_id = cur.fetchone()
    if last_id:
        conn.execute("UPDATE history SET simulation=? WHERE id=?", (json.dumps(sim_data, ensure_ascii=False), last_id[0]))
        conn.commit()
    conn.close()

    return {"simulation": sim_data}

@app.post("/api/take_advice")
async def api_take_advice(data: dict):
    user_input = data.get("user_input", "").strip()
    if not user_input:
        return JSONResponse({"error": "Input is empty"}, status_code=400)

    prediction_data = predict_advice_outcome(user_input)
    if prediction_data.get("error"):
        return JSONResponse({"error": prediction_data["error"]}, status_code=502)

    return {"prediction": prediction_data}

@app.get("/history", response_class=HTMLResponse)
async def view_history(request: Request):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT id, timestamp, user_input, analysis, simulation, confidence_score, confidence_reason, mood
        FROM history
        ORDER BY timestamp DESC
    """)
    rows = cur.fetchall()
    conn.close()

    history_list = []
    for row in rows:
        history_list.append({
            "id": row[0],
            "timestamp": row[1],
            "user_input": row[2],
            "analysis": row[3],
            "simulation": row[4],
            "confidence": row[5],
            "confidence_reason": row[6],
            "mood": row[7]
        })

    return templates.TemplateResponse("history.html", {"request": request, "history": history_list})

@app.delete("/api/history/{entry_id}")
async def delete_history_entry(entry_id: int):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id FROM history WHERE id = ?", (entry_id,))
    if not cur.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Entry not found")

    conn.execute("DELETE FROM history WHERE id = ?", (entry_id,))
    conn.commit()
    conn.close()
    return {"message": "Entry deleted"}
