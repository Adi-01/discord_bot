import json
import os

# File path for storing moderation data
MODERATION_FILE = "moderations.json"

# Ensure the file exists
if not os.path.exists(MODERATION_FILE):
    with open(MODERATION_FILE, "w") as f:
        json.dump({"warnings": {}, "bans": {}, "mutes": {}, "removed_roles": {}}, f)

def load_data():
    """Load moderation data from the JSON file."""
    with open(MODERATION_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    """Save moderation data to the JSON file."""
    with open(MODERATION_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_warning(user_id, reason):
    """Add a warning to a user and return the updated count."""
    data = load_data()
    warnings = data["warnings"]

    if str(user_id) not in warnings:
        warnings[str(user_id)] = []

    warnings[str(user_id)].append(reason)
    save_data(data)

    return len(warnings[str(user_id)])

def get_warnings(user_id):
    """Get the list of warnings for a user."""
    data = load_data()
    return data["warnings"].get(str(user_id), [])

def clear_warnings(user_id):
    """Clear all warnings for a user."""
    data = load_data()
    if str(user_id) in data["warnings"]:
        del data["warnings"][str(user_id)]
    save_data(data)

def add_ban(user_id, reason):
    """Add a banned user to the database."""
    data = load_data()
    data["bans"][str(user_id)] = reason
    save_data(data)

def is_banned(user_id):
    """Check if a user is banned."""
    data = load_data()
    return str(user_id) in data["bans"]

def remove_ban(user_id):
    """Remove a user from the ban list."""
    data = load_data()
    if str(user_id) in data["bans"]:
        del data["bans"][str(user_id)]
    save_data(data)

def add_mute(user_id, duration):
    """Store a muted user with their duration."""
    data = load_data()
    data["mutes"][str(user_id)] = duration
    save_data(data)

def remove_mute(user_id):
    """Remove a user from the mute list."""
    data = load_data()
    if str(user_id) in data["mutes"]:
        del data["mutes"][str(user_id)]
    save_data(data)

# New functions for storing and restoring removed admin roles
def store_removed_roles(user_id, roles):
    """Store removed admin roles when a user is muted."""
    data = load_data()
    data["removed_roles"][str(user_id)] = roles  # Store role IDs directly (since roles are already IDs)
    save_data(data)


def get_removed_roles(user_id):
    """Retrieve removed roles for a user."""
    data = load_data()
    return data["removed_roles"].get(str(user_id), [])

def clear_removed_roles(user_id):
    """Clear stored removed roles for a user after unmute."""
    data = load_data()
    if str(user_id) in data["removed_roles"]:
        del data["removed_roles"][str(user_id)]
    save_data(data)
