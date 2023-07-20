from utils import randcell

def generate_tree(field_x, field_y, field_width, field_height, tree_size):
    rand_cell = randcell(field_x, field_y, field_width, field_height, tree_size)
    tree_x = rand_cell[0]
    tree_y = rand_cell[1]
    return tree_x, tree_y