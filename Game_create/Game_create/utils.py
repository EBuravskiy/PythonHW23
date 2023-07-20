from random import randint as rand


def introduce():
    print("ИГРА. ПОЖАРНЫЙ ВЕРТОЛЕТ")
    print("Описание игры:")
    print("На прямоугольном поле расположены деревья, водоемы, больница и мастерская")
    print("Деревья периодически вырастают и могут загораться")
    print("Для тушения пожара в игре используется вертолет, который для тушения пожара в установленный на борту \nбак набирает воду из реки")
    print("Задачей игры является вовремя тушить деревья с помощью вертолета")
    print("За потушенное дерево Вам начислятся очки, но если дерево сгорело, то Вы потеряете очки")
    print("Также в процессе игры появляются облака и торнадо, которые загораживают видимую область")
    print("Если вертолет попадает в область действия торнадо, то у него теряются очки прочности")
    print("Если в ходе игры Ваши очки стали меньше 0, либо Вы израсходовали все очки прочности вертолета, то игра заканчивается")
    print("В мастерской можно установить дополнительный бак для воды. Стоимость установки составляет 5000 очков")
    print("В больнице можно отремонтировать вертолет, либо увеличить количество прочности вертолета. Стоимость ремонта составляет 5000 очков")
    print("Управление вертолетом осуществляется при помощи клавиш w - вверх, s- вниз, a - влево, d - вправо")
    print("Также в процессе игры, можно осуществить сохранение текущих достижений при помощи клавиши f")
    print("Возобновление сохраненной игры осуществляется нажатием на клавишу g")

    # continue_game = input(
    #     "Для продолжения нажмите Enter, для выхода введите stop: ")
    # if continue_game == "stop":
    #     quit()
    # operation_system = input(
    #     "Введите используемую операционную систему (win - Windows или ios - unux подобных систем): ")
    # if operation_system == "win":
    #     o_system = "cls"
    # elif operation_system == "ios":
    #     o_system = "clear"
    # else:
    #     print("Вы произвели неверный выбор. Попробуйте еще раз")
    #     quit()
    # return str(o_system)


def mapsize():
    map_width = input("Введите ширину игрового поля: ")
    map_height = input("Введите высоту игрового поля: ")
    if map_width == "" or map_height == "":
        print("Вы не ввели размеры поля")
        quit()
    else:
        map_width = int(map_width)
        print(map_width)
        map_height = int(map_height)
        print(map_height)
        if map_width == 0 or map_height == 0:
            print("Поле не может быть с нулевой шириной, либо нулевой длинной")
            quit()
        map_size = [map_width, map_height]
    return map_size


def randbool(r, max_rand):
    rand_number = rand(0, max_rand)
    return (rand_number <= r)


def randcell(wight, height):
    rc_wight = rand(0, wight - 1)
    rc_height = rand(0, height - 1)
    return (rc_height, rc_wight)


def randnearcell(x_cell, y_cell):
    moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    temp = rand(0, 3)
    rncell_x, rncell_y = moves[temp][0], moves[temp][1]
    return (x_cell + rncell_x, y_cell + rncell_y)
