import random
import tkinter as tk

import Sprite
import Enemy

class GameWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Game Window")
        self.width = 500
        self.height = 500

        # Initialize score variable
        self.score = 0

        # Create and place the score label
        self.score_label = tk.Label(self, text="Score: 0", font=("Helvetica", 12))
        self.score_label.pack(side=tk.TOP, anchor=tk.NW)

        # Center the window on the screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - self.width) // 2
        y = (screen_height - self.height) // 2
        self.geometry(f"{self.width}x{self.height}+{x}+{y}")

        self.start_button = tk.Button(self, text="Start", command=self.start_game)
        self.start_button.pack(pady=self.height / 2.5)
        

        self.canvas = tk.Canvas(self, width=self.width, height=self.height)
        self.canvas.pack()

        self.sprite_size = 20
        self.sprite = Sprite.Sprite(self.canvas, self.width, self.height, self.sprite_size)
        self.sprite.game_window = self  # Pass the reference to GameWindow to the Sprite

        self.enemies = []  # List to store enemy instances
        self.enemy_spawn_interval = 2000  # Time interval for spawning enemies in milliseconds
        self.enemy_speed = 1.5  # Speed of enemies

        self.shrink_interval = 100  # Time interval for shrinking in milliseconds
        self.game_tick_rate = 10  # Time interval for updating all other parts of the game in milliseconds
        self.decrement = 1  # Amount to shrink in each interval
        self.move_distance = 3  # Distance to move the sprite in each key press

        self.end_game_flag = False

        self.bind("w", lambda event: self.move_sprite(0, -self.move_distance))
        self.bind("s", lambda event: self.move_sprite(0, self.move_distance))
        self.bind("d", lambda event: self.move_sprite(self.move_distance, 0))
        self.bind("a", lambda event: self.move_sprite(-self.move_distance, 0))
        self.bind("<Button-1>", lambda event: self.fire_bullet())
        self.bind("<Down>", lambda event: self.move_sprite(0, self.move_distance))
        self.bind("<Right>", lambda event: self.move_sprite(self.move_distance, 0))
        self.bind("<Left>", lambda event: self.move_sprite(-self.move_distance, 0))
        self.bind("<Button-1>", lambda event: self.fire_bullet())

        # Store the last key pressed
        self.last_key = ""

    def start_game(self):
        self.start_button.pack_forget()

        # Show the sprite when the game starts
        self.sprite.show()

        
        self.update()
        self.shrink()
        self.spawn_enemies()

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

        if self.check_collision_player_enemy():
            self.end_game()

        self.after(self.game_tick_rate, self.update)

    def check_collision_bullet_enemy(self, bullet):
        bullet_coords = self.canvas.coords(bullet.bullet)

        for enemy in self.enemies:
            enemy_coords = self.canvas.coords(enemy.enemy)

            # Check for overlap between bullet and enemy
            if (
                bullet_coords[0] < enemy_coords[2] and
                bullet_coords[2] > enemy_coords[0] and
                bullet_coords[1] < enemy_coords[3] and
                bullet_coords[3] > enemy_coords[1]
            ):
                if enemy.health > 1:
                    enemy.health -= 1
                    enemy.update_color()
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
            enemy_coords = self.canvas.coords(enemy.enemy)

            # Check for overlap between player and enemy
            if (
                player_coords[0] < enemy_coords[2] and
                player_coords[2] > enemy_coords[0] and
                player_coords[1] < enemy_coords[3] and
                player_coords[3] > enemy_coords[1]
            ):
                return True

        return False

    def end_game(self):
        self.end_game_flag = True

        # Display game over message
        game_over_label = tk.Label(self, text="Game Over", font=("Helvetica", 24))
        game_over_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        score_label = tk.Label(self, text=f"Score: {self.score}", font=("Helvetica", 12))
        score_label.place(relx=0.5, rely=0.575, anchor=tk.CENTER)

        for enemy in self.enemies:
            self.canvas.delete(enemy.enemy)
        for bullet in self.sprite.bullets:
            self.canvas.delete(bullet.bullet)

        # Hide the sprite and stop updating the game
        self.sprite.hide()
        self.after_cancel(self.update)

    def grow(self, direction):
        increment = 10

        if direction == "up":
            self.height += increment
            self.geometry(f"{self.width}x{self.height}+{self.winfo_x()}+{self.winfo_y() - increment}")
        elif direction == "down":
            self.height += increment
        elif direction == "right":
            self.width += increment
        elif direction == "left":
            self.width += increment
            self.geometry(f"{self.width}x{self.height}+{self.winfo_x() - increment}+{self.winfo_y()}")

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
        self.enemy_spawn_interval -= 50  # Reduce the spawn interval by 1% each time

        # Spawn enemies at random positions off-screen
        x = random.choice([-50, self.width + 50])
        y = random.uniform(0, self.height)
        maxhealth = (self.score // 10) + 1
        enemy = Enemy.Enemy(self.canvas, self, x, y, self.enemy_speed, random.randint(1, maxhealth))
        self.enemies.append(enemy)

        # Schedule the next enemy spawn
        self.after(self.enemy_spawn_interval, self.spawn_enemies)

    def update_score_label(self):
        # Update the score label
        self.score_label.config(text=f"Score: {self.score}")