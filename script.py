from random import randint

board = []
health = 100

constant_features = {'border' : '#', 'space' : ' '}
random_features = {'enemy' : 'ß', 'barrier' : '.', 'player' : '$'}


def enumerateRandomly( random_features ):
#No need to enumerate player since it is only one

    enemy_list = []
    barrier_list = []

    enemy_number = randint(6, 12)
    barrier_number = randint(8, 15)

    enemy_list = [random_features['enemy']] * enemy_number

    barrier_list = [random_features['barrier']] * barrier_number

    player = random_features['player']

    randomFeature_list = [enemy_list, barrier_list, player]

    return randomFeature_list

def assign_coordinates ( randomFeature_list ):

    enemy_coordinates = randomFeature_list[0]
    barrier_coordinates = randomFeature_list[1]

    enemy_i = 0
    barrier_i = 0

#Assign coordinates to player
    randomFeature_list[2] = [randint(1, 33), randint(1, 33)]
    player_coordinate = randomFeature_list[2]

#Assign [number : coordinates] to enemies and barriers and add them to the dictionary
    for enemy in range(len( enemy_coordinates )):
        enemy_coordinates[enemy_i] = [randint(1, 33), randint(1, 33)]
        enemy_i += 1

    for barrier in range(len( barrier_coordinates )):
        barrier_coordinates[barrier_i] = [randint(1, 33), randint(1, 33)]
        barrier_i += 1

#Compare the elements and change the coordinates in case of a duplicate
    if len(enemy_coordinates) >= len(barrier_coordinates):
        for enemy in enemy_coordinates:
           for barrier in barrier_coordinates:
            if enemy == barrier:
                enemy = [randint(1, 33), randint(1, 33)]
    else:
        for barrier in barrier_coordinates:
            for enemy in enemy_coordinates:
                if enemy == barrier:
                    enemy = [randint(1, 33), randint(1, 33)]

    while (player_coordinate in enemy_coordinates) \
        or (player_coordinate in barrier_coordinates):
        randomFeature_list[2] = [randint(1, 33), randint(1, 33)]

    return randomFeature_list


def create_map ( constant_features ):
    count = 0
    game_map = []
    border = '#'
    space = ' '

    first_border = border * 34
    game_map.append(first_border)

    while count < 32:
        game_map.append( border + (space * 33) + border)
        count += 1

    last_border = border * 34
    game_map.append(last_border)

    return game_map


def place_random_features( randomFeature_list, game_map):

    enemy_coordinates = randomFeature_list[0]
    barrier_coordinates = randomFeature_list[1]
    player_coordinate = randomFeature_list[2]

    for enemy in enemy_coordinates:
        line = game_map[enemy[0]]
        char_index = enemy[1]
        line = line[:char_index] + 'ß' + line[char_index + 1:]
        game_map[enemy[0]] = line

    for barrier in barrier_coordinates:
        line = game_map[barrier[0]]
        char_index = barrier[1]
        line = line[:char_index] + '.' + line[char_index + 1:]
        game_map[barrier[0]] = line

    line = game_map[player_coordinate[0]]
    char_index = player_coordinate[1]
    line = line[:char_index] + '$' + line[char_index + 1:]
    game_map[player_coordinate[0]] = line

    return game_map


def ask_direction():
    introduction = '''\
    Hello Player! The game is ready..
    We want you to enter a direction to move in map..
    There are only four options:
            
               W: UP
            
        A: LEFT     D: RIGHT
        
               S: DOWN
                    
    Now, please kindly enter a directon accordingly to the instructions.
    >Direction I wanna go: ''' 

    direction = input(introduction).upper()

    return direction


def make_movement(direction, game_map, randomFeature_list):

    enemy_coordinates = randomFeature_list[0]
    barrier_coordinates = randomFeature_list[1]
    player_coordinate = randomFeature_list[2]

    moves = {
        'W' : [player_coordinate[0] - 1, player_coordinate[1]],
        'S' : [player_coordinate[0] + 1, player_coordinate[1]],
        'D' : [player_coordinate[0],     player_coordinate[1] + 1],
        'A' : [player_coordinate[0],     player_coordinate[1] - 1]
    }

#FIND THE INDEX OF PLAYER, CHANGE IT TO SPACE
    line = game_map[player_coordinate[0]]
    char_index = player_coordinate[1]
    line = line[:char_index] + ' ' + line[char_index + 1:]
    game_map[player_coordinate[0]] = line

#CHOOSE WHICH DIRECTION WHICH COORDINATE
    if moves[direction] not in barrier_coordinates:
        player_coordinate = moves[direction]

#MOVE TO NEW COORDINATE
    line = game_map[player_coordinate[0]]
    char_index = player_coordinate[1]
    line = line[:char_index] + '$' + line[char_index + 1:]
    game_map[player_coordinate[0]] = line
    
    randomFeature_list[2] = player_coordinate

    return (game_map, randomFeature_list)


def fight(game_map, randomFeature_list, health):
    player_coordinate = randomFeature_list[2]
    enemy_coordinates = randomFeature_list[0]

    moves = {
        'W' : [player_coordinate[0] - 1, player_coordinate[1]],
        'S' : [player_coordinate[0] + 1, player_coordinate[1]],
        'D' : [player_coordinate[0],     player_coordinate[1] + 1],
        'A' : [player_coordinate[0],     player_coordinate[1] - 1]
    }

#CHECK ONE SPACE DISTANCE AND DETECT IF THERE IS AN ENEMEY
    for possible_enemy in moves:
        if moves[possible_enemy] in enemy_coordinates:
            
#IF THERE IS, START THE FIGHT!
            magic_number = randint(0, 6)
            warning = 'Oi! It is time to fight! Spell the magic words: '
            magic_word = input(warning)

            vowel_set = set("aeiou")
            count_vowels = 0
            for letter in magic_word.lower():
                if (letter in vowel_set):
                    count_vowels += 1
                    
            
            while (count_vowels != magic_number) and (health > 0):
                damage = (magic_number - count_vowels) * 6
                health -= damage
                damaged = \
                'Health: ' + str(health) +\
                '\nYou missed! You got ' + str(damage) + ' damage.'+\
                '\nTry again: '
                different_number = input(damaged)

                vowel_set = set("aeiou")
                count_vowels = 0
                for letter in different_number.lower():
                    if (letter in vowel_set):
                        count_vowels += 1

            else:
#REMOVE THE ENEMY IF COUNT_VOWELS == MAGIC_NUMBER
                killed_enemy = moves[possible_enemy]
                line = game_map[killed_enemy[0]]
                char_index = killed_enemy[1]
                line = line[:char_index] + ' ' + line[char_index + 1:]
                game_map[killed_enemy[0]] = line

                return [game_map, randomFeature_list, health]


def print_game( health, game_map):
    print(str(health))
    print(*game_map, sep = "\n")


def play_game(random_features, health):

    a = enumerateRandomly( random_features )
    b = assign_coordinates ( a )
    c = create_map ( b )
    d = place_random_features(b, c)
    print(*d, sep = "\n")

    while health > 0:
        
        f = ask_direction()
        g = make_movement(f, d, b)
        h = fight(g[0], g[1], health)
        print(*d, sep = "\n") 
        #b = h[1]
    else:
            print('{ { { Y O U      L O S T } } }')



play_game( random_features, health )
