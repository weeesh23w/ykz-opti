import random
import customtkinter as ctk


class PurpleStarsBackground:
    def __init__(self, parent, width=1200, height=700, stars=120):
        self.width = width
        self.height = height
        self.stars_total = stars

        self.canvas = ctk.CTkCanvas(parent,
                                    width=self.width,
                                    height=self.height,
                                    highlightthickness=0,
                                    bg="#050005")

        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)

        self.stars = []

        for _ in range(self.stars_total):
            self.stars.append(self.create_star())

        self.animate()

    def create_star(self):
        return {
            "x": random.uniform(-self.width, self.width),
            "y": random.uniform(-self.height, self.height),
            "z": random.uniform(0.1, self.width),
        }

    def animate(self):
        self.canvas.delete("all")

        cx = self.width / 2
        cy = self.height / 2

        for star in self.stars:

            star["z"] -= 4

            if star["z"] <= 1:
                star.update(self.create_star())

            k = 128 / star["z"]

            x = star["x"] * k + cx
            y = star["y"] * k + cy

            size = (1 - star["z"] / self.width) * 4

            color = "#9b30ff"

            self.canvas.create_oval(
                x,
                y,
                x + size,
                y + size,
                fill=color,
                outline=""
            )

        self.canvas.after(16, self.animate)


# Theme colors (purple)
COLOR_BG = "#050005"
COLOR_PANEL = "#120012"
COLOR_ACCENT = "#9b30ff"
COLOR_ACCENT_HOVER = "#7a1ed6"

if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    root = ctk.CTk()
    root.geometry("1200x700")
    root.configure(fg_color=COLOR_BG)

    # Fondo animado
    stars = PurpleStarsBackground(root)

    root.mainloop()
