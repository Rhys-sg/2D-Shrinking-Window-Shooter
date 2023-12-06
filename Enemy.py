import math
import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import os

class Enemy:
    def __init__(self, canvas, game_window, x, y, speed, health):
        self.canvas = canvas
        self.game_window = game_window
        self.x = x
        self.y = y
        self.speed = speed
        self.enemy_size = 30   
        
        self.health = health
        self.starting_health = health
        self.health_bar_x_offset = 20
        self.health_bar_width = self.enemy_size + self.health_bar_x_offset
        self.health_bar_height = 5
        self.health_bar_y_offset = -20
        
        self.tick_count = 0

        # Load the GIF images using Pillow
        path = os.path.dirname(__file__)
        self.r_frames = self.load_gif_frames(path+"/Assets/r_crop.gif")
        self.l_frames = self.load_gif_frames(path+"/Assets/l_crop.gif")

        self.enemy_image = self.r_frames[0]

        # Animation variables
        self.animation_index = 0

        # Create the enemy as an image on the canvas
        self.visual = self.canvas.create_image(self.x + self.enemy_size/2, self.y + self.enemy_size/2, anchor="center", image=self.enemy_image)

        # Create a bounding/hurt box on the canvas
        self.bounding_box = self.canvas.create_rectangle(self.x, self.y, self.x + self.enemy_size, self.y + self.enemy_size, fill="red")
        self.canvas.itemconfig(self.bounding_box, state=tk.HIDDEN) # Hide the bounding box

        self.HB_base_x = self.x - self.health_bar_x_offset/2
        self.HB_base_y = self.y + self.health_bar_y_offset

        health_bar_coordinates = [self.HB_base_x, self.HB_base_y, self.HB_base_x + self.health_bar_width, self.HB_base_y + self.health_bar_height]

        self.health_bar_r = self.canvas.create_rectangle(*health_bar_coordinates, fill="red")
        self.health_bar_g = self.canvas.create_rectangle(*health_bar_coordinates, fill="green")


    def load_gif_frames(self, path):
        gif = Image.open(path)
        frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(gif)]
        return frames

    def move_towards_player(self):
        player_x, player_y, _, _ = self.canvas.coords(self.game_window.sprite.sprite)
        enemy_x, enemy_y = self.canvas.coords(self.visual)

        angle = math.atan2(player_y - enemy_y, player_x - enemy_x)
        dx = self.speed * math.cos(angle)
        dy = self.speed * math.sin(angle)

        # Move the enemy image
        self.x += dx
        self.y += dy
        self.canvas.move(self.visual, dx, dy)
        self.canvas.move(self.bounding_box, dx, dy)
        self.canvas.move(self.health_bar_r, dx, dy)
        self.canvas.move(self.health_bar_g, dx, dy)


        # Flip the enemy image horizontally if it is to the right of the player/reset the scaling if the enemy is to the left of the player
        if player_x < enemy_x:
            self.animate_enemy(self.l_frames)
        else:
            self.animate_enemy(self.r_frames)

    def animate_enemy(self, frames):

        # only update the animation every 5 ticks
        self.tick_count += 1
        if self.tick_count % 5 != 0:
            return

        if self.animation_index >= len(frames)-1:
            self.animation_index = 0
        else:
            self.animation_index += 1

        # Update the image
        self.enemy_image = frames[self.animation_index]
        self.canvas.itemconfig(self.visual, image=self.enemy_image)
        

    def delete_enemy(self):
        self.canvas.delete(self.visual)
        self.canvas.delete(self.bounding_box)
        self.canvas.delete(self.health_bar_r)
        self.canvas.delete(self.health_bar_g)

    def update_health(self):
        self.HB_base_x, self.HB_base_y, _, _ = self.canvas.coords(self.health_bar_g)
        health_bar_percentage = self.health/self.starting_health

        updated_health_bar_coordinates = [self.HB_base_x, self.HB_base_y, self.HB_base_x + (self.health_bar_width * health_bar_percentage), self.HB_base_y + self.health_bar_height]

        self.canvas.delete(self.health_bar_g)
        self.health_bar_g = self.canvas.create_rectangle(*updated_health_bar_coordinates, fill="green")