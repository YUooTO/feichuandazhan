class Settings():
    """储存 所有设置"""
    def __init__(self):
        # 初始化游戏的静态设置
        self.screen_width = 1200
        self.screen_height = 800
        # 背景
        self.bg_color = (230,230,230)
        #  飞船的设置
        
        self.ship_limit = 3
        # 子弹的设置
        
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullet_allowed = 5

        # 外星人的设置
        self.fleet_drop_speed = 5


        # 以什么样的速度加快游戏节奏
        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        # 初始化随游戏而变化的值
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        # 计分
        self.alien_points = 50
        # 外星人的方向， 1 为右侧， -1 为左侧
        self.fleet_direction = 1
    
    def inc_speed(self):
        # 提高速度设置
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points*self.speedup_scale)

