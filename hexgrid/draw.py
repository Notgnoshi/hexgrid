import itertools
import math
from tkinter import Tk, Canvas, ALL, BOTH

from hexgrid import Grid


class DrawGrid(Canvas):
    """
        Draws a Grid object for debugging purposes.
    """
    def __init__(self, grid, coords=None, radius=50, master=Tk()):
        """
            Draws the given Grid. If an iterable of coordinates is given, only draw the cells with
            the given coordinates. The default radius for the hexagonal cells is 50 pixels.
        """
        super().__init__(master=master, highlightthickness=0)
        self.height = self.winfo_height()
        self.width = self.winfo_width()
        self.bind("<Configure>", self.on_resize)
        self.grid = grid
        if coords is None:
            self.coords = grid.keys()
        else:
            self.coords = coords
        self.radius = radius

    def draw_hexagon(self, coord, label=False, fill='#7070ff'):
        """
            Draws a single hexagon at a given coordinate.
        """
        center = self.hex_to_pixel(coord, self.radius)
        vertices = self.hex_corners(center, self.radius)

        self.create_polygon(tuple(itertools.chain.from_iterable(vertices)),
                            fill=fill,
                            outline='black')

        if label:
            self.create_text(*center, text=f'{coord}')

    def draw_hexagons(self, coords, labels=False, fill='#7070ff'):
        """
            Draws a collection of hexagons.
        """
        for coord in coords:
            self.draw_hexagon(coord, labels, fill=fill)

    def on_resize(self, event):
        """
            Callback for resize events.
        """
        # determine the ratio of old width/height to new width/height
        wscale = event.width / self.width
        hscale = event.height / self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas
        self.config(width=self.width, height=self.height)
        # Make sure everything fits
        self.config(scrollregion=self.bbox(ALL))
        self.pack(fill=BOTH, expand=True)
        # Rescale everything to the new size
        self.scale(ALL, 0, 0, wscale, hscale)

    def draw(self):
        """
            Draws the Grid.
        """
        x0, y0, x1, y1 = self.bbox(ALL)
        self.width = x1 - x0
        self.height = y1 - y0
        self.config(height=self.height, width=self.width)
        self.config(scrollregion=self.bbox(ALL))
        self.pack(fill=BOTH, expand=True)
        self.master.mainloop()

    def hex_to_pixel(self, coord, radius):
        """
            Converts hexagonal coordinates to cartesian pixel coordinates for drawing on a screen.
        """
        q, r = Grid.convert(coord, self.grid.coordinate_system, 'axial')
        if self.grid.hexagon_type == 'pointy-topped':
            x = radius * math.sqrt(3) * (q + r / 2)
            y = radius * (3 / 2) * r
        else:
            x = radius * (3 / 2) * q
            y = radius * math.sqrt(3) * (r + q / 2)
        return x, y

    def hex_corners(self, coord, radius):
        """
            Given an (x, y) cartesian coordinate and a hexagon radius, returns
            a list of corner points.
        """
        x, y = coord
        corners = []

        if self.grid.hexagon_type == 'pointy-topped':
            for i in range(6):
                theta = (math.pi / 3) * i + math.pi / 6
                cx = x + radius * math.cos(theta)
                cy = y + radius * math.sin(theta)
                corners.append((cx, cy))
        else:
            for i in range(6):
                theta = (math.pi / 3) * i
                cx = x + radius * math.cos(theta)
                cy = y + radius * math.sin(theta)
                corners.append((cx, cy))

        return corners
