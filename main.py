import pygame
import random
import os

# Pygame এবং Mixer ইনিশিয়ালাইজেশন
pygame.init()
pygame.mixer.init()

# স্ক্রিন সেটআপ
width, height = 600, 700 
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("SUPER BIKE RACE - CREATED BY GOPAL")

# রঙসমূহ
WHITE, YELLOW, RED, ORANGE, BLACK, GOLD, BLUE, GREEN_P = (255, 255, 255), (255, 255, 0), (200, 0, 0), (255, 165, 0), (0, 0, 0), (255, 215, 0), (0, 191, 255), (0, 255, 0)

# ফন্ট
font_main = pygame.font.SysFont("Arial", 50, bold=True)
font_small = pygame.font.SysFont("Arial", 25, bold=True)

# ডাটা সেভ/লোড (High Score, Total Coins, Unlocked Bikes)
def load_data():
    if not os.path.exists("gamedata.txt"): 
        return 0, 0, "default" # হাই স্কোর, মোট কয়েন, বর্তমান বাইক
    with open("gamedata.txt", "r") as f:
        try:
            lines = f.readlines()
            return int(lines[0].strip()), int(lines[1].strip()), lines[2].strip()
        except: return 0, 0, "default"

def save_data(h_score, t_coins, current_bike):
    with open("gamedata.txt", "w") as f:
        f.write(f"{h_score}\n{t_coins}\n{current_bike}")

# ছবি লোড
try:
    bike_img = pygame.image.load('bike.png').convert_alpha()
    bike_img = pygame.transform.scale(bike_img, (55, 85)) 
    car_img = pygame.image.load('car.png').convert_alpha()
    car_img.set_colorkey((255, 255, 255))
    car_img = pygame.transform.rotate(car_img, -90)
    car_img = pygame.transform.scale(car_img, (45, 90))
    pygame.mixer.music.load('music.mp3')
except: bike_img = car_img = None

def draw_road(offset, level):
    grass_c = [(34, 139, 34), (194, 178, 128), (20, 20, 20)][((level-1)//10)%3]
    screen.fill(grass_c)
    pygame.draw.rect(screen, (50, 50, 50), [100, 0, 400, height])
    for i in range(-100, height, 100):
        pygame.draw.rect(screen, WHITE, [300, i + offset, 5, 50])

# --- শপ মেনু ফাংশন ---
def shop_menu():
    h_score, t_coins, current_bike = load_data()
    while True:
        screen.fill((20, 20, 20))
        screen.blit(font_main.render("BIKE SHOP", True, GOLD), (width//2-120, 50))
        screen.blit(font_small.render(f"COINS: {t_coins}", True, YELLOW), (width//2-50, 120))
        
        # বাইক অপশন ১ (ফ্রি)
        pygame.draw.rect(screen, GRAY if current_bike == "default" else BLACK, [150, 200, 300, 80])
        screen.blit(font_small.render("1. Classic Bike (Owned)", True, WHITE), (170, 225))
        
        # বাইক অপশন ২ (৫০০ কয়েন)
        pygame.draw.rect(screen, GRAY if current_bike == "red" else BLACK, [150, 300, 300, 80])
        screen.blit(font_small.render("2. Red Racer (500 Coins)", True, RED), (170, 325))
        
        screen.blit(font_small.render("Press 'B' to Go Back", True, WHITE), (width//2-100, 600))
        
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b: return
                if event.key == pygame.K_2 and t_coins >= 500:
                    current_bike = "red"
                    save_data(h_score, t_coins - 500, current_bike)

def start_menu():
    while True:
        h_score, t_coins, bike = load_data()
        screen.fill(BLACK)
        screen.blit(font_small.render("CREATED BY GOPAL", True, RED), (width//2-100, 50))
        screen.blit(font_main.render("START BIKE RACE", True, YELLOW), (width//2-180, 200))
        
        # বাটনসমূহ
        pygame.draw.rect(screen, GRAY, [width//2-100, 400, 200, 50])
        screen.blit(font_small.render("PLAY GAME", True, WHITE), (width//2-60, 410))
        
        pygame.draw.rect(screen, GRAY, [width//2-100, 480, 200, 50])
        screen.blit(font_small.render("OPEN SHOP", True, WHITE), (width//2-60, 490))
        
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if width//2-100 <= mx <= width//2+100:
                    if 400 <= my <= 450: return # Play
                    if 480 <= my <= 530: shop_menu() # Shop

def game_loop():
    h_score, total_bank_coins, bike_type = load_data()
    bike_x, bike_y = 275, 550
    score, current_coins, nitro_fuel = 0, 0, 100
    shield_timer = 0
    
    # বাইকের রঙ পরিবর্তন
    current_bike_img = bike_img
    if bike_type == "red":
        current_bike_img.fill((255, 0, 0), special_flags=pygame.BLEND_RGB_ADD)

    enemies = [[random.randint(110, 445), random.randint(-800, -100)] for _ in range(4)]
    coins = [[random.randint(110, 445), random.randint(-1000, -200)] for _ in range(2)]
    powers = [[random.randint(110, 445), random.randint(-3000, -1000), "N"]]
    
    clock = pygame.time.Clock()
    road_off = 0

    while True:
        level = (score // 10) + 1
        mouse_pos = pygame.mouse.get_pos()
        mouse_press = pygame.mouse.get_pressed()
        
        using_nitro = mouse_press[0] and mouse_pos[1] < 200 and nitro_fuel > 0
        speed = (7 + level*0.3) * (1.7 if using_nitro else 1)
        if using_nitro: nitro_fuel -= 1
        elif nitro_fuel < 100: nitro_fuel += 0.1

        if mouse_press[0]:
            if mouse_pos[0] < width//2 and bike_x > 105: bike_x -= 9
            if mouse_pos[0] > width//2 and bike_x < 445: bike_x += 9

        road_off = (road_off + speed) % 100
        draw_road(road_off, level)

        # কয়েন ও পাওয়ার-আপ লজিক (আগের মতই)
        for c in coins:
            c[1] += speed
            if c[1] > height: c[1], c[0] = random.randint(-500, -100), random.randint(110, 445)
            pygame.draw.circle(screen, GOLD, (c[0], c[1]), 12)
            if abs(bike_x+27-c[0]) < 30 and abs(bike_y+40-c[1]) < 40:
                current_coins += 1; c[1] = -100

        for e in enemies:
            e[1] += speed
            if e[1] > height: e[1], e[0] = random.randint(-600, -100), random.randint(110, 445); score += 1
            if car_img: screen.blit(car_img, (e[0], e[1]))
            if abs(bike_x+27-(e[0]+22)) < 35 and abs(bike_y+40-(e[1]+45)) < 50:
                save_data(max(h_score, score), total_bank_coins + current_coins, bike_type)
                return

        if bike_img: screen.blit(current_bike_img, (bike_x, bike_y))
        
        pygame.display.update()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); exit()

GRAY = (100, 100, 100)
while True:
    start_menu()
    game_loop()