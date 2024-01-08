class Emoji():
    
    def __init__(self) -> None:
        
        self.custom_emojis = {
            "th16": 1189273117286215700,
            "earth": 1189280370714222672,
            "legend_trophy": 1189280876354355302,
            "plus_trophy":1193226778429374575,
            "min_trophy":1193226714046804040,

        }
    
    def get_emoji(self, emoji: str):
        return self.custom_emojis[emoji]