from global_settings import SESSION_FILE, STORAGE_PATH
import yaml
import os

def ensure_directory_exists(file_path):
    """Ensure the directory for the given file path exists."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

def save_session(state):
    """Save the session state to a YAML file."""
    ensure_directory_exists(SESSION_FILE)
    state_to_save = {key: value for key, value in state.items()}
    with open(SESSION_FILE, 'w') as file:
        yaml.dump(state_to_save, file)

def load_session(state):
    """Load the session state from a YAML file."""
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, 'r') as file:
            try:
                loaded_state = yaml.safe_load(file) or {}
                for key, value in loaded_state.items():
                    state[key] = value
                return True
            except yaml.YAMLError as e:
                print(f"Error loading session file: {e}")
                return False
    return False

def delete_session(state):
    """Delete the session file and clear the session state."""
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
    if os.path.exists(STORAGE_PATH):
        for filename in os.listdir(STORAGE_PATH):
            file_path = os.path.join(STORAGE_PATH, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)
    for key in list(state.keys()):
        del state[key]
