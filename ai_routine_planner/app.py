from flask import Flask, render_template, request, jsonify
import sqlite3, os, json

app = Flask(__name__)

# ============================================================
# DATABASE SETUP
# ============================================================
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "feedback.db")
if not os.path.exists(DB_NAME):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""CREATE TABLE feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    activities TEXT,
                    schedule TEXT,
                    feedback TEXT
                )""")
    conn.commit()
    conn.close()


# ============================================================
# MAIN ROUTES
# ============================================================
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    if not data or 'tasks' not in data:
        return jsonify({"error": "No tasks provided"}), 400

    user_input = [t.lower().strip() for t in data['tasks'] if t.strip()]
    if len(user_input) < 4:
        return jsonify({"error": "Please enter at least 4 activities for better accuracy."})

    # ============================================================
    # KEYWORD CATEGORIES
    # ============================================================
    school = ["school", "student", "class", "homework", "exam", "study", "child"]
    college = ["college", "campus", "lecture", "assignment", "btech", "engineering", "mba", "university", "project"]
    work = ["work", "office", "job", "meeting", "startup", "career", "company", "employee", "boss"]
    gym = ["gym", "workout", "fitness", "exercise", "training", "health"]
    retired = ["retired", "old", "senior", "elder", "pension", "grandparent"]
    coaching = ["coaching", "neet", "jee", "upsc", "ssc", "bank", "exam", "academy"]
    freelancing = ["freelance", "client", "project", "remote", "coding", "design"]
    creative = ["art", "painting", "music", "dance", "video", "content", "creator", "editing", "shoot"]
    lazy = ["rest", "sleep", "chill", "relax", "binge", "tv"]
    housewife = ["housewife", "homemaker", "mother", "mom", "cooking", "cleaning", "laundry", "shopping"]
    athlete = ["athlete", "sports", "training", "practice", "match", "running", "fitness"]
    shift_worker = ["night shift", "shift", "guard", "factory", "driver", "late work"]
    student_hostel = ["hostel", "roommate", "college", "canteen", "study", "exam"]

    # ============================================================
    # SCHEDULE TEMPLATES
    # ============================================================
    schedules = {
        "school": [
            "6:30 AM – 7:00 AM → Wake up & get ready for school",
            "7:30 AM – 2:00 PM → Attend school",
            "2:00 PM – 4:00 PM → Lunch & rest",
            "4:00 PM – 6:00 PM → Homework or tuition",
            "6:00 PM – 8:00 PM → Play / relax",
            "9:00 PM – Sleep"
        ],
        "college": [
            "6:00 AM – 7:00 AM → Wake up & breakfast",
            "8:00 AM – 2:00 PM → College / lectures",
            "2:00 PM – 4:00 PM → Lunch & rest",
            "4:00 PM – 6:00 PM → Assignments / projects",
            "7:00 PM – 10:00 PM → Study or relax",
            "11:00 PM – Sleep"
        ],
        "work": [
            "6:30 AM – 7:30 AM → Exercise / breakfast",
            "9:00 AM – 6:00 PM → Office work",
            "6:00 PM – 7:00 PM → Travel & rest",
            "7:00 PM – 9:00 PM → Family / dinner",
            "10:00 PM – Sleep"
        ],
        "gym": [
            "6:00 AM – 7:00 AM → Gym session",
            "7:30 AM – 8:30 AM → Breakfast / shower",
            "9:00 AM – 1:00 PM → Productive work / study",
            "2:00 PM – 5:00 PM → Learn / work",
            "6:00 PM – 7:00 PM → Evening cardio / walk",
            "10:00 PM – Sleep"
        ],
        "housewife": [
            "6:00 AM – 6:30 AM → Wake up & prepare breakfast",
            "7:00 AM – 10:00 AM → Cleaning / cooking / chores",
            "10:00 AM – 1:00 PM → Groceries / laundry / errands",
            "1:00 PM – 2:00 PM → Lunch & rest",
            "3:00 PM – 6:00 PM → Family / kids / TV",
            "7:00 PM – 9:00 PM → Dinner & unwind",
            "10:00 PM – Sleep"
        ],
        "retired": [
            "6:00 AM – Morning walk",
            "7:30 AM – Breakfast & newspaper",
            "10:00 AM – Reading / gardening / relaxation",
            "1:00 PM – Lunch & nap",
            "5:00 PM – Family time / TV",
            "9:00 PM – Sleep"
        ],
        "coaching": [
            "5:30 AM – Wake up & revise",
            "6:00 AM – 8:00 AM → Self-study",
            "9:00 AM – 1:00 PM → Coaching classes",
            "2:00 PM – Lunch & short nap",
            "3:00 PM – 6:00 PM → Practice problems",
            "7:00 PM – 9:00 PM → Revision & notes",
            "10:00 PM – Sleep"
        ],
        "freelancing": [
            "7:00 AM – 8:00 AM → Breakfast",
            "8:00 AM – 12:00 PM → Client projects",
            "12:00 PM – 2:00 PM → Lunch & break",
            "2:00 PM – 6:00 PM → Learning / editing",
            "7:00 PM – 10:00 PM → Relaxation / side project"
        ],
        "creative": [
            "8:00 AM – 9:00 AM → Plan content ideas",
            "10:00 AM – 2:00 PM → Create / shoot / edit",
            "3:00 PM – 6:00 PM → Post-production or design",
            "7:00 PM – 9:00 PM → Audience engagement",
            "10:00 PM – Sleep"
        ],
        "athlete": [
            "5:30 AM – 7:30 AM → Morning training / run",
            "8:00 AM – Breakfast & rest",
            "10:00 AM – Skill practice",
            "2:00 PM – Lunch / recovery",
            "4:00 PM – Evening practice / gym",
            "9:00 PM – Sleep"
        ],
        "shift_worker": [
            "8:00 AM – Sleep (after night shift)",
            "4:00 PM – Wake up & breakfast",
            "6:00 PM – Commute",
            "8:00 PM – Night shift starts",
            "4:00 AM – Short break",
            "8:00 AM – Shift ends"
        ],
        "lazy": [
            "9:00 AM – Wake up slowly",
            "10:00 AM – Chill with breakfast",
            "1:00 PM – Lunch & nap",
            "4:00 PM – Watch something / relax",
            "8:00 PM – Dinner",
            "11:00 PM – Sleep"
        ],
        "default": [
            "7:00 AM – Wake up",
            "8:00 AM – Breakfast & plan your day",
            "9:00 AM – Productive work / learning",
            "1:00 PM – Lunch & rest",
            "3:00 PM – Continue work",
            "6:00 PM – Relax / gym / family",
            "10:00 PM – Sleep"
        ]
    }

    # ============================================================
    # ACTIVITY MATCHING
    # ============================================================
    all_keywords = {
        "school": school, "college": college, "work": work, "gym": gym,
        "retired": retired, "coaching": coaching, "freelancing": freelancing,
        "creative": creative, "lazy": lazy, "housewife": housewife,
        "athlete": athlete, "shift_worker": shift_worker, "student_hostel": student_hostel
    }

    match_scores = {k: sum(word in user_input for word in v) for k, v in all_keywords.items()}
    sorted_matches = sorted(match_scores.items(), key=lambda x: x[1], reverse=True)

    if sorted_matches[0][1] == 0:
        schedule = schedules["default"]
    else:
        top_matches = [k for k, v in sorted_matches if v > 0]
        combo_key = "+".join(top_matches[:2]) if len(top_matches) > 1 else top_matches[0]
        schedule = schedules.get(combo_key, schedules[top_matches[0]])

    return jsonify({"schedule": schedule})


# ============================================================
# FEEDBACK STORAGE
# ============================================================
@app.route('/feedback', methods=['POST'])
def feedback():
    data = request.get_json()
    activities = data.get("activities", "")
    schedule = data.get("schedule", "")
    fb = data.get("feedback", "")

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO feedback (activities, schedule, feedback) VALUES (?, ?, ?)",
              (json.dumps(activities), json.dumps(schedule), fb))
    conn.commit()
    conn.close()

    return jsonify({"status": "success"})

@app.route("/check_feedback")
def check_feedback():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM feedback ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()

    html = "<h2>📋 Feedback Records</h2><table border=1 cellpadding=6><tr><th>ID</th><th>Activities</th><th>Feedback</th></tr>"
    for row in rows:
        html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[3]}</td></tr>"
    html += "</table>"
    return html


if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True)
    