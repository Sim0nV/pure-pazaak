import os
from dotenv import load_dotenv

import ast

# Environment Variables Constants
load_dotenv()  # Load .env file

# Options
IS_DEBUG_MODE = os.getenv("IS_DEBUG_MODE", "False") == "True"
SHOULD_SYNC_COMMANDS = os.getenv("SHOULD_SYNC_COMMANDS", "False") == "True"

# Debug Mode Bot Info
DEV_BOT_ID = os.getenv("DEV_BOT_ID")
DEV_BOT_TOKEN = os.getenv("DEV_BOT_TOKEN")

# Prod Mode Bot Info (Debug Mode False)
PROD_BOT_ID = os.getenv("PROD_BOT_ID")
PROD_BOT_TOKEN = os.getenv("PROD_BOT_TOKEN")

# Acknowledgements
ACK_URL = os.getenv("ACK_URL")

# Thumbnails
RULES_HELP_THUMBNAIL = os.getenv("RULES_HELP_THUMBNAIL")
USAGE_THUMBNAIL = os.getenv("USAGE_THUMBNAIL")
MESSAGE_ERROR_THUMBNAIL = os.getenv("MESSAGE_ERROR_THUMBNAIL")
STATS_THUMBNAIL = os.getenv("STATS_THUMBNAIL")
EGG_1_THUMBNAIL = os.getenv("EGG_1_THUMBNAIL")

# Thumbnail Arrays
CHALLENGE_THUMBNAILS = ast.literal_eval(os.getenv("CHALLENGE_THUMBNAILS"))
INGAME_THUMBNAILS = ast.literal_eval(os.getenv("INGAME_THUMBNAILS"))
MATCH_END_THUMBNAILS = ast.literal_eval(os.getenv("MATCH_END_THUMBNAILS"))
FORFEIT_THUMBNAILS = ast.literal_eval(os.getenv("FORFEIT_THUMBNAILS"))
TIMEOUT_THUMBNAILS = ast.literal_eval(os.getenv("TIMEOUT_THUMBNAILS"))
ERROR_THUMBNAILS = ast.literal_eval(os.getenv("ERROR_THUMBNAILS"))
SFX_ON_THUMBNAILS = ast.literal_eval(os.getenv("SFX_ON_THUMBNAILS"))
SFX_OFF_THUMBNAILS = ast.literal_eval(os.getenv("SFX_OFF_THUMBNAILS"))

# Database
DB_CONNECTION_URL = os.getenv("DB_CONNECTION_URL")
PROD_DB_COLLECTION = os.getenv("PROD_DB_COLLECTION")
DEV_DB_COLLECTION = os.getenv("DEV_DB_COLLECTION")

# Sounds
DEAL_CARD_SOUND = os.getenv("DEAL_CARD_SOUND")
PLAY_CARD_SOUND = os.getenv("PLAY_CARD_SOUND")
STAND_SOUND = os.getenv("STAND_SOUND")
BUST_SOUND = os.getenv("BUST_SOUND")
DRAW_SOUND = os.getenv("DRAW_SOUND")
ROUND_END_SOUND = os.getenv("ROUND_END_SOUND")
FORFEIT_TIMEOUT_SOUND = os.getenv("FORFEIT_TIMEOUT_SOUND")
MATCH_END_SOUND = os.getenv("MATCH_END_SOUND")
NINE_CARDS_SOUND = os.getenv("NINE_CARDS_SOUND")

# Card Images dictionary in the format:
# {
#     # Negative cards -6 through -1
#     "-6": NEG_6_IMAGE_URL_STRING,
#     # ...
#     "-1": NEG_1_IMAGE_URL_STRING,
#     # Positive Cards +1 through +6
#     "+1": POS_1_IMAGE_URL_STRING,
#     # ...
#     "+6": POS_6_IMAGE_URL_STRING,
#     # Dealer Cards 1 through 10
#     "1": 1_IMAGE_URL_STRING,
#     #...
#     "10": 10_IMAGE_URL_STRING,
# }
CARD_IMAGES_DICT: dict = ast.literal_eval(os.getenv("CARD_IMAGES_DICT"))
