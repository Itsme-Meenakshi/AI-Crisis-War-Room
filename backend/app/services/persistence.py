import os
import json
import threading
from datetime import datetime, timedelta
from typing import List, Optional

DB_DIR = "c:/Users/adars/OneDrive/Desktop/AI-Crisis-War-Room/backend/app/data"
DB_PATH = os.path.join(DB_DIR, "crises_store.json")

# Thread lock to prevent concurrent write corruption
db_lock = threading.Lock()

# Seed data matching the default frontend seed
SEED_CRISES = [
    {
        "id": "c_demo1",
        "title": "Customer data exposure — analytics vendor",
        "description": "Third-party analytics vendor reported unauthorized access affecting an estimated 18k customer records.",
        "createdAt": (datetime.utcnow() - timedelta(hours=6)).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
        "status": "active",
        "severity": 82,
        "category": "Cybersecurity",
        "attachments": [],
        "stakeholders": [
            {"name": "Customers", "impact": 88, "sentiment": "negative"},
            {"name": "Regulators", "impact": 76, "sentiment": "neutral"},
            {"name": "Investors", "impact": 64, "sentiment": "negative"},
            {"name": "Employees", "impact": 42, "sentiment": "neutral"}
        ],
        "risks": [
            {"category": "Financial", "likelihood": 72, "impact": 78},
            {"category": "Reputation", "likelihood": 86, "impact": 82},
            {"category": "Legal", "likelihood": 80, "impact": 84},
            {"category": "Operational", "likelihood": 55, "impact": 60},
            {"category": "Compliance", "likelihood": 78, "impact": 80}
        ],
        "perspectives": [
            {
                "perspective": "Business",
                "summary": "Short-term revenue exposure is moderate. Prioritize customer retention messaging and protect top-100 accounts.",
                "recommendations": [
                    "Brief executive team within 1 hour",
                    "Freeze non-critical marketing campaigns",
                    "Activate retention task force for tier-1 accounts"
                ]
            },
            {
                "perspective": "PR",
                "summary": "Public sentiment is trending negative. A factual, empathetic statement within the next 2 hours is critical to control narrative.",
                "recommendations": [
                    "Publish holding statement on owned channels",
                    "Brief key journalists with verified facts",
                    "Monitor sentiment hourly across social channels"
                ]
            },
            {
                "perspective": "Legal",
                "summary": "Disclosure obligations may apply. Preserve evidence, restrict internal commentary, and prepare regulator notifications.",
                "recommendations": [
                    "Issue litigation hold to all involved teams",
                    "Engage outside counsel on disclosure timing",
                    "Draft regulator notification template"
                ]
            },
            {
                "perspective": "Operations",
                "summary": "Containment is the priority. Isolate affected systems and stand up an incident command with 30-min checkpoints.",
                "recommendations": [
                    "Activate incident command structure",
                    "Isolate affected systems / facilities",
                    "Establish 30-min status cadence"
                ]
            }
        ],
        "timeline": [
            {"time": "0-1h", "title": "Activate war room & assign incident commander", "owner": "Operations", "priority": "P0"},
            {"time": "0-2h", "title": "Publish holding statement to customers & media", "owner": "PR", "priority": "P0"},
            {"time": "1-3h", "title": "Issue litigation hold & assess disclosure duties", "owner": "Legal", "priority": "P0"},
            {"time": "2-6h", "title": "Brief board and top-100 customers", "owner": "Business", "priority": "P1"}
        ]
    },
    {
        "id": "c_demo2",
        "title": "Manufacturing line halt — Plant 4",
        "description": "Unplanned shutdown of Line B affecting shipment SLAs for the Northeast region.",
        "createdAt": (datetime.utcnow() - timedelta(hours=26)).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
        "status": "monitoring",
        "severity": 58,
        "category": "Operational",
        "attachments": [],
        "stakeholders": [
            {"name": "Customers", "impact": 65, "sentiment": "negative"},
            {"name": "Employees", "impact": 40, "sentiment": "neutral"},
            {"name": "Partners", "impact": 55, "sentiment": "neutral"}
        ],
        "risks": [
            {"category": "Financial", "likelihood": 60, "impact": 50},
            {"category": "Reputation", "likelihood": 40, "impact": 45},
            {"category": "Legal", "likelihood": 30, "impact": 20},
            {"category": "Operational", "likelihood": 85, "impact": 70},
            {"category": "Compliance", "likelihood": 25, "impact": 30}
        ],
        "perspectives": [
            {
                "perspective": "Operations",
                "summary": "Line B mechanical failure has halted manufacturing. Assess physical repairs and logistics rerouting options.",
                "recommendations": [
                    "Deploy maintenance engineering team immediately",
                    "Audit spare parts stock levels",
                    "Initiate line failover routing configurations"
                ]
            }
        ],
        "timeline": [
            {"time": "0-2h", "title": "Inspect Line B physical mechanical failures", "owner": "Operations", "priority": "P0"},
            {"time": "2-6h", "title": "Re-route shipment backlogs to Plant 2", "owner": "Business", "priority": "P1"}
        ]
    },
    {
        "id": "c_demo3",
        "title": "Executive social media controversy",
        "description": "Public statement by SVP gaining negative traction; trending in two markets.",
        "createdAt": (datetime.utcnow() - timedelta(hours=70)).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
        "status": "resolved",
        "severity": 44,
        "category": "Reputation",
        "attachments": [],
        "stakeholders": [
            {"name": "Customers", "impact": 45, "sentiment": "neutral"},
            {"name": "Media", "impact": 60, "sentiment": "negative"},
            {"name": "Employees", "impact": 35, "sentiment": "neutral"}
        ],
        "risks": [
            {"category": "Financial", "likelihood": 30, "impact": 25},
            {"category": "Reputation", "likelihood": 70, "impact": 60},
            {"category": "Legal", "likelihood": 20, "impact": 15},
            {"category": "Operational", "likelihood": 10, "impact": 10},
            {"category": "Compliance", "likelihood": 10, "impact": 10}
        ],
        "perspectives": [
            {
                "perspective": "PR",
                "summary": "Controversy is resolved after executive issued a public apology and deleted the post.",
                "recommendations": [
                    "Publish official corporate distancing response",
                    "Conduct employee training on media conduct rules"
                ]
            }
        ],
        "timeline": [
            {"time": "0-1h", "title": "Delete post and issue personal apology", "owner": "PR", "priority": "P0"},
            {"time": "6-12h", "title": "Brief internal staff on media policies", "owner": "Business", "priority": "P2"}
        ]
    }
]

