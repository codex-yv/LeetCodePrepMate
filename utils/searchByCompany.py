import os
import sys
import sqlite3

# Time-period suffixes used in table names (order matters: most preferred first)
_TIMEFRAME_PRIORITY = ["_alltime", "_2year", "_1year", "_6months"]

def _get_db_connection():
    if getattr(sys, 'frozen', False):
        # Inside PyInstaller bundle — data files live in _MEIPASS
        base = sys._MEIPASS
    else:
        base = os.path.join(os.path.dirname(__file__), '..')
    db_path = os.path.join(base, 'companies', 'companies.db')
    return sqlite3.connect(db_path)


def _extract_company_name(table_name: str) -> str:
    """
    Strips the known timeframe suffix from a table name to get the clean
    company name.  e.g. 'google_alltime' → 'google', 'adobe_6months' → 'adobe'
    """
    for suffix in _TIMEFRAME_PRIORITY:
        if table_name.endswith(suffix):
            return table_name[: -len(suffix)]
    # Fallback: strip the last underscore-separated segment
    parts = table_name.rsplit("_", 1)
    return parts[0] if len(parts) > 1 else table_name


def _read_table(cur, table: str) -> list:
    """Read all question rows from a single table and return as list of dicts."""
    questions = []
    try:
        cur.execute(
            f'SELECT ID, Title, Acceptance, Difficulty, Frequency, Leetcode_Question_Link FROM "{table}"'
        )
        for row in cur.fetchall():
            try:
                raw_id, title, acceptance, difficulty, frequency, link = row
                questions.append({
                    "id": int(raw_id),
                    "question": title.strip() if title else "",
                    "frequency": float(frequency) if frequency else 0.0,
                    "difficulty": difficulty.strip().lower() if difficulty else "",
                    "acceptance": acceptance.strip() if acceptance else "",
                    "link": link.strip() if link else "",
                })
            except (ValueError, TypeError) as e:
                print(f"Skipping row in '{table}': {e}")
    except Exception as e:
        print(f"Error reading table '{table}': {e}")
    return questions


def getDataByCompany() -> dict:
    """
    Returns a dict keyed by *clean company name* (e.g. 'google', 'amazon'),
    where each value is the question list from the best available timeframe
    table for that company (prefer _alltime > _2year > _1year > _6months).

    This maintains the same dict structure as the old CSV-based version so
    the rest of main.py needs no changes.
    """
    conn = _get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    all_tables = [row[0] for row in cur.fetchall()]

    # Group tables by clean company name
    company_tables: dict[str, list[str]] = {}
    for table in all_tables:
        cname = _extract_company_name(table)
        company_tables.setdefault(cname, []).append(table)

    s: dict[str, list] = {}

    for cname, tables in company_tables.items():
        # Pick the best table according to priority order
        chosen = None
        for suffix in _TIMEFRAME_PRIORITY:
            for t in tables:
                if t == cname + suffix:
                    chosen = t
                    break
            if chosen:
                break
        if chosen is None:
            chosen = tables[0]  # fallback

        s[cname] = _read_table(cur, chosen)

    conn.close()
    return s


class FindDataByCompany:
    def __init__(self):
        self.data_ldict: list
        self.totalq: int
        self.easy: int
        self.medium: int
        self.hard: int
        self.only_hard: list
        self.only_easy: list
        self.only_medium: list
        # Store only keys (company names) — no need to keep question data in memory twice
        self._company_names: list[str] = []
        self._load_company_names()

    def _load_company_names(self):
        """Load just the company name keys from the DB (fast — no row data)."""
        conn = _get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        all_tables = [row[0] for row in cur.fetchall()]
        conn.close()

        seen = set()
        for table in all_tables:
            cname = _extract_company_name(table)
            if cname not in seen:
                seen.add(cname)
                self._company_names.append(cname)

    def findDataByCompany(self, data: dict = None, cname: str = None):
        if data is None or cname is None:
            return 101
        try:
            self.data_ldict = data[cname]
            self.totalq = len(self.data_ldict)
            e = m = h = 0
            for item in self.data_ldict:
                d = item["difficulty"]
                if d == "easy":
                    e += 1
                elif d == "medium":
                    m += 1
                elif d == "hard":
                    h += 1
            self.easy = e
            self.medium = m
            self.hard = h
        except KeyError:
            return 404

    def dropDownList(self, cname: list = None):
        """
        Returns company names whose name *contains* (as a substring) all the
        characters typed so far, in order.  Uses prefix / substring matching
        so 'goo' only matches names that contain 'goo' as a contiguous run,
        giving a much cleaner, expected autocomplete experience.
        """
        if not cname:
            return []

        # Build the substring the user has typed so far
        typed = "".join(cname).lower()
        return [comp for comp in self._company_names if typed in comp.lower()]

    def sortedDifficulty(self, data: list):
        sorted_hard = []
        sorted_medium = []
        sorted_easy = []

        for details in data:
            try:
                d = details["difficulty"]
                if d == "hard":
                    sorted_hard.append(details)
                elif d == "medium":
                    sorted_medium.append(details)
                elif d == "easy":
                    sorted_easy.append(details)
                else:
                    return 101
            except KeyError:
                return 101

            self.only_easy = sorted_easy
            self.only_medium = sorted_medium
            self.only_hard = sorted_hard
