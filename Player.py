"""
Name: Daniel Gladkov
Date: 27/05/2020
"""
import pygame

pygame.init()

WHITE = (255, 255, 255)
SCORE_TO_WIN = 5
speed = 18
font = pygame.font.SysFont('Comic Sans MS', 125)


class Player:
    """
          A class that represents a player

          Attributes
          ----------
          :var screen: The screen the player is drawn on
          :type screen: pygame.display
          :var window_height: The height of the screen
          :type window_height: int
          :var length: The length of the player
          :type length: int
          :var width: The width of the player
          :type width: int
          :var x: The X position of the player
          :type x: int
          :var y: The Y position of the player
          :type y: int
          :var speed: The speed of the player (vertical only)
          :type speed: int
          :var go_up: Does the player go up?
          :type go_up: boolean
          :var go_down: Does the player go down?
          :type go_down: boolean
          :var score: The score of the player
          :type score: int
          :var name: The identifying name of the player (left/right)
          :type name: string
          :var win: The win screen of the player (left/right)
          :type win: function

          Methods
          -------
          draw_self()
              draws the object

          move()
              attempts to move the object up/down

          up()
              makes the player move up

          down()
              makes the player move down

          stopup()
              stops the player from going up

          stopdown()
              stops the player from going down

          stop()
              attempts to stop the player completely

          goal()
              increases score by one

          check_win()
              returns True if the current player score is equal or greater then SCORE_TO_WIN, else False

          draw_score()
              draws the current player score at their side

          reset()
              reset all vars of the player (x and y position, score and movement)

          data()
              returns a string containing the x and y position and its score (x,y,score)

          move_to()
               updates the player to input data it receives
      """

    def __init__(self, screen, x, name, win_screen):
        self.screen = screen
        self.window_height = screen.get_height()
        self.length = 150
        self.width = 25
        self.y = (self.window_height - self.length) // 2
        self.x = x
        self.speed = 0
        self.go_up = False
        self.go_down = False
        self.score = 0
        self.name = name
        self.win = win_screen

    def draw_self(self):
        pygame.draw.rect(self.screen, WHITE, (self.x, self.y, self.width, self.length))
        self.draw_score()

    def move(self):
        self.y += self.speed
        if self.y > (self.window_height - self.length):
            self.y = (self.window_height - self.length)
        elif self.y < 0:
            self.y = 0

    def up(self):
        self.go_up = True
        self.speed = -speed

    def down(self):
        self.go_down = True
        self.speed = speed

    def stopup(self):
        self.go_up = False
        self.stop()

    def stopdown(self):
        self.go_down = False
        self.stop()

    def stop(self):
        if not self.go_down and not self.go_up:
            self.speed = 0

    def get_position(self):
        return self.x, self.y

    def get_length(self):
        return self.length

    def get_width(self):
        return self.width

    def goal(self):
        self.score += 1

    def check_win(self):
        return self.score >= SCORE_TO_WIN

    def draw_score(self):
        score = font.render(str(self.score), False, WHITE)
        if self.name == "Right Player":
            self.screen.blit(score, (self.screen.get_width() - self.screen.get_width() // 4, 0))
        else:
            self.screen.blit(score, (self.screen.get_width() // 4, 0))

    def reset(self):
        self.y = (self.window_height - self.length) // 2
        self.go_up = False
        self.go_down = False
        self.score = 0
        self.stop()

    def data(self):
        data = str(self.x) + ',' + str(self.y) + ',' + str(self.score)
        while len(data) < 10:
            data = data + ','
        return data

    def move_to(self, data):
        data = data.split(',')
        self.x = int(data[0])
        self.y = int(data[1])
        self.score = int(data[2])
