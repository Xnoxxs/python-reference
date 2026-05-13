
"""
 path of file.py, inside Train/Imports
os.path.dirname(__file__) → goes UP to the Train folder
os.path.dirname(os.path.dirname(__file__)) → goes UP AGAIN to the Server folder
sys.path.append(...) → adds Server/ to Python imports
"""
import json
import os

# 1. Get the directory of THIS Python file
current_dir = os.path.dirname(__file__) # Server/Train/Imports

# 2. Go up 2 folders to reach project root:
project_root = os.path.dirname(os.path.dirname(current_dir)) # Server

# 3. Build full path to JSON file
json_path = os.path.join(project_root, "firebase_service_key_prod.json")

# 4. Load the JSON
with open(json_path, "r") as f:
    settings = json.load(f)

print(settings)