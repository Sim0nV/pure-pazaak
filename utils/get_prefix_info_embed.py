from discord import Embed
from constants import colors, env, strings


def get_prefix_info_embed(new_command: str) -> Embed:
    """Get prefix commands removal info embed

    Args:
        new_command (str): Command to use instead

    Returns:
        Embed: Prefix commands removal info embed
    """
    # Embed dictionary for prefix removal info
    PREFIX_INFO_EMBED_DICT = {
        "title": "Please use Slash Commands instead!",
        "description": (
            "Prefix commands have been removed: these are the commands which"
            " start with ``$``, such as ``$p`` and ``$pazaak_sfx``.\n"
            + "Please use the corresponding slash command ``"
            + new_command
            + "`` instead.\n"
            + "Full details can be found [here]("
            + strings.PREFIX_EXPLANATION_URL
            + ")."
        ),
        "color": colors.RULES_HELP_COLOUR_VALUE,
        "thumbnail": {"url": env.RULES_HELP_THUMBNAIL},
    }

    return Embed.from_dict(PREFIX_INFO_EMBED_DICT)
