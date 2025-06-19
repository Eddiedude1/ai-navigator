"""
Simple configuration management module for loading TOML files as Python
objects.
"""

import toml
from typing import Any, Dict


class Config:
    """
    Simple configuration object that provides attribute-style access to
    TOML data.
    """
    def __init__(self, config_data: Dict[str, Any]):
        for key, value in config_data.items():
            if isinstance(value, dict):
                setattr(self, key, Config(value))
            else:
                setattr(self, key, value)


def create_default_config() -> Config:
    """Create a complete default config so we can use direct access"""
    default_data = {
        "general": {
            "max_navigation_steps": 20,
            "log_level": "INFO"
        },
        "ai": {
            "model": "claude-3-5-sonnet-20241022",
            "token_limits": {
                "page_analysis": 2000,
                "decision_making": 1000,
                "goal_completion": 400
            }
        },
        "browser": {
            "headless": False,
            "viewport_width": 1920,
            "viewport_height": 1080,
            "timeout": 30000
        },
        "timing": {
            "min_action_delay": 1.0,
            "max_action_delay": 3.0,
            "page_load_wait": 2.0,
            "click_delay": 0.5
        }
    }
    return Config(default_data)


def load_config(file_path: str) -> Config:
    """
    Load a TOML configuration file and return a Config object.

    Args:
        file_path: Path to the TOML configuration file

    Returns:
        Config object with attribute access to configuration values
    """
    try:
        with open(file_path, 'r') as f:
            config_data = toml.load(f)
        return Config(config_data)

    except FileNotFoundError:
        print("Error: config.toml not found.")
        raise
    except PermissionError:
        print("Error: Permission denied to read config.toml.")
        raise
    except toml.decoder.TomlDecodeError as e:
        print(f"Error: Invalid TOML format in config.toml: {e}")
        raise
    except OSError as e:
        print(f"Error: An OS error occurred: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise


# Example usage
if __name__ == "__main__":
    # Example TOML content
    example_toml = """
    app_name = "MyApp"
    debug = true

    [database]
    host = "localhost"
    port = 5432

    [logging]
    level = "INFO"
    """

    # Create test file
    with open("config.toml", "w") as f:
        f.write(example_toml)

    # Load and use config
    config = load_config("config.toml")

    print(f"App: {config.app_name}")
    print(f"Debug: {config.debug}")
    print(f"DB Host: {config.database.host}")
    print(f"DB Port: {config.database.port}")
    print(f"Log Level: {config.logging.level}")
