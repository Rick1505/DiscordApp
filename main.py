from settings import Config
from custom_bot import MyBot

if __name__ == "__main__":
    try:
        config = Config()
        print("test")
        bot = MyBot(config)
        print("test")
        
        bot.run(config.discord_token)
    except BaseException as error:
        print(error)
    