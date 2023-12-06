import tkinter as tk


def create_start_screen_objects(self, width, height):
    button_width = 100
    button_height = 40
    x_padding = 10
    y_padding_upper = 15
    y_padding_lower = 30
    title_width = (button_width * 2) + x_padding
    title_font = 12

    # Load the image and store it as an instance variable
    original_image  = tk.PhotoImage(file="C:/Users/rsore/Documents/GitHub/2D-Shrinking-Window-Shooter/Assets/Icon_nobg.png")
    image_width, image_height = original_image.width(), original_image.height()

    new_width = 100
    new_height = 100

    # Calculate the subsample factor to resize the image
    subsample_factor = max(1, image_width // new_width, image_height // new_height)
    resized_image = original_image.subsample(subsample_factor)

    # Store the resized image as an instance variable
    self.photo = resized_image

    # Create an image item on canvas
    image_x = self.width // 2
    image_y = self.height // 2 - title_font - new_height - y_padding_upper - y_padding_lower
    self.canvas.create_image(image_x, image_y, anchor=tk.N, image=self.photo, tags="start_image")

    title_button_x = ((self.width - button_width) // 2) - button_width // 2 - x_padding // 2
    title_button_y = self.height // 2 - title_font - y_padding_lower
    title_text_x = title_button_x + title_width // 2
    title_text_y = title_button_y + title_font // 2
    self.canvas.create_text(title_text_x, title_text_y, text="CLAUSTROPHOBIA", font=("Helvetica", title_font, "bold"), tags="title_text")

    start_button_x = ((self.width - button_width) // 2)  - button_width // 2 - x_padding // 2
    start_button_y = self.height // 2
    self.canvas.create_rectangle(start_button_x, start_button_y, start_button_x + button_width, start_button_y + button_height, outline="black", tags="start_button")
    start_text_x = start_button_x + button_width // 2
    start_text_y = start_button_y + button_height // 2
    self.canvas.create_text(start_text_x, start_text_y, text="Start", font=("Helvetica", 12, "bold"), tags="start_text")
    self.canvas.tag_bind("start_button", "<Button-1>", lambda event: self.start_game())
    self.canvas.tag_bind("start_text", "<Button-1>", lambda event: self.start_game())
    self.canvas.tag_bind("start_button", "<Enter>", lambda event: self.canvas.itemconfig("start_button", fill="lightgrey"))
    self.canvas.tag_bind("start_button", "<Leave>", lambda event: self.canvas.itemconfig("start_button", fill=""))
    self.canvas.tag_bind("start_text", "<Enter>", lambda event: self.canvas.itemconfig("start_button", fill="lightgrey"))
    self.canvas.tag_bind("start_text", "<Leave>", lambda event: self.canvas.itemconfig("start_button", fill=""))

    help_button_x = ((self.width - button_width) // 2) + button_width // 2 + x_padding // 2
    help_button_y = self.height // 2
    self.canvas.create_rectangle(help_button_x, help_button_y, help_button_x + button_width, help_button_y + button_height, outline="black", tags="help_button")
    help_text_x = help_button_x + button_width // 2
    help_text_y = help_button_y + button_height // 2
    self.canvas.create_text(help_text_x, help_text_y, text="Info", font=("Helvetica", 12, "bold"), tags="help_text")
    self.canvas.tag_bind("help_button", "<Button-1>", lambda event: self.create_help_popup())
    self.canvas.tag_bind("help_text", "<Button-1>", lambda event: self.create_help_popup())
    self.canvas.tag_bind("help_button", "<Enter>", lambda event: self.canvas.itemconfig("help_button", fill="lightgrey"))
    self.canvas.tag_bind("help_button", "<Leave>", lambda event: self.canvas.itemconfig("help_button", fill=""))
    self.canvas.tag_bind("help_text", "<Enter>", lambda event: self.canvas.itemconfig("help_button", fill="lightgrey"))
    self.canvas.tag_bind("help_text", "<Leave>", lambda event: self.canvas.itemconfig("help_button", fill=""))