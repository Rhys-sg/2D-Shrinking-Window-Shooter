import math
import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import os

import Bullet

class Sprite:
    def __init__(self, canvas, width, height, sprite_size):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.sprite_size = sprite_size

        # Initialize sprite velocity and damping factor
        self.sprite_dx = 0
        self.sprite_dy = 0
        self.damping = 0.985

        # Initialize bullet variables
        self.bullet_speed = 10
        self.bullets = []

        self.sprite = self.canvas.create_rectangle(0, 0, sprite_size, sprite_size, fill="blue")
        self.canvas.move(self.sprite, (width - sprite_size) / 2, (height - sprite_size) / 2)
        self.canvas.itemconfig(self.sprite, state=tk.HIDDEN)

        self.tick_count = 0

        # Load the GIF images using Pillow
        path = os.path.dirname(__file__)
        self.r_frames = self.load_gif_frames(path+"/Assets/r_crop.gif")
        self.l_frames = self.load_gif_frames(path+"/Assets/l_crop.gif")

        self.image = self.r_frames[0]

        # Animation variables
        self.s_animation_index = 0

        # Create an image on the canvas
        self.visual = self.canvas.create_image((width - sprite_size) / 2, (height - sprite_size) / 2, anchor="center", image=self.image)

    def load_gif_frames(self, path):
        gif = Image.open(path)
        frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(gif)]
        return frames

    def animate(self, frames):

        # only update the animation every 5 ticks
        self.tick_count += 1
        if self.tick_count % 5 != 0:
            return

        if self.s_animation_index >= len(frames)-1:
            self.s_animation_index = 0
        else:
            self.s_animation_index += 1

        # Update the image
        self.image = frames[self.s_animation_index]
        self.canvas.itemconfig(self.visual, image=self.image)

    def show(self):
        self.canvas.itemconfig(self.visual, state=tk.NORMAL)

    def hide(self):
        self.canvas.itemconfig(self.visual, state=tk.HIDDEN)

    def move(self):
        current_x, current_y, _, _ = self.canvas.coords(self.sprite)
        new_x = current_x + self.sprite_dx
        new_y = current_y + self.sprite_dy

        # Boundary checks to prevent moving past the edge
        if new_x < 0:
            new_x = 0
        elif new_x + self.sprite_size > self.width:
            new_x = self.width - self.sprite_size

        if new_y < 0:
            new_y = 0
        elif new_y + self.sprite_size > self.height:
            new_y = self.height - self.sprite_size

        self.canvas.coords(self.sprite, new_x, new_y, new_x + self.sprite_size, new_y + self.sprite_size)
        self.canvas.coords(self.visual, new_x + self.sprite_size / 2, new_y + self.sprite_size / 2)

        # Apply damping to simulate friction
        self.sprite_dx *= self.damping
        self.sprite_dy *= self.damping

        # Flip the image horizontally if the sprite is to the right of the mouse/ the scaling if the enemy is to the left of the player
        mouse_x = self.canvas.winfo_pointerx() - self.canvas.winfo_rootx()
        if new_x > mouse_x:
            self.animate(self.l_frames)
        else:
            self.animate(self.r_frames)

    def fire_bullet(self):
        current_x, current_y, _, _ = self.canvas.coords(self.sprite)

        # Get the mouse coordinates
        mouse_x = self.canvas.winfo_pointerx() - self.canvas.winfo_rootx()
        mouse_y = self.canvas.winfo_pointery() - self.canvas.winfo_rooty()

        # Calculate the direction towards the mouse
        angle = math.atan2(mouse_y - current_y - self.sprite_size / 2, mouse_x - current_x - self.sprite_size / 2)
        dx = self.bullet_speed * math.cos(angle)
        dy = self.bullet_speed * math.sin(angle)

        bullet = Bullet.Bullet(self.canvas, self.game_window, current_x + self.sprite_size / 2, current_y + self.sprite_size / 2, dx, dy)
        self.bullets.append(bullet)