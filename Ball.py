"""
Name: Daniel Gladkov
Date: 27/05/2020
"""
import pygame
import random
import time
pygame.init()

WHITE = (255, 255, 255)
speed = 16


class Ball:
    """
          A class that represents a ball

          Attributes
          ----------
          :var screen: The screen the ball is drawn on
          :type screen: pygame.display
          :var window_height: The height of the screen
          :type window_height: int
          :var window_width: The width of the screen
          :type window_width: int
          :var radius: The radius of the ball
          :type radius: int
          :var x: The X position of the ball
          :type x: int
          :var y: The Y position of the ball
          :type y: int
          :var speed_x: The horizontal speed of the ball
          :type speed_x: int
          :var score_y: The vertical speed of the ball
          :type score_y: int
          :var t: Tracks time for when ball is reset (timer)
          :type t: int

          Methods
          -------
          draw_self()
              draws the object

          respawn()
              reset all vars of the ball (x and y position and movement)

          move()
              attempts to move the ball: checks for collisions with walls or player and checks if a goal was made

          data()
              returns a string containing the x and y position (x,y)

          move_to()
               updates the ball to input data it receives
    """

    def __init__(self, screen):
        self.screen = screen
        self.window_height = screen.get_height()
        self.window_width = screen.get_width()
        self.radius = 25
        self.y = self.window_height // 2
        self.x = self.window_width // 2
        self.speed_x = 0
        self.speed_y = 0
        self.t = 0

    def respawn(self):
        self.y = self.window_height // 2
        self.x = self.window_width // 2
        self.speed_x = speed * random.choice([-1, 1]) + random.choice(range(-2,3))
        self.speed_y = speed // 2 * random.choice([-1, 1]) + random.choice(range(-2,3))
        self.draw_self()

    def draw_self(self):
        pygame.draw.circle(self.screen, WHITE, (self.x, self.y), self.radius)

    def move(self, player1, player2):
        if self.t < time.time():
            p1_pos = player1.get_position()
            p2_pos = player2.get_position()

            if self.y + self.speed_y >= self.window_height or self.y + self.speed_y <= 0:
                self.speed_y *= -1
            if p1_pos[0] + player1.get_width() > self.x + self.speed_x and p1_pos[0] < self.x and\
                    p1_pos[1] < self.y + self.radius and p1_pos[1] + player1.get_length() > self.y:
                self.speed_x *= -1
                if self.speed_y > 0:
                    self.speed_y += 1
                else:
                    self.speed_y -= 1
            elif p2_pos[0] < self.x + self.speed_x and p2_pos[0] + player2.get_width() > self.x and\
                    p2_pos[1] < self.y + self.radius and p2_pos[1] + player2.get_length() > self.y:
                self.speed_x *= -1
                if self.speed_y > 0:
                    self.speed_y += 1
                else:
                    self.speed_y -= 1
            if self.x + self.speed_x >= self.window_width:
                player1.goal()
                self.t = time.time() + 2
                self.respawn()
            elif self.x + self.speed_x <= 0:
                player2.goal()
                self.t = time.time() + 2
                self.respawn()
            else:
                self.y += self.speed_y
                self.x += self.speed_x

        self.draw_self()

    def data(self):
        data = str(self.x) + ',' + str(self.y)
        while len(data) < 10:
            data = data + ','
        return data

    def move_to(self, data):
        data = data.split(',')
        self.x = int(data[0])
        self.y = int(data[1])

