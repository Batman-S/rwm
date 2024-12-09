from datetime import datetime
from typing import Dict

def waitlist_model(name: str, party_size: int) -> Dict:
    return {
        "name": name,
        "party_size": party_size,
        "status": "waiting",  
        "created_at": datetime.now(datetime.timezone.utc),  
    }
