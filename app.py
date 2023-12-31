#!/usr/bin/python3
# from modules import logger, config
from main import app

PORT = 6969
LOGGING_HEADER = "[APP]"
# LOGGING_LVL = config_load_config("config.json")["settings"]["log_lvl"]
LOGGING = True

if __name__ == "__main__":
    try:
        app.run(debug=True, host="0.0.0.0", port=6969)
# logger.log(message=f"App started on port {PORT}", level=LOGGING_LVL, header=LOGGING_HEADER, enabled=LOGGING, lvl=1)
    except Exception as e:
        print(f"Error starting app! {e}")
        # logger.log(f"Error starting app! {e}", LOGGING_LVL, LOGGING_HEADER, LOGGING, lvl=4)
        exit(1)
