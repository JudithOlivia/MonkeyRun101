import pygame
import random
import json
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # temporary folder when running .exe
    except Exception:
        base_path = os.path.abspath(".")  # when running .py normally
    return os.path.join(base_path, relative_path)


pygame.init()

WIDTH, HEIGHT = 800, 400
FPS = 60

score = 0
high_score = 0
show_new_high_score = False
show_new_high_score_time = 0
SCORE_RATE = 5

GREEN = (34, 177, 76)
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
RED = (255, 0, 0)          
GRAY = (120, 120, 120)     
BLUE = (0, 100, 255)      
BLACK = (0, 0, 0)

GROUND_HEIGHT = 60
PLAYER_WIDTH, PLAYER_HEIGHT = 40, 60
INIT_SPEED = 4

screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Load images with error handling
try:
    background_img = pygame.image.load("StartBG.png").convert()
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
except:
    background_img = pygame.Surface((WIDTH, HEIGHT))
    background_img.fill(GREEN)

try:
    background1_img = pygame.image.load("Background.png").convert()
    background1_img = pygame.transform.scale(background1_img, (WIDTH, HEIGHT))
except:
    background1_img = pygame.Surface((WIDTH, HEIGHT))
    background1_img.fill(BLUE)

try:
    player_image = pygame.image.load("Player2.png").convert()
    player_image = pygame.transform.scale(player_image, (PLAYER_WIDTH, PLAYER_HEIGHT))
except:
    player_image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
    player_image.fill(RED)

try:
    ground_img = pygame.image.load("Ground.png").convert_alpha()
    ground_img = pygame.transform.scale(ground_img, (WIDTH, GROUND_HEIGHT))
except:
    ground_img = pygame.Surface((WIDTH, GROUND_HEIGHT))
    ground_img.fill(BROWN)

pygame.display.set_caption("Monkey Run")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 60)
small_font = pygame.font.SysFont(None, 32)

login_button = pygame.Rect(WIDTH - 100, 10, 80, 30)
ground_scroll_x = 0 

