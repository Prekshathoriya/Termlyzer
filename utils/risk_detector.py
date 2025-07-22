import re

# Define patterns to flag risky clauses
RISK_PATTERNS = {
    "Auto-renewal": r"(auto[-\s]?renew|automatically\s+renewed)",
    "Data Sharing": r"(share.*?data|third[-\s]?part(y|ies))",
    "Waiver of Rights": r"(waive.*?right|class\s+action|arbitration)",
    "Unilateral Changes": r"(we\s+may\s+change.*?without\s+notice)",
    "Ambiguous Terms": r"(sole\s+discretion|reasonable\s+efforts)",
}

def detect_risky_clauses(text: str) -> list:
    """
    Splits text into clauses and flags any that match risky patterns.
    Returns list of dicts with clause, risk tag, and match type.
    """
    clauses = re.split(r'(?<=[.?!])\s+', text)
    risky = []

    for clause in clauses:
        for label, pattern in RISK_PATTERNS.items():
            if re.search(pattern, clause, flags=re.IGNORECASE):
                risky.append({
                    "clause": clause.strip(),
                    "tag": label,
                    "highlight": True
                })
                break  # Only tag once per clause

    return risky
