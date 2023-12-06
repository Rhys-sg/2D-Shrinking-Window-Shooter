class Bullet:
    def __init__(self, canvas, game_window, x, y, dx, dy):
        self.canvas = canvas
        self.game_window = game_window
        self.bullet_size = 5
        self.bullet = self.canvas.create_oval(x, y, x + self.bullet_size, y + self.bullet_size, fill="black")
        self.dx = dx
        self.dy = dy
        self.delete_flag = False

    def move(self):
        if self.delete_flag:
            return

        current_x, current_y, _, _ = self.canvas.coords(self.bullet)
        new_x = current_x + self.dx
        new_y = current_y + self.dy

        # Check if the bullet is outside the canvas
        if (
            new_x < 0 or
            new_y < 0 or
            new_x + self.bullet_size > self.game_window.width or
            new_y + self.bullet_size > self.game_window.height
        ):
            # Determine the direction of the edge and call grow
            if new_x < 0:
                self.game_window.grow("left")
            elif new_y < 0:
                self.game_window.grow("up")
            elif new_x + self.bullet_size > self.game_window.width:
                self.game_window.grow("right")
            elif new_y + self.bullet_size > self.game_window.height:
                self.game_window.grow("down")

            # Mark the bullet for deletion
            self.delete_flag = True

            # Delay the deletion to avoid interference with grow
            self.canvas.after(1, self.delete_bullet)
            return

        self.canvas.coords(self.bullet, new_x, new_y, new_x + self.bullet_size, new_y + self.bullet_size)

    def delete_bullet(self):
        self.canvas.delete(self.bullet)