class Player:
    def __init__(self):
        try:
            self.image = pygame.image.load("Player2.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))
        except:
            self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
            self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = 100 
        self.rect.y = HEIGHT - GROUND_HEIGHT - self.rect.height + 10
        self.vel_y = 0
        self.jump_count = 0
        self.on_island = False

    def update(self):
        self.vel_y += 1  
        self.rect.y += self.vel_y

        if self.rect.bottom >= HEIGHT - GROUND_HEIGHT:
            self.rect.bottom = HEIGHT - GROUND_HEIGHT
            self.vel_y = 0
            self.jump_count = 0
            self.on_island = False

    def jump(self):
        if self.jump_count < 2:
            if self.jump_count == 0:
                self.vel_y = -15
            elif self.jump_count == 1:
                self.vel_y = -20
            self.jump_count += 1
            self.on_island = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Obstacle:
    def __init__(self, type_):
        self.type = type_
        if type_ == 'rock':
            self.width = PLAYER_WIDTH + 50  
            self.height = PLAYER_HEIGHT - 20 
            try:
                self.image = pygame.image.load("snake.png").convert_alpha()
                self.image = pygame.transform.scale(self.image, (self.width, self.height))
            except:
                self.image = pygame.Surface((self.width, self.height))
                self.image.fill(GRAY)
            self.rect = self.image.get_rect()
            self.rect.x = WIDTH
            self.rect.y = HEIGHT - GROUND_HEIGHT - self.height + 10
        elif type_ == 'floating':
            self.width = PLAYER_WIDTH + 60
            self.height = PLAYER_HEIGHT + 10
            try:
                self.image = pygame.image.load("float.png").convert_alpha()
                self.image = pygame.transform.scale(self.image, (self.width, self.height))
            except:
                self.image = pygame.Surface((self.width, self.height))
                self.image.fill(BLUE)
            self.rect = pygame.Rect(WIDTH, HEIGHT - GROUND_HEIGHT - self.height - 140, self.width, self.height)
        elif type_ == 'thorn':
            self.width = PLAYER_WIDTH - 10
            self.height = PLAYER_HEIGHT + 0.2
            try:
                self.image = pygame.image.load("Thorn.png").convert_alpha()
                self.image = pygame.transform.scale(self.image, (self.width, self.height))
            except:
                self.image = pygame.Surface((self.width, self.height))
                self.image.fill(RED)
            self.rect = self.image.get_rect()
            self.rect.x = WIDTH
            self.rect.y = HEIGHT - GROUND_HEIGHT - self.height + 10
        elif type_ == 'lake':
            self.width = 100
            self.height = GROUND_HEIGHT + 30
            try:
                self.image = pygame.image.load("lake.png").convert_alpha()
                self.image = pygame.transform.scale(self.image, (self.width, self.height))
            except:
                self.image = pygame.Surface((self.width, self.height))
                self.image.fill(BLUE)
            self.rect = pygame.Rect(WIDTH, HEIGHT - GROUND_HEIGHT - self.height + GROUND_HEIGHT - 10, self.width , self.height )
        else:
            self.width = 40
            self.height = 40
            self.rect = pygame.Rect(WIDTH, HEIGHT - GROUND_HEIGHT - self.height, self.width, self.height)

    def move(self, speed):
        if self.type == 'floating':
            self.rect.x -= speed * 1.5
        elif self.type == 'rock':
            self.rect.x -= speed * 1.75
        else:
            self.rect.x -= speed

    def draw(self, surface):
        if hasattr(self, 'image'):
            surface.blit(self.image, self.rect)
        else:
            pygame.draw.rect(surface, (255, 0, 0), self.rect)

def generate_obstacle(existing_obstacles):
    lake_present = any(obs.type == 'lake' for obs in existing_obstacles)

    if lake_present:
        return Obstacle('thorn')

    return Obstacle(random.choice(['thorn', 'rock', 'lake', 'floating']))

def draw_start_screen():
    screen.blit(background_img, (0, 0))
    title1 = font.render("MONKEY", True, WHITE)
    title2 = font.render("RUN", True, WHITE)
    instr = small_font.render("Press SPACE to start", True, WHITE)

    screen.blit(title1, title1.get_rect(center=(WIDTH//2, 100)))
    screen.blit(title2, title2.get_rect(center=(WIDTH//2, 160)))
    screen.blit(instr, instr.get_rect(center=(WIDTH//2, HEIGHT-100)))

    pygame.draw.rect(screen, WHITE, login_button)
    login_text = small_font.render("Login", True, BLACK)
    screen.blit(login_text, (login_button.x + 10, login_button.y + 5))

    pygame.display.update()

def draw_lose_screen():
    screen.fill(BLACK)
    lost = font.render("You Lost :(", True, WHITE)
    retry_text = small_font.render("Press R to Retry", True, WHITE)
    screen.blit(lost, lost.get_rect(center=(WIDTH//2, HEIGHT//2 - 30)))
    screen.blit(retry_text, retry_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 20)))
    pygame.display.update()

def load_high_score(email):
    try:
        if os.path.exists("scores.json"):
            with open("scores.json", "r") as f:
                # Check if file is not empty
                if os.path.getsize("scores.json") > 0:
                    scores = json.load(f)
                    return scores.get(email, 0)
    except (json.JSONDecodeError, Exception) as e:
        print(f"Error loading high score: {e}")
        # If there's an error, create a new empty file
        with open("scores.json", "w") as f:
            json.dump({}, f)
    return 0

def save_high_score(email, score):
    try:
        scores = {}
        if os.path.exists("scores.json") and os.path.getsize("scores.json") > 0:
            with open("scores.json", "r") as f:
                scores = json.load(f)
        
        scores[email] = max(scores.get(email, 0), score)
        
        with open("scores.json", "w") as f:
            json.dump(scores, f)
    except Exception as e:
        print(f"Error saving high score: {e}")

logged_in = False
name = ""
email = ""
high_score = 0
new_high_score_shown = False

def main():
    global score, high_score, show_new_high_score, show_new_high_score_time, name, email, ground_scroll_x, new_high_score_shown, logged_in

    player = Player()
    obstacles = [generate_obstacle([])]
    lives = 3
    speed = INIT_SPEED
    started = False
    lost = False

    invincible = False
    hit_timer = 0
    INVINCIBILITY_DURATION = 1500

    last_speed_increase = 0

    score = 0
    show_new_high_score = False
    show_new_high_score_time = 0

    while True:
        clock.tick(FPS)
        current_time = pygame.time.get_ticks()

        if not started:
            draw_start_screen()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if login_button.collidepoint(event.pos):
                        name = get_text_input("Enter Name:")
                        email = get_text_input("Enter Email:")
                        high_score = load_high_score(email)
                        logged_in = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        started = True

        if started and not lost:
            score += SCORE_RATE * (1 / FPS)

        if logged_in and score > high_score:
            high_score = score
            if not new_high_score_shown:
                show_new_high_score = True
                show_new_high_score_time = current_time
                new_high_score_shown = True

        if started and not lost and current_time - last_speed_increase >= 5000:
            speed += 0.2
            last_speed_increase = current_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if not started and event.key == pygame.K_SPACE:
                    started = True
                elif started and not lost and event.key in [pygame.K_SPACE, pygame.K_UP, pygame.K_w, pygame.K_e]:
                    player.jump()
                elif lost and event.key == pygame.K_r:
                    player = Player()
                    obstacles = [generate_obstacle([])]
                    lives = 3
                    speed = INIT_SPEED
                    lost = False
                    started = False
                    invincible = False
                    hit_timer = 0
                    score = 0
                    new_high_score_shown = False

        if not started:
            continue

        if lost:
            draw_lose_screen()
            continue

        screen.blit(background1_img, (0, 0))
        ground_scroll_x -= speed
        if ground_scroll_x <= -WIDTH:
            ground_scroll_x = 0

        screen.blit(ground_img, (ground_scroll_x, HEIGHT - GROUND_HEIGHT))
        screen.blit(ground_img, (ground_scroll_x + WIDTH, HEIGHT - GROUND_HEIGHT))

        player.update()

        if not invincible or (current_time // 100 % 2 == 0):
            player.draw(screen)

        if invincible and current_time - hit_timer >= INVINCIBILITY_DURATION:
            invincible = False

        if not obstacles or obstacles[-1].rect.x < WIDTH - 300:
            obstacles.append(generate_obstacle(obstacles))

        for obs in obstacles[:]:
            obs.move(speed)
            obs.draw(screen)

            if obs.rect.right < 0:
                obstacles.remove(obs)

            if not invincible and player.rect.colliderect(obs.rect):
                if obs.type == 'floating':
                    player_bottom = player.rect.bottom
                    island_top = obs.rect.top
                    if player.vel_y >= 0 and abs(player_bottom - island_top) <= 15 and player.jump_count == 2:
                        player.rect.bottom = island_top
                        player.vel_y = 0
                        player.jump_count = 2
                        player.on_island = True
                    else:
                        lives -= 1
                        invincible = True
                        hit_timer = current_time
                        if lives <= 0:
                            if logged_in:
                                save_high_score(email, int(score))
                            lost = True
                        else:
                            player.rect.x = 100
                            player.rect.y = HEIGHT - GROUND_HEIGHT - PLAYER_HEIGHT
                            player.vel_y = 0
                            player.jump_count = 0
                            player.on_island = False
                        break
                else:
                    lives -= 1
                    invincible = True
                    hit_timer = current_time
                    if lives <= 0:
                        if logged_in:
                            save_high_score(email, int(score))
                        lost = True
                    else:
                        player.rect.x = 100
                        player.rect.y = HEIGHT - GROUND_HEIGHT - PLAYER_HEIGHT
                        player.vel_y = 0
                        player.jump_count = 0
                        player.on_island = False
                    break

        lives_text = small_font.render(f"Lives: {lives}", True, WHITE)
        screen.blit(lives_text, (10, 10))

        score_text = small_font.render(f"Score: {int(score)}", True, WHITE)
        screen.blit(score_text, (WIDTH - 160, 10))

        if logged_in:
            high_score_text = small_font.render(f"High Score: {int(high_score)}", True, WHITE)
            screen.blit(high_score_text, (WIDTH - 160, 40))

        BLINK_INTERVAL = 300

        if logged_in and show_new_high_score and current_time - show_new_high_score_time <= 2500:
            if (current_time // BLINK_INTERVAL) % 2 == 0:
                popup_text = font.render("New High Score!", True, (255, 215, 0))
                screen.blit(popup_text, popup_text.get_rect(center=(WIDTH // 2, 30)))
        else:
            show_new_high_score = False

        pygame.display.update()

def get_text_input(prompt_text):
    input_box = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 32)
    active = True
    user_text = ""
    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return ""
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return user_text
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode

        screen.fill((0, 0, 0))
        prompt = font.render(prompt_text, True, WHITE)
        screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2 - 50))

        pygame.draw.rect(screen, WHITE, input_box, 2)
        txt_surface = small_font.render(user_text, True, WHITE)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()