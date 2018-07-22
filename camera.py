import pygame

class Camera():
    def __init__(self, x, y, width, height, target, x_min, y_min, x_max, y_max):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.target = target
        self.x_max = x_max
        self.x_min = x_min
        self.y_max = y_max
        self.y_min = y_min

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        self.x = self.target.x - (self.width/2)
        self.y = self.target.y - (self.height/2)

        if self.x < self.x_min:
            self.x = self.x_min
        if self.y < self.y_min:
            self.y = self.y_min
        if self.x > self.x_max - self.width:
            self.x = self.x_max - self.width
        if self.y > self.y_max - self.height:
            self.y = self.y_max - self.height
