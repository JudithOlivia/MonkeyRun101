import pygame
import random
import json
import os
import pygame

pygame.init()
screen = pygame.display.set_mode((640,480))
pygame.display.set_caption("Monkey Run")


WIDTH, HEIGHT = 800, 400
FPS = 60


GREEN = (34, 177, 76)
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
RED = (255, 0, 0)
GRAY = (120, 120, 120)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

GROUND_HEIGHT = 60
PLAYER_WIDTH, PLAYER_HEIGHT = 40, 60
INIT_SPEED = 4

screen = pygame.display.set_mode((WIDTH, HEIGHT))

background_img = pygame.image.load("StartBG.png").convert()
background_img = pygame.transform.scale(background_img (WIDTH, HEIGHT))

background1_img = pygame.imager.load("Baclground.png").convert()
background1_img = pygame.transform.scale(background1_img, (WIDTH, HEIGHT))

player_image = pygame.image.load("Player2.png").convert()
player_image = pygame.transform.scale(player_image, (PLAYER_WIDTH, PLAYER_HEIGHT))

ground_image = pygame.image.load("Ground.png").convert_alpha()
ground_image = pygame.transform.scale(ground_image, (WIDTH, GROUND_HEIGHT))

