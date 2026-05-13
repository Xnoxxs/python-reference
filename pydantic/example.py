
from pydantic import BaseModel
from typing import Optional


# -------------------------
# User request model
# -------------------------
class UserRequest(BaseModel):
    name: str
    email: str
    photo: Optional[str] = None
    password: Optional[str] = None
    device_push_token: Optional[str] = None


# -------------------------
# Simulate frontend JSON
# -------------------------
frontend_json = {
    "name": "John",
    "email": "john@example.com",
    "photo": "photo.png",
    "password": "Secret123",
    "device_push_token": "token123"
}


# -------------------------
# Parse + validate request
# -------------------------
user_data = UserRequest(**frontend_json)


# -------------------------
# Access fields safely
# -------------------------
print("User name:", user_data.name)
print("User email:", user_data.email)

# -------------------------
# Turn the model back into json
# -------------------------
print("User Model:", user_data.model_dump())


# -------------------------
# Print all fields dynamically
# -------------------------
print("\nFields received from frontend:")

for field_name, value in user_data.model_dump().items():
    print(field_name, "=", value)


print(user_data.name.key)  # "name"