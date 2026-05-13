import json
import os
import requests
from typing import Protocol, cast

from train.deploymentPipeline.variables import PROD_SERVER_URL

CONTRACT_DIR = os.path.join(os.path.dirname(__file__), "tests_need_fix", "contracts")
os.makedirs(CONTRACT_DIR, exist_ok=True)

class _SupportsWriteStr(Protocol):
    def write(self, __s: str) -> object: ...

endpoints = {"/get-users", "/get-activity"}

for endpoint in endpoints:

    # /get-users
    print(f"Capturing contract for {endpoint}...")

    # Make a request to that endpoint
    response = requests.get(PROD_SERVER_URL + endpoint)
    response.raise_for_status()

    data = response.json()

    endpoint_name = endpoint[1:] # /et-users
    out_path = os.path.join(CONTRACT_DIR, f"{endpoint_name}.json")

    # Make a json file that contains the repositories that came from the endpoint of the PROD SERVER
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, cast(_SupportsWriteStr, f), indent=2)

print("✔ Contract snapshots saved.")
