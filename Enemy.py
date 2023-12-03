import math

class Enemy:
    def __init__(self, canvas, game_window, x, y, speed, health):
        self.canvas = canvas
        self.game_window = game_window
        self.enemy_size = 20
        self.health = health
        self.enemy = self.canvas.create_rectangle(x, y, x + self.enemy_size, y + self.enemy_size, fill=self.rgbtohex(255//self.health, 0, 0))
        self.speed = speed

    def move_towards_player(self):
        player_x, player_y, _, _ = self.canvas.coords(self.game_window.sprite.sprite)
        enemy_x, enemy_y, _, _ = self.canvas.coords(self.enemy)

        angle = math.atan2(player_y - enemy_y - self.enemy_size / 2, player_x - enemy_x - self.enemy_size / 2)
        dx = self.speed * math.cos(angle)
        dy = self.speed * math.sin(angle)

        self.canvas.move(self.enemy, dx, dy)

    def delete_enemy(self):
        self.canvas.delete(self.enemy)
    
    def update_color(self):
        self.canvas.itemconfig(self.enemy, fill=self.rgbtohex(255//self.health, 0, 0))

    def rgbtohex(self, r,g,b):
        return f'#{r:02x}{g:02x}{b:02x}'