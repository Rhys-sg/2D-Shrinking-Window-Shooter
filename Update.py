import random

import Enemy

# Main game loop
def update(self):
    if self.end_game_flag:
        return

    self.sprite.move()

    self.update_score_label() 

    for bullet in self.sprite.bullets:
        bullet.move()
        self.check_collision_bullet_enemy(bullet)

    for enemy in self.enemies:
        enemy.move_towards_player()

    if self.check_collision_player_enemy() or self.check_collision_player_wall():
        self.end_game()

    self.after(self.game_tick_rate, self.update)

def check_collision_bullet_enemy(self, bullet):
    bullet_coords = self.canvas.coords(bullet.bullet)

    for enemy in self.enemies:
        enemy_coords = self.canvas.coords(enemy.bounding_box)

        # Check for overlap between bullet and enemy
        if (
            bullet_coords[0] < enemy_coords[2] and
            bullet_coords[2] > enemy_coords[0] and
            bullet_coords[1] < enemy_coords[3] and
            bullet_coords[3] > enemy_coords[1]
        ):
            if enemy.health > 1:
                enemy.health -= 1
                enemy.update_health()
            else:
                enemy.canvas.after(1, enemy.delete_enemy)  # Delay the deletion to avoid interference with grow

                # Remove flagged enemies from the list
                self.enemies.remove(enemy)
                # Increase the score when an enemy is killed
                self.score += 1
                self.update_score_label()

            bullet.delete_flag = True  # Mark the bullet for deletion

            bullet.canvas.after(1, bullet.delete_bullet)  # Delay the deletion to avoid interference with grow
            
    # Remove flagged bullets from the list
    self.sprite.bullets = [each for each in self.sprite.bullets if not each.delete_flag]

def check_collision_player_enemy(self):
    player_coords = self.canvas.coords(self.sprite.sprite)

    for enemy in self.enemies:
        enemy_coords = self.canvas.coords(enemy.bounding_box)

        # Check for overlap between player and enemy
        if (
            player_coords[0] < enemy_coords[2] and
            player_coords[2] > enemy_coords[0] and
            player_coords[1] < enemy_coords[3] and
            player_coords[3] > enemy_coords[1]
        ):
            return True

    return False

def check_collision_player_wall(self):
    # Boundary check for player's sprite
    current_x, current_y, _, _ = self.canvas.coords(self.sprite.sprite)

    return (current_x + self.sprite.sprite_dx < 0 or
            current_y + self.sprite.sprite_dy < 0 or
            current_x + self.sprite.sprite_dx + self.sprite.sprite_size > self.width or
            current_y + self.sprite.sprite_dy + self.sprite.sprite_size > self.height)

def grow(self, direction):
    if direction == "up":
        self.height += self.growth_increment
        self.geometry(f"{self.width}x{self.height}+{self.winfo_x()}+{self.winfo_y() - self.growth_increment}")
    elif direction == "down":
        self.height += self.growth_increment
    elif direction == "right":
        self.width += self.growth_increment
    elif direction == "left":
        self.width += self.growth_increment
        self.geometry(f"{self.width}x{self.height}+{self.winfo_x() - self.growth_increment}+{self.winfo_y()}")

    self.geometry(f"{self.width}x{self.height}")

def shrink(self):
    if self.end_game_flag:
        return

    if self.width > 0 and self.height > 0:
        self.width -= self.decrement * 2
        self.height -= self.decrement * 2

        self.geometry(f"{self.width}x{self.height}+{self.winfo_x() + self.decrement}+{self.winfo_y() + self.decrement}")

        self.after(self.shrink_interval, self.shrink)

def move_sprite(self, dx, dy):
    # Update sprite velocity based on the key pressed
    self.sprite.sprite_dx += dx
    self.sprite.sprite_dy += dy

    # Boundary checks to prevent moving past the edge
    current_x, current_y, _, _ = self.canvas.coords(self.sprite.sprite)

    if current_x + self.sprite.sprite_dx < 0 or current_x + self.sprite.sprite_dx + self.sprite.sprite_size > self.width:
        self.sprite.sprite_dx = 0

    if current_y + self.sprite.sprite_dy < 0 or current_y + self.sprite.sprite_dy + self.sprite.sprite_size > self.height:
        self.sprite.sprite_dy = 0

def fire_bullet(self):
    # If the game is not over, fire a bullet in the direction of the mouse
    if not self.end_game_flag:
        self.sprite.fire_bullet()

def spawn_enemies(self):
    self.enemy_spawn_interval *= 0.99  # Reduce the spawn interval by 1% each time

    # Spawn enemies at random positions off-screen
    x = random.choice([-50, self.width + 50])
    y = random.uniform(0, self.height)
    maxhealth = (self.score // 15) + 1
    enemy = Enemy.Enemy(self.canvas, self, x, y, self.enemy_speed, random.randint(1, maxhealth))
    self.enemies.append(enemy)

    # Schedule the next enemy spawn
    self.after(round(self.enemy_spawn_interval), self.spawn_enemies)

def update_score_label(self):
    # Update the score label
    self.score_label.config(text=f"Score: {self.score}")