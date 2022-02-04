from wordleAssistant import Assistant
from wordleGame import Game

class Simulation:
    MAX_SIMULATIONS = 100
    
    def __init__(self) -> None:
        self.assisstant = Assistant()
        self.game = Game()