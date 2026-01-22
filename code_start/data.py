class Data:
    def __init__(self, ui):
        self.ui = ui
        self._coins = 0
        self._health = 5
        self.ui.create_hearts(self._health)
        self._boss_health = 21 
        self.ui.create_boss_healthbar()

        self.unlocked_level = 0
        self.current_level = 0

    def start_level(self, level_number):
        self.current_level = level_number
        
        # Only show the healthbar if it's the boss level (currently level 1)
        if self.current_level == 1:
            self.ui.create_boss_healthbar()
        else:
            self.ui.hide_boss_healthbar() 

    @property
    def coins(self):
        return self._coins

    @coins.setter
    def coins(self, value):
        self._coins = value
        if self.coins >= 10:
            self.coins -= 10
            self.health += 1
        self.ui.show_coins(self.coins)

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
        
