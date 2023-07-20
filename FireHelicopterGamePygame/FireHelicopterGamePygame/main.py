import ast
import json
import pygame
import sys
import os
from utils import randcell
from utils import randnearcell
from utils import check_bounds

# print("Добро пожаловать в игру 'Пожарный вертолет'")
# print("Внимание! Игра откроется в отдельном окне")
# print("Вам потребуется ввести ширину и высоту игрового поля")
# print("Для комфортной игры ширина и высота игрового поля ограничены")
# print("В игре предусмотрено сохрание игрового процесса - клавиша f")
# print("В игре предусмотрено восстановление игрового процесса - клавиша g")
# s_width = int(input("Введите ширину игрового поля (от 3 до 10): "))
# s_height = int(input("Введите высоту игрового поля (от 3 до 8): "))
# if s_width < 3 or s_width > 10 or s_height < 3 or s_height > 8:
#     print("Вы ввели неправильные ширину или длину игрового поля")
# else:
#     s_width = (s_width * 100) + 100
#     s_height = (s_height * 100) + 100

TREE_ADD = 300
FIRE_ADD = 75
FIRE_UPDATE = 100
LIGHTS_UPDATE = 50
CLOUDS_UPDATE = 10
LIFE_UPGRADE = 10

clock = pygame.time.Clock()

pygame.init()

game_font = pygame.font.Font(None, 28)

screen_width = 900
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Fire Helicopter")

gamemap = dict()
tick = 0
lighttick = 0

field_width = screen_width - 100
field_height = screen_height - 100
field_x = int(screen_width / 2 - field_width / 2)
field_y = int(screen_height / 2 - field_height / 2)
# field_color = pygame.Color(255, 255, 255)
# pygame.draw.rect(screen, field_color, (field_x, field_y, field_width, field_height))
start_image = pygame.image.load('img/startgame.png')
screen.blit(start_image, (field_x, field_y))

start_text = pygame.image.load('img/start_text.png')
text_width, text_heigth = start_text.get_size()
text_x = int(screen_width / 2 - text_width / 2)
text_y = int((screen_height / 2 - text_heigth / 2) + 120)
screen.blit(start_text, (text_x, text_y))
pygame.display.update()
pygame.time.wait(5000)

page_1 = pygame.image.load('img/1_page.png')
screen.blit(page_1, (field_x, field_y))
pygame.display.update()
pygame.time.wait(10000)

page_2 = pygame.image.load('img/2_page.png')
screen.blit(page_2, (field_x, field_y))
pygame.display.update()
pygame.time.wait(10000)

page_3 = pygame.image.load('img/3_page.png')
screen.blit(page_3, (field_x, field_y))
pygame.display.update()
pygame.time.wait(20000)

grass_image = pygame.image.load('img/grass20х20.png')
grass_width, grass_heigth = grass_image.get_size()
grass_x, grass_y = field_x, field_y

for i in range(int(field_height / grass_heigth)):
    for j in range(int(field_width / grass_width)):
        grass_x = field_x + (grass_width * j)
        grass_y = field_y + (grass_heigth * i)
        grass_coordinates = (grass_x, grass_y)
        gamemap[grass_coordinates] = 'grass'
        screen.blit(grass_image, (grass_x, grass_y))
pygame.display.update()

tree_image = pygame.image.load('img/conifertree20x20.png')
tree_size = tree_image.get_width()


