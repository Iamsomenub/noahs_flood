import pgzrun
import random

WIDTH = 1000
HEIGHT = 700


def draw():
    screen.blit("sky", (0,0))
    
    for ground_piece in ground:
        ground_piece.draw()       
    player.draw()

    for island in islands:
        island.draw()
    for water_piece in flood:
        water_piece.draw()

    if game_over == True:
        screen.fill((25, 25, 25))
        screen.draw.text("Game Over :(", color="white", pos=(375, 200), fontsize=60)
        screen.draw.text(f"score: {score}", color="white", pos=(475, 250), fontsize=30)


def update():
    global in_jump, player_jump, player_fall_rate, gap, number, game_over, boost

    if keyboard.left:
        player.x -= player_speed
    elif keyboard.right:
        player.x += player_speed

    if not in_jump:
        touching_island = False
        for island in islands:
            touching_island = player.colliderect(island)
            if touching_island:
                player_fall_rate = player_min_fall_rate
                break
        if not touching_island:           
            player.y += player_fall_rate
            for ground_piece in ground:
                ground_piece.y -= player_jump / 10 
            if player_fall_rate < player_max_fall_rate:
                for part in objects:
                    part.y -= player_fall_rate
                player_fall_rate += 0.05
            
        else:
            if keyboard.up:
                in_jump = True
                clock.schedule(reset_jump_flag, 1)
    else:
        player.y -= player_jump
        for part in objects:
            part.y += player_jump        
        for ground_piece in ground:
            ground_piece.y += player_jump / 10
        player_jump -= 0.05
        
    for island in islands:
        if island.y >= 800:
            island.x = random.randint(100, WIDTH - 100)
            island.y = random.randint(number - 30, number + 10)

    for water_piece in flood:
        water_piece.y += 0.15
        touching_water = water_piece.colliderect(player)
        if touching_water:
            game_over = True

    if wait <= 0:
        for water_piece in flood:
            water_piece.y -= boost
        if boost > 0:
            boost -= 0.1
             

def reset_jump_flag():
    global in_jump, player_jump
    
    in_jump = False
    player_jump = base_player_jump


def place_islands(islands):
    global number, gap
    
    for island in islands:
        if island == islands[0]:
            island.pos = WIDTH / 2, HEIGHT - 100
        else:
            island.x = random.randint(100, WIDTH - 100)
            island.y = random.randint(number - 10, number + 10)
            number -= gap


def flood_countdown():
    global wait, score
    wait -= 1
    if game_over == False:    
        score += 1


def flood_pause():
    global wait, boost
    wait = 3
    boost = random.randint(10, 12)


in_jump = False

player = Actor("player")

objects = []

player_speed = 3
player_fall_rate = 0.05
player_jump = 4

base_player_jump = 4
player_max_fall_rate = 5
player_min_fall_rate = 0.1

player_starting_pos = (WIDTH / 2, HEIGHT - 150)
player_y = HEIGHT - 150
player.pos = player_starting_pos
objects.append(player)

islands_loaded = 30
islands = []

number = HEIGHT
gap = 60
wait = 3
boost = 10

game_over = False
score = 0

ground = []
mountains = []

for island in range(islands_loaded):
    random_number = random.randrange(1, 3)
    if random_number == 1:
        platform = Actor("floating_island")
    else:
        platform = Actor("complex_island")
    islands.append(platform)
    objects.append(platform)

for i in range(5):
    ground_piece = Actor("ground")
    ground_piece.pos = i * 280, 650
    ground.append(ground_piece)


flood = []
water_speed = 0.1
max_water_speed = 1.75

for i in range(6):
    water = Actor("water")
    water.pos = i * 200, 700
    flood.append(water)
    objects.append(water)


place_islands(islands)
clock.schedule_interval(flood_countdown, 1)
clock.schedule_interval(flood_pause, 5)


pgzrun.go()