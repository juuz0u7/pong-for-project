import pygame.freetype
import pygame

pygame.init()

icon = pygame.image.load("image/ping_pong.ico")
pong = pygame.mixer.Sound("music/pong.wav")
score = pygame.mixer.Sound("music/score.wav")
win = pygame.mixer.Sound("music/win.wav")
lose = pygame.mixer.Sound("music/lose.wav")

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 500
START_game = 0
main_font = pygame.freetype.Font(None, 42)
font = pygame.font.SysFont('Arial', 40)
objects = []
objects_lvl = []
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()
pygame.display.set_caption("Pong")
pygame.display.set_icon(icon)
button_time = 0


