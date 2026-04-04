import json
import os
from datetime import datetime

class Storage:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def save(self, category: str, identifier: str, data: dict):
        """
        Saves data as a JSON file.
        Example: save("character", "azshara_김비비", {...})
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{category}_{identifier}.json" # Overwrite same character/auction per day or use timestamp?
        # For simplicity, let's keep it per identifier.
        
        filepath = os.path.join(self.data_dir, filename)
        
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return filepath
        except Exception as e:
            print(f"Error saving to {filepath}: {e}")
            return None

storage = Storage()
