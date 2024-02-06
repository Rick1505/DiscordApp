from settings import Config
from custom_bot import MyBot

if __name__ == "__main__":
    try:
        config = Config()
        bot = MyBot(config)
        
        bot.run(config.discord_token)
    except BaseException as error:
        print(error)
    