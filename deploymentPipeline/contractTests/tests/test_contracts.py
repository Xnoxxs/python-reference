
from pathlib import Path
import os
import json
import requests
import pytest
from deepdiff import DeepDiff

contracts_directory = Path(__file__).parent / "contracts"
DEV_SERVER_URL = os.getenv("DEV_SERVER_URL", "http://localhost:9000")
RUN_CONTRACT_TESTS = os.getenv("RUN_CONTRACT_TESTS", "0") == "1"

# These tests_need_fix compare DEV responses against captured PROD contracts.
# They are opt-in because CI does not run a local DEV backend by default.
pytestmark = pytest.mark.skipif(
    not RUN_CONTRACT_TESTS,
    reason="Contract tests_need_fix are disabled by default. Set RUN_CONTRACT_TESTS=1 to enable.",
)

def check_contract(endpoint, path):
    # endpoint = get_users
    # path = /get-users

    # call the DEV endpoint
    response = requests.get(DEV_SERVER_URL + path)
    response.raise_for_status()
    actual = response.json()

    # get the PROD repositories for this endpoint
    with open(contracts_directory / f"{endpoint}.json") as f:
        expected = json.load(f)

    # Compare the PROD and DEV repositories to detect any breaking changes
    diff = DeepDiff(expected, actual, ignore_order=True)

    return diff

def test_get_users_contract():
    diff = check_contract("get-users", "/get-users")
    assert diff == {}, f"\n❌ Contract violation:\n{diff}\n"


def test_get_activity_contract():
    diff = check_contract("get-activity", "/get-activity")
    assert diff == {}, f"\n❌ Contract violation:\n{diff}\n"
