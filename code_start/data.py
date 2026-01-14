class Data:
    def __init__(self, ui):
        self.ui = ui
        self.coins = 0
        self._health = 5
        self.ui.create_hearts(self._health)
        self._boss_health = 21 

    @property
    def health(self):
        return self._health
    
    @health.setter
    def health(self, value):
        self._health = value
        self.ui.create_hearts(value)

    @property
    def boss_health(self):
        return self._boss_health

    @boss_health.setter
    def boss_health(self, value):
        self._boss_health = value
        
