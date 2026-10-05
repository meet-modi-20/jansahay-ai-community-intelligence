import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

from analytics.priority_engine import calculate_priority
from gemini.analyzer import analyze_issue

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "jansahay.db"
app = Flask(__name__)


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS issues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            latitude REAL,
            longitude REAL,
            image_base64 TEXT,
            category TEXT,
            severity TEXT,
            context TEXT,
            impact INTEGER,
            recommended_action TEXT,
            status TEXT DEFAULT 'Reported',
            department TEXT,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def seed_demo_data():
    conn = get_db()
    count = conn.execute("SELECT COUNT(*) FROM issues").fetchone()[0]
    if count:
        conn.close()
        return

    records = json.loads(
        (BASE_DIR / "data" / "demo_issues.json").read_text(encoding="utf-8")
    )

    for item in records:
        conn.execute("""
            INSERT INTO issues
            (text, latitude, longitude, category, severity, context, impact,
             recommended_action, status, department, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item["text"], item["latitude"], item["longitude"],
            item["category"], item["severity"], item["context"],
            item["impact"], item["recommended_action"], item["status"],
            item["department"], item["created_at"]
        ))
    conn.commit()
    conn.close()


@app.get("/")
def index():
    return render_template(
        "index.html",
        maps_key=os.getenv("GOOGLE_MAPS_API_KEY", "")
    )


@app.get("/api/issues")
def issues():
    conn = get_db()
    rows = conn.execute("SELECT * FROM issues ORDER BY id DESC").fetchall()
    conn.close()

    data = []
    for row in rows:
        item = dict(row)
        item["priority_score"] = calculate_priority(item)
        data.append(item)

    data.sort(key=lambda x: x["priority_score"], reverse=True)
    return jsonify(data)


@app.post("/api/issues")
def create_issue():
    payload = request.get_json(silent=True) or {}
    text = (payload.get("text") or "").strip()

    if not text:
        return jsonify({"error": "Please describe the issue."}), 400

    analysis = analyze_issue(
        text=text,
        image_base64=payload.get("image_base64"),
        latitude=payload.get("latitude"),
        longitude=payload.get("longitude"),
    )

    now = datetime.now(timezone.utc).isoformat()

    conn = get_db()
    cursor = conn.execute("""
        INSERT INTO issues
        (text, latitude, longitude, image_base64, category, severity, context,
         impact, recommended_action, status, department, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'Reported', '', ?)
    """, (
        text, payload.get("latitude"), payload.get("longitude"),
        payload.get("image_base64"), analysis["category"],
        analysis["severity"], analysis["context"], analysis["impact"],
        analysis["recommended_action"], now
    ))
    conn.commit()
    issue_id = cursor.lastrowid
    conn.close()

    return jsonify({
        "id": issue_id,
        "analysis": analysis,
        "demo_mode": not bool(os.getenv("GEMINI_API_KEY"))
    }), 201


@app.patch("/api/issues/<int:issue_id>")
def update_issue(issue_id):
    payload = request.get_json(silent=True) or {}
    allowed_status = {"Reported", "Assigned", "In Progress", "Resolved"}
    status = payload.get("status")
    department = payload.get("department", "")

    if status not in allowed_status:
        return jsonify({"error": "Invalid status."}), 400

    conn = get_db()
    result = conn.execute(
        "UPDATE issues SET status=?, department=? WHERE id=?",
        (status, department, issue_id)
    )
    conn.commit()
    conn.close()

    if result.rowcount == 0:
        return jsonify({"error": "Issue not found."}), 404

    return jsonify({"ok": True})


@app.get("/api/summary")
def summary():
    conn = get_db()
    rows = conn.execute("SELECT * FROM issues").fetchall()
    conn.close()

    records = [dict(r) for r in rows]
    categories = {}
    for r in records:
        categories[r["category"]] = categories.get(r["category"], 0) + 1

    return jsonify({
        "total": len(records),
        "high_priority": sum(
            1 for r in records if r["severity"] in {"HIGH", "CRITICAL"}
        ),
        "resolved": sum(1 for r in records if r["status"] == "Resolved"),
        "categories": categories
    })


if __name__ == "__main__":
    init_db()
    seed_demo_data()
    app.run(debug=True)
