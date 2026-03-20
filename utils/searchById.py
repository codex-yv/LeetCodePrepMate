import os
import sys
import sqlite3

def _get_db_connection():
    if getattr(sys, 'frozen', False):
        base = sys._MEIPASS
    else:
        base = os.path.join(os.path.dirname(__file__), '..')
    db_path = os.path.join(base, 'companies', 'companies.db')
    return sqlite3.connect(db_path)

def getDatabyId():
    """
    Returns a dict keyed by question ID (str), each value being:
      {
        "Companies_List": [{"company_name": str, "frequency": float}, ...],
        "acceptance": float,
        "difficulty": str,
        "question": str,
        "Link": str
      }
    Aggregates across all company tables in the database.
    """
    conn = _get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [row[0] for row in cur.fetchall()]

    s = {}

    for table in tables:
        try:
            cur.execute(f'SELECT ID, Title, Acceptance, Difficulty, Frequency, Leetcode_Question_Link FROM "{table}"')
            rows = cur.fetchall()
            for row in rows:
                try:
                    raw_id, title, acceptance_str, difficulty, frequency_str, link = row

                    qid = str(raw_id).strip()

                    # Clean and convert fields
                    acceptance = float(str(acceptance_str).strip('%')) if acceptance_str else 0.0
                    frequency = float(frequency_str) if frequency_str else 0.0

                    if qid not in s:
                        s[qid] = {
                            "Companies_List": [],
                            "acceptance": acceptance,
                            "difficulty": difficulty.strip() if difficulty else "",
                            "question": title.strip() if title else "",
                            "Link": link.strip() if link else ""
                        }

                    # Always add the company entry
                    s[qid]["Companies_List"].append({
                        "company_name": table,
                        "frequency": frequency
                    })

                except (ValueError, TypeError) as e:
                    print(f"Skipping row in table '{table}' due to error: {e}")

        except Exception as e:
            print(f"Error reading table '{table}': {e}")

    conn.close()
    return s


class FindDataByID:
    def __init__(self):
        self.acceptance: float
        self.difficulty: str
        self.question: str
        self.link: str
        self.companies: list
        self.total: int

    def findDatabyId(self, k: str = None, s: dict = None):
        if k is None:
            return 101
        try:
            self.data = s[k]
            self.companies = self.data["Companies_List"]
            self.acceptance = self.data["acceptance"]
            self.question = self.data["question"]
            self.difficulty = self.data["difficulty"]
            self.link = self.data["Link"]
            self.total = len(self.companies)
        except KeyError:
            return 404
