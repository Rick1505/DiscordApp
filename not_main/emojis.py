class Emoji():
    
    def __init__(self) -> None:
        
        self.custom_emojis = {
            "th16": 1189273117286215700,
            "earth": 1189280370714222672,
            "legend_trophy": 1189280876354355302,
        }
    
    def get_emoji(self, emoji: str):
        return self.custom_emojis[emoji]