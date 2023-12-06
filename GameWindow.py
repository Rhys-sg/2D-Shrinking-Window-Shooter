import random
import tkinter as tk

import Sprite
import Enemy
import StartScreen

class GameWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Claustrophobia")

        self.width = 500
        self.height = 500

        # Center the window on the screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - self.width) // 2
        y = (screen_height - self.height) // 2
        self.geometry(f"{self.width}x{self.height}+{x}+{y}")

        # Create and place the score label
        self.score_label = tk.Label(self, text="", font=("Helvetica", 12)) # Initialize the label with an empty string to not display on startup
        self.score_label.pack(side=tk.TOP, anchor=tk.NW)

        self.canvas = tk.Canvas(self, width=self.width, height=self.height)
        self.canvas.pack()

        StartScreen.create_start_screen_objects(self, self.width, self.height)

        # Store the last key pressed
        self.last_key = ""

        self.high_score = 0

    def create_help_popup(self):
        # Dimensions and position of the popup
        popup_width = 300
        popup_height = 275
        popup_x = (self.width - popup_width) // 2
        popup_y = (self.height - popup_height) // 2 - 50

        # Create a rectangle as the background of the popup
        popup_rectangle = self.canvas.create_rectangle(
            popup_x, popup_y, popup_x + popup_width, popup_y + popup_height,
            fill="white", outline="black", tags="popup"
        )

        # Help text
        help_text = (
            "Welcome to Claustrophobia!\n\n"
            "Objective: Survive as long as possible by\nnot touching the walls and avoiding enemies.\n\n"
            "Controls:\n"
            "   - Use 'W', 'A', 'S', 'D' or arrow keys to move.\n"
            "   - Click the left mouse button to shoot.\n\n"
            "The walls will begin to close in on you, so\nshoot them to make them grow."
        )

        # Create a text item inside the popup rectangle
        text_x = popup_x + 20
        text_y = popup_y + 20
        help_text_item = self.canvas.create_text(
            text_x, text_y, text=help_text, font=("Helvetica", 10), anchor=tk.NW, tags="popup"
        )

        # Create a button to close the popup
        button_width = 80
        button_height = 30
        button_x = (self.width - button_width) // 2
        button_y = popup_y + popup_height - 40
        close_button = self.canvas.create_rectangle(
            button_x, button_y, button_x + button_width, button_y + button_height,
            fill="", outline="black", tags="popup"
        )
        close_text_x = button_x + button_width // 2
        close_text_y = button_y + button_height // 2
        close_text = self.canvas.create_text(
            close_text_x, close_text_y, text="Close", font=("Helvetica", 10, "bold"), tags="popup"
        )

        # Bind events to close the popup when the close button is clicked
        self.canvas.tag_bind(close_button, "<Button-1>", lambda event: self.close_help_popup())
        self.canvas.tag_bind(close_text, "<Button-1>", lambda event: self.close_help_popup())
        
        self.canvas.tag_bind(close_button, "<Enter>", lambda event: self.canvas.itemconfig(close_button, fill="lightgrey"))
        self.canvas.tag_bind(close_button, "<Leave>", lambda event: self.canvas.itemconfig(close_button, fill=""))
        self.canvas.tag_bind(close_text, "<Enter>", lambda event: self.canvas.itemconfig(close_button, fill="lightgrey"))
        self.canvas.tag_bind(close_text, "<Leave>", lambda event: self.canvas.itemconfig(close_button, fill=""))

    def close_help_popup(self):
        # Delete all items with the "popup" tag (rectangle, text, and button)
        self.canvas.delete("popup")


    def start_game(self):
        # controls need to be here so that they are not active on the start screen
        self.bind("w", lambda event: self.move_sprite(0, -self.move_distance))
        self.bind("s", lambda event: self.move_sprite(0, self.move_distance))
        self.bind("d", lambda event: self.move_sprite(self.move_distance, 0))
        self.bind("a", lambda event: self.move_sprite(-self.move_distance, 0))
        self.bind("<Button-1>", lambda event: self.fire_bullet())
        self.bind("<Down>", lambda event: self.move_sprite(0, self.move_distance))
        self.bind("<Right>", lambda event: self.move_sprite(self.move_distance, 0))
        self.bind("<Left>", lambda event: self.move_sprite(-self.move_distance, 0))
        self.bind("<Button-1>", lambda event: self.fire_bullet())

        self.sprite_size = 20

        self.enemies = []  # List to store enemy instances
        self.enemy_spawn_interval = 2000  # Time interval for spawning enemies in milliseconds
        self.enemy_speed = 1.5  # Speed of enemies

        self.shrink_interval = 100  # Time interval for shrinking in milliseconds
        self.game_tick_rate = 10  # Time interval for updating all other parts of the game in milliseconds
        self.decrement = 1  # Amount to shrink in each interval
        self.move_distance = 3  # Distance to move the sprite in each key press
        self.growth_increment = 10  # Amount to grow in each interval

        self.end_game_flag = False
        
        self.score = 0
        self.score_label.config(text=f"Score: {self.score}")
        
        self.canvas.itemconfig("start_image", state=tk.HIDDEN)
        self.canvas.itemconfig("title_text", text="")
        self.canvas.itemconfig("start_button", state=tk.HIDDEN)
        self.canvas.itemconfig("start_text", text="")
        self.canvas.itemconfig("help_button", state=tk.HIDDEN)
        self.canvas.itemconfig("help_text", text="")

        self.sprite = Sprite.Sprite(self.canvas, self.width, self.height, self.sprite_size)
        self.sprite.game_window = self  # Pass the reference to GameWindow to the Sprite

        # Show the sprite when the game starts
        self.sprite.show()

        self.update()
        self.shrink()
        self.spawn_enemies()

    def end_game(self):
        # Center the window on the screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - self.width) // 2
        y = (screen_height - self.height) // 2
        self.geometry(f"{self.width}x{self.height}+{x}+{y}")

        self.end_game_flag = True

        # Display game over message
        self.canvas.itemconfig("title_text", text="Game Over", font=("Helvetica", 28))
        
        self.high_score = max(self.high_score, self.score)
        self.canvas.itemconfig("help_text", text="Score: " + str(self.score) + "\n" + "  Best: " + str(self.high_score))
        self.canvas.itemconfig("start_text", text="Restart")
        self.canvas.itemconfig("start_text", state=tk.NORMAL)
        self.canvas.itemconfig("start_button", state=tk.NORMAL)
        self.canvas.itemconfig("help_text", state=tk.NORMAL)

        # Delete all enemies and bullets
        for enemy in self.enemies:
            enemy.delete_enemy()
        self.enemies = []
        for bullet in self.sprite.bullets:
            self.canvas.delete(bullet.bullet)
        self.sprite.bullets = []

        self.score_label.config(text="")
        self.score = 0

        # Hide the sprite and stop updating the game
        self.sprite.hide()
        self.after_cancel(self.update)

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
        if self.end_game_flag:
            return
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