def generate_gorest():
    rand_cell = randcell(field_x, field_y, field_width, field_height)
    tree_x = rand_cell[0]
    tree_y = rand_cell[1]
    screen.blit(tree_image, (tree_x, tree_y))
    tree_coordinates = (tree_x, tree_y)
    gamemap[tree_coordinates] = 'tree'
    pygame.display.update()
    forest_size = (field_width * field_height // 10000 * 40)
    while forest_size > 0:
        rand_near = randnearcell(tree_x, tree_y)
        rand_near_x = rand_near[0]
        rand_near_y = rand_near[1]
        if check_bounds(rand_near_x, field_x, field_width, rand_near_y, field_y, field_height):
            screen.blit(tree_image, (rand_near_x, rand_near_y))
            tree_x = rand_near_x
            tree_y = rand_near_y
            tree_coordinates = (tree_x, tree_y)
            gamemap[tree_coordinates] = 'tree'
            forest_size -= 1
        else:
            forest_size -= 1


river_image = pygame.image.load('img/river20x20.png')
river_size = river_image.get_width()


def generate_rivers():
    rand_cell = randcell(field_x, field_y, field_width, field_height)
    river_x = rand_cell[0]
    river_y = rand_cell[1]
    screen.blit(river_image, (river_x, river_y))
    river_coordinates = (river_x, river_y)
    gamemap[river_coordinates] = 'river'
    pygame.display.update()
    rivers_size = (field_width * field_height // 10000 * 10)
    while rivers_size > 0:
        rand_near = randnearcell(river_x, river_y)
        rand_near_x = rand_near[0]
        rand_near_y = rand_near[1]
        if check_bounds(rand_near_x, field_x, field_width, rand_near_y, field_y, field_height):
            screen.blit(river_image, (rand_near_x, rand_near_y))
            river_x = rand_near_x
            river_y = rand_near_y
            river_coordinates = (river_x, river_y)
            gamemap[river_coordinates] = 'river'
            rivers_size -= 1
        else:
            rivers_size -= 1


workshop_image = pygame.image.load('img/workshop20x20.png')
workshop_size = workshop_image.get_width()


def generate_workshop():
    rand_cell = randcell(field_x, field_y, field_width,
                         field_height, workshop_size)
    workshop_x = rand_cell[0]
    workshop_y = rand_cell[1]
    gamemap[workshop_x, workshop_y] = 'workshop'
    screen.blit(workshop_image, (workshop_x, workshop_y))
    pygame.display.update()


helipad_image = pygame.image.load('img/helipad20x20.png')
helipad_size = helipad_image.get_width()


def generate_helipad():
    rand_cell = randcell(field_x, field_y, field_width, field_height)
    helipad_x = rand_cell[0]
    helipad_y = rand_cell[1]
    gamemap[helipad_x, helipad_y] = 'helipad'
    screen.blit(helipad_image, (helipad_x, helipad_y))
    pygame.display.update()


helicopter_image = pygame.image.load('img/helicopter20x20.png')
helicopter_size = helicopter_image.get_width()
rand_cell = randcell(field_x, field_y, field_width,
                     field_height, workshop_size)
helicopter_x, helicopter_y = rand_cell
HELICOPTER_STEP = 20
helicopter_left, helicopter_right, helicopter_up, helicopter_down = False, False, False, False

life_image = pygame.image.load('img/life20x20.png')
life_size = life_image.get_width()
life = 20

tank_image = pygame.image.load('img/tank20x20.png')
tank_size = tank_image.get_width()
tank = 1
maxtank = 1

score_image = pygame.image.load('img/score20x20.png')
score_size = score_image.get_width()
score = 5

fire_image = pygame.image.load('img/fire20x20.png')
fire_size = fire_image.get_width()


def generate_tree():
    tree_x, tree_y = randcell(field_x, field_y, field_width, field_height)
    if (tree_x, tree_y) in gamemap:
        if gamemap[(tree_x, tree_y)] == 'grass':
            gamemap[(tree_x, tree_y)] = 'tree'
            screen.blit(tree_image, (tree_x, tree_y))
            pygame.display.update()


def generate_fire():
    fire_x, fire_y = randcell(field_x, field_y, field_width, field_height)
    if (fire_x, fire_y) in gamemap:
        if gamemap[(fire_x, fire_y)] == 'tree':
            gamemap[(fire_x, fire_y)] = 'fire'
            screen.blit(fire_image, (fire_x, fire_y))
            pygame.display.update()


def update_fire(score):
    fire_x = rand_cell[0]
    fire_y = rand_cell[1]
    for key, value in gamemap.items():
        if value == 'fire':
            fire_x, fire_y = key
            gamemap[key] = 'grass'
            score -= 1
            screen.blit(grass_image, (fire_x, fire_y))
    for fires in range(3):
        rand_near_x, rand_near_y = randnearcell(fire_x, fire_y)
        if (rand_near_x, rand_near_y) in gamemap:
            if gamemap[rand_near_x, rand_near_y] == 'tree':
                gamemap[rand_near_x, rand_near_y] = 'fire'
                screen.blit(fire_image, (rand_near_x, rand_near_y))
                pygame.display.update()
    generate_fire()
    generate_fire()
    return (score)


def reverse_cloudobjects(helicopter_x, helicopter_y, life):
    value_clouds = cloudmap[helicopter_x, helicopter_y]
    if value_clouds == 'cloud':
        screen.blit(cloud_image, (helicopter_x, helicopter_y))
    elif value_clouds == 'light':
        screen.blit(light_image, (helicopter_x, helicopter_y))
        life -= 1
    return life


def reverse_mapobjects(helicopter_x, helicopter_y):
    value_map = gamemap[helicopter_x, helicopter_y]
    if value_map == 'grass':
        screen.blit(grass_image, (helicopter_x, helicopter_y))
    elif value_map == 'tree':
        screen.blit(tree_image, (helicopter_x, helicopter_y))
    elif value_map == 'river':
        screen.blit(river_image, (helicopter_x, helicopter_y))
    elif value_map == 'fire':
        screen.blit(fire_image, (helicopter_x, helicopter_y))
    elif value_map == 'workshop':
        screen.blit(workshop_image, (helicopter_x, helicopter_y))
    elif value_map == 'helipad':
        screen.blit(helipad_image, (helicopter_x, helicopter_y))


def upgrade_helicopter(helicopter_x, helicopter_y, score, maxtank, life):
    tank_upgrade = maxtank * 10
    value_map = gamemap[helicopter_x, helicopter_y]
    if value_map == 'helipad' and score >= LIFE_UPGRADE:
        life += 1
        score -= LIFE_UPGRADE
    elif value_map == 'workshop' and score >= tank_upgrade:
        maxtank += 1
        score -= tank_upgrade
    upgrade = [score, maxtank, life]
    return upgrade


cloud_image = pygame.image.load('img/clouds.png')
cloud_size = cloud_image.get_width()
light_image = pygame.image.load('img/lights.png')
light_size = light_image.get_width()

cloudmap = gamemap.copy()


def cloud_add():
    cloud_x, cloud_y = randcell(field_x, field_y, field_width, field_height)
    screen.blit(cloud_image, (cloud_x, cloud_y))
    if (cloud_x, cloud_y) in cloudmap:
        cloudmap[cloud_x, cloud_y] = 'cloud'
        pygame.display.update()
        clouds_size = int(field_width * field_height // 10000 * 10)
        while clouds_size > 0:
            rand_near_x, rand_near_y = randnearcell(cloud_x, cloud_y)
            if check_bounds(rand_near_x, field_x, field_width, rand_near_y, field_y, field_height):
                screen.blit(cloud_image, (rand_near_x, rand_near_y))
                cloud_coordinates = (rand_near_x, rand_near_y)
                cloudmap[cloud_coordinates] = 'cloud'
                clouds_size -= 1
            else:
                clouds_size -= 1


def lights_update():
    for j in range(20):
        cloud_x, cloud_y = randcell(
            field_x, field_y, field_width, field_height, workshop_size)
        if (cloud_x, cloud_y) in gamemap:
            if cloudmap[cloud_x, cloud_y] == 'cloud':
                cloudmap[cloud_x, cloud_y] = 'light'
                for i in range(3):
                    rand_near_x, rand_near_y = randnearcell(cloud_x, cloud_y)
                    if check_bounds(rand_near_x, field_x, field_width, rand_near_y, field_y, field_height):
                        if cloudmap[rand_near_x, rand_near_y] == 'cloud':
                            cloudmap[rand_near_x, rand_near_y] = 'light'
                            screen.blit(
                                light_image, (rand_near_x, rand_near_y))
                            pygame.display.update()
    for count in range(5):
        cloud_add()


def clouds_update():
    for key, value in cloudmap.items():
        if value == 'cloud' or value == 'light':
            cloud_x, cloud_y = key
            cloudmap[cloud_x, cloud_y] = 'none'
            if gamemap[cloud_x, cloud_y] == 'grass':
                screen.blit(grass_image, (cloud_x, cloud_y))
            elif gamemap[cloud_x, cloud_y] == 'tree':
                screen.blit(tree_image, (cloud_x, cloud_y))
            elif gamemap[cloud_x, cloud_y] == 'river':
                screen.blit(river_image, (cloud_x, cloud_y))
            elif gamemap[cloud_x, cloud_y] == 'fire':
                screen.blit(fire_image, (cloud_x, cloud_y))
            elif gamemap[cloud_x, cloud_y] == 'workshop':
                screen.blit(workshop_image, (cloud_x, cloud_y))
            elif gamemap[cloud_x, cloud_y] == 'helipad':
                screen.blit(helipad_image, (cloud_x, cloud_y))
            elif gamemap[cloud_x, cloud_y] == 'fire':
                screen.blit(fire_image, (cloud_x, cloud_y))


def key_to_json(data):
    if data is None or isinstance(data, (bool, int, str)):
        return data
    if isinstance(data, (tuple, frozenset)):
        return str(data)
    raise TypeError


generate_gorest()
generate_rivers()
generate_workshop()
generate_helipad()

gamerunning = True

while gamerunning:
    tick += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # path = 'save.json'
            # if os.path.isfile(path):
            #     os.remove(path)
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                helicopter_up = True
            if event.key == pygame.K_DOWN:
                helicopter_down = True
            if event.key == pygame.K_LEFT:
                helicopter_left = True
            if event.key == pygame.K_RIGHT:
                helicopter_right = True
            if event.key == pygame.K_f:
                data_gamemap = str(gamemap)
                data_cloudmap = str(cloudmap)
                helicopter_dic = {"helicopter_x": helicopter_x,
                                  "helicopter_y": helicopter_y}
                data_helicopter = str(helicopter_dic)
                tick_dic = {"tick": tick, "lighttick": lighttick}
                data_tick = str(tick_dic)
                atributes_dic = {"life": life, "tank": tank,
                                 "maxtank": maxtank, "score": score}
                data_atributes = str(atributes_dic)
                all_data = [data_gamemap, data_cloudmap,
                            data_helicopter, data_tick, data_atributes]
                with open("save.json", "w") as file:
                    json.dump(all_data, file)
            if event.key == pygame.K_g:
                with open("save.json", "r") as file:
                    all_data = json.load(file)
                    str_map = (all_data[0])
                    restore_gamemap = ast.literal_eval(str_map)
                    for key, value in restore_gamemap.items():
                        if key in gamemap:
                            if value == 'grass':
                                gamemap[key] = 'grass'
                                screen.blit(grass_image, key)
                            elif value == 'tree':
                                gamemap[key] = 'tree'
                                screen.blit(tree_image, key)
                            elif value == 'river':
                                gamemap[key] = 'river'
                                screen.blit(river_image, key)
                            elif value == 'fire':
                                gamemap[key] = 'fire'
                                screen.blit(fire_image, key)
                            elif value == 'workshop':
                                gamemap[key] = 'workshop'
                                screen.blit(workshop_image, key)
                            elif value == 'helipad':
                                gamemap[key] = 'helipad'
                                screen.blit(helipad_image, key)
                    str_cloud = (all_data[1])
                    restore_cloudmap = ast.literal_eval(str_cloud)
                    for key in cloudmap:
                        cloudmap[key] = 'None'
                    for key, value in restore_cloudmap.items():
                        if key in cloudmap:
                            if value == 'cloud':
                                cloudmap[key] = 'cloud'
                                screen.blit(cloud_image, key)
                            elif value == 'light':
                                cloudmap[key] = 'light'
                                screen.blit(cloud_image, key)
                    str_helicopter = (all_data[2])
                    restore_helicopter = ast.literal_eval(str_helicopter)
                    helicopter_x = restore_helicopter['helicopter_x']
                    helicopter_y = restore_helicopter['helicopter_y']
                    str_tick = (all_data[3])
                    restore_tick = ast.literal_eval(str_tick)
                    tick = restore_tick['tick']
                    lighttick = restore_tick['lighttick']
                    str_atributes = (all_data[4])
                    restore_atributes = ast.literal_eval(str_atributes)
                    life = restore_atributes['life']
                    tank = restore_atributes['tank']
                    maxtank = restore_atributes['maxtank']
                    score = restore_atributes['score']
            if event.key == pygame.K_ESCAPE:
                sys.exit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                helicopter_up = False
            if event.key == pygame.K_DOWN:
                helicopter_down = False
            if event.key == pygame.K_LEFT:
                helicopter_left = False
            if event.key == pygame.K_RIGHT:
                helicopter_right = False

    if helicopter_left and helicopter_x > field_x:
        reverse_mapobjects(helicopter_x, helicopter_y)
        life = reverse_cloudobjects(helicopter_x, helicopter_y, life)
        upgrade = upgrade_helicopter(
            helicopter_x, helicopter_y, score, maxtank, life)
        score, maxtank, life = upgrade
        helicopter_x -= HELICOPTER_STEP
    if helicopter_right and helicopter_x < field_x + field_width - helicopter_size:
        reverse_mapobjects(helicopter_x, helicopter_y)
        life = reverse_cloudobjects(helicopter_x, helicopter_y, life)
        upgrade = upgrade_helicopter(
            helicopter_x, helicopter_y, score, maxtank, life)
        score, maxtank, life = upgrade
        helicopter_x += HELICOPTER_STEP
    if helicopter_up and helicopter_y > field_y:
        reverse_mapobjects(helicopter_x, helicopter_y)
        life = reverse_cloudobjects(helicopter_x, helicopter_y, life)
        upgrade = upgrade_helicopter(
            helicopter_x, helicopter_y, score, maxtank, life)
        score, maxtank, life = upgrade
        helicopter_y -= HELICOPTER_STEP
    if helicopter_down and helicopter_y < field_y + field_height - helicopter_size:
        reverse_mapobjects(helicopter_x, helicopter_y)
        life = reverse_cloudobjects(helicopter_x, helicopter_y, life)
        upgrade = upgrade_helicopter(
            helicopter_x, helicopter_y, score, maxtank, life)
        score, maxtank, life = upgrade
        helicopter_y += HELICOPTER_STEP

    screen.blit(helicopter_image, (helicopter_x, helicopter_y))

    if (tick % TREE_ADD == 0):
        generate_tree()
    if (tick == FIRE_ADD) or (tick % FIRE_UPDATE == 0):
        score = update_fire(score)
    if (tick % LIGHTS_UPDATE == 0):
        lights_update()
        lighttick += 1
        if (lighttick % CLOUDS_UPDATE == 0):
            clouds_update()
            lights_update()

    if gamemap[helicopter_x, helicopter_y] == 'river':
        tank = maxtank

    if gamemap[helicopter_x, helicopter_y] == 'fire' and tank > 0:
        gamemap[helicopter_x, helicopter_y] = 'tree'
        screen.blit(tree_image, (helicopter_x, helicopter_y))
        tank -= 1
        score += 1

    text_area_width = screen_width - 100
    text_area_height = 50
    text_area_x = 50
    text_area_y = 0
    area_color = pygame.Color(0, 0, 0)
    pygame.draw.rect(screen, area_color, (text_area_x,
                     text_area_y, text_area_width, text_area_height))

    screen.blit(life_image, (50, 20))
    life_text = game_font.render(f'{life}', True, 'red')
    screen.blit(life_text, (80, 20))

    screen.blit(tank_image, (150, 20))
    tank_text = game_font.render(f'{maxtank}/{tank}', True, 'blue')
    screen.blit(tank_text, (180, 20))

    screen.blit(score_image, (250, 20))
    score_text = game_font.render(f'{score}', True, 'yellow')
    screen.blit(score_text, (280, 20))

    pygame.display.update()
    clock.tick(15)
    if (score < 0) or (life <= 0):
        gamerunning = False
        # path = 'save.json'
        # if os.path.isfile(path):
        #     os.remove(path)
        # else:
        #     print('Path is not a file')

game_over_image = pygame.image.load('img/game_over.png')
screen.blit(game_over_image, (field_x, field_y))
game_over_text = game_font.render(
    f"Game Over!!! Your score is {score}", True, "red")
game_over_rectangle = game_over_text.get_rect()
game_over_rectangle.center = (screen_width / 2, screen_height / 2)
screen.blit(game_over_text, game_over_rectangle)
pygame.display.update()
pygame.time.wait(10000)
pygame.quit()
