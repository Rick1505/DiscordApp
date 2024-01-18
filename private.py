import os
import discord


from urllib.parse import quote_plus

DATABASE_HOST = os.getenv("DB_HOST") 
DATABASE_PORT = os.getenv("DB_PORT") 
DATABASE_PASSWORD = os.getenv("DB_PASSWORD") 
DATBASE_USER = os.getenv("DB_USER") 
DATABASE_NAME = os.getenv("DB_NAME")
DATABASE_PASSWORD_UPDATED = quote_plus(DATABASE_PASSWORD)

class dev_secrets:
    db_connection_string = f"mysql+mysqlconnector://{DATBASE_USER}:{DATABASE_PASSWORD_UPDATED}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
    discord_token = os.getenv("DISCORD_TOKEN_TUTORIAL")
    coc_api_token = os.getenv("COC_API_TOKEN")
    dev_guild_id = discord.Object(int(os.getenv("TEST_GUILD_ID")))
    
    
class prod_secrets:
    db_connection_string = f"mysql+mysqlconnector://{DATBASE_USER}:{DATABASE_PASSWORD_UPDATED}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
    db_discord_token = os.getenv("DISCORD_TOKEN")
    coc_token = os.getenv("COC_API_TOKEN")
    
