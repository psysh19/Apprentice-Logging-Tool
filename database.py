import sqlite3
import pandas as pd

# --- Setup: create table if needed ---
conn = sqlite3.connect("otj_log.db")
conn.executescript("""
CREATE TABLE IF NOT EXISTS otj_entries (
    entry_id                TEXT PRIMARY KEY,
    student_id              TEXT NOT NULL,
    activity_date           TEXT NOT NULL,
    start_time              TEXT NOT NULL,
    end_time                TEXT NOT NULL,
    activity_description    TEXT NOT NULL,
    apprenticeship_standard TEXT,
    within_contracted_hours TEXT CHECK (within_contracted_hours IN ('Yes','No','Needs review')),
    funding_eligible        TEXT CHECK (funding_eligible IN ('Yes','No','Needs review')),
    ai_decision             TEXT CHECK (ai_decision IN ('Approved','Manual review')),
    ai_confidence           REAL CHECK (ai_confidence BETWEEN 0 AND 1),
    final_status            TEXT CHECK (final_status IN ('Approved','Rejected','Pending review')),
    reviewer_notes          TEXT
);
CREATE INDEX IF NOT EXISTS idx_otj_student ON otj_entries(student_id);
CREATE INDEX IF NOT EXISTS idx_otj_status ON otj_entries(final_status);
""")
conn.close()          # ← close it before moving on

def add_entry(entry):
    conn = sqlite3.connect("otj_log.db")
    try:
        conn.execute(
            "INSERT INTO otj_entries VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                entry["entry_id"], entry["student_id"], entry["activity_date"],
                entry["start_time"], entry["end_time"], entry["activity_description"],
                entry["apprenticeship_standard"], entry["within_contracted_hours"],
                entry["funding_eligible"], entry["ai_decision"], entry["ai_confidence"],
                entry["final_status"], entry["reviewer_notes"],
            ),
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        print(f"Skipped {entry['entry_id']}: {e}")   # e.g. duplicate ID on re-run
    finally:
        conn.close()

add_entry({
    "entry_id": "E004", "student_id": "S12345",
    "activity_date": "2026-07-06", "start_time": "10:00", "end_time": "12:00",
    "activity_description": "Paired with data engineer on Databricks pipeline",
    "apprenticeship_standard": "Data Scientist L6",
    "within_contracted_hours": "Yes", "funding_eligible": "Yes",
    "ai_decision": "Approved", "ai_confidence": 0.88,
    "final_status": "Approved", "reviewer_notes": None,
})

# --- Read ---
conn = sqlite3.connect("otj_log.db")
df = pd.read_sql("SELECT * FROM otj_entries WHERE student_id = ?", conn, params=("S12345",))
conn.close()

print(df)