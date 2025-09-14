import pygame
import random
import json
import os
import pygame

pygame.init()
screen = pygame.display.set_mode((640,480))
pygame.display.set_caption("Monket Run")


WIDTH, HEIGHT = 800, 400
FPS = 60

score = 0
high_score = 0
show_new_high_score = Falseshow_new_hogh_score_time = 0
SCORE_RATE = 5 

GREEN = (34, 177, 76)
WHITE = (255, 255, 255)



