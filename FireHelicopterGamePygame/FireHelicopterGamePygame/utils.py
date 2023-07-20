from random import randint


def check_bounds(x, field_x, field_width, y, field_y, field_height, size = 20):
    field_x_end = field_x + field_width
    field_y_end = field_y + field_height
    if (x < field_x) or (y < field_y) or (x + size >= field_x_end) or (y + size >= field_y_end):
        return False
    return True


def randcell(field_x, field_y, field_width, field_height, size = 20):
    field_step_x = field_width / size # 40 = 800/20
    field_step_y = field_height / size # 30 = 600/20
    rand_x = (field_x + (randint(0, field_step_x) * size)) - size #50 + (40*20) - 20 = 780
    rand_y = (field_y + (randint(0, field_step_y) * size)) - size
    if rand_x < field_x:
        rand_x += size
    elif rand_x > field_x + field_width - size:
        rand_x -= size
    elif rand_y < field_y:
        rand_y += size
    elif rand_y > field_y + field_height - size:
        rand_y -= size
    return rand_x, rand_y


def randnearcell(x, y):
    moves = [(-20, 0), (0, 20), (20, 0), (0, -20)]
    temp = (randint(0, 3))
    near_x, near_y = moves[temp][0], moves[temp][1]
    return x + near_x, y + near_y