def init_db():
    """Ensure database directories exist and seed defaults if empty."""
    os.makedirs(DB_DIR, exist_ok=True)
    with db_lock:
        if not os.path.exists(DB_PATH):
            print(f"Initializing JSON database at {DB_PATH} with seed entries...")
            with open(DB_PATH, "w", encoding="utf-8") as f:
                json.dump(SEED_CRISES, f, indent=2)

def read_db() -> List[dict]:
    """Read all crises from the local database."""
    init_db()
    with db_lock:
        try:
            with open(DB_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error reading local database: {e}")
            return []

def write_db(data: List[dict]):
    """Write all crises atomically back to the database."""
    init_db()
    with db_lock:
        try:
            # Temporary file write + rename pattern for atomic operations
            temp_path = DB_PATH + ".tmp"
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            os.replace(temp_path, DB_PATH)
        except Exception as e:
            print(f"Error writing to database: {e}")

def get_all_crises() -> List[dict]:
    """Retrieve all crises sorted by creation date descending."""
    list_data = read_db()
    # Sort by createdAt descending
    try:
        list_data.sort(key=lambda c: c.get("createdAt", ""), reverse=True)
    except Exception:
        pass
    return list_data

def get_crisis_by_id(crisis_id: str) -> Optional[dict]:
    """Retrieve a single crisis by ID."""
    list_data = read_db()
    for c in list_data:
        if c.get("id") == crisis_id:
            return c
    return None

def save_crisis(analysis: dict):
    """Save or update a crisis analysis record in the database."""
    list_data = read_db()
    
    # Check if already exists and update, or append new
    idx = -1
    for i, c in enumerate(list_data):
        if c.get("id") == analysis.get("id"):
            idx = i
            break
            
    if idx >= 0:
        list_data[idx] = analysis
    else:
        list_data.append(analysis)
        
    write_db(list_data)
    print(f"Saved crisis {analysis.get('id')} to the database.")
