import json
import modules.logger as logger

LOGGING_HEADER = "[CONFIG]"


def load_config(config_file):
    try:
        with open(config_file, "r") as f:
            file = json.load(f)

    except Exception as e:
        logger.log(f"Error loading config file! {e}", file["settings"]["log_lvl"], LOGGING_HEADER,
                   file["settings"]["log"], lvl=4)
        exit(1)
    logger.log("Config file loaded!", file["settings"]["log_lvl"], LOGGING_HEADER,
               file["settings"]["log"], lvl=1)
    return file
