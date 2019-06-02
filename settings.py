class Settings():
    """储存 所有设置"""
    def __init__(self):
        self.screen_width = 1000
        self.screen_height = 600
        # 背景
        self.bg_color = (230,230,230)
        #  飞船的设置
        self.ship_speed_factor = 1.5
        # 子弹的设置
        self.bullet_speed_factor = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullet_allowed = 3
    

