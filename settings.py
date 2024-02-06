import logging
import discord
from private import dev_secrets, prod_secrets


class Config:
    def __init__(self) -> None:
        dev_mode = True

        if dev_mode:
            print("DEV_MODE ON")
            self.db_connection_string = dev_secrets.db_connection_string
            self.discord_token = dev_secrets.discord_token
            self.coc_api_token = dev_secrets.coc_api_token
            self.guild_id: discord.Object = dev_secrets.dev_guild_id
        else:
            print("DEV_MODE OFF")
            self.db_connection_string = prod_secrets.db_connection_string
            self.discord_token = prod_secrets.discord_token
            self.coc_api_token = prod_secrets.coc_api_token
            
        self.initial_extensions = (
            "cogs.group",
            "cogs.legend_feed",
            "cogs.player_info",
            "cogs.background_tasks",
            "design.custom_embeds"
        )
