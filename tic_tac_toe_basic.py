# logic for the game when the user takes first move
# user = X , computer = O ,else = -1

state = [
    [-1, -1, -1],
    [-1, -1, -1],
    [-1, -1, -1]
]

game_over = False

winning_trios = (
    ((0, 0), (0, 1), (0, 2)),
    ((1, 0), (1, 1), (1, 2)),
    ((2, 0), (2, 1), (2, 2)),

    ((0, 0), (1, 0), (2, 0)),
    ((0, 1), (1, 1), (2, 1)),
    ((0, 2), (1, 2), (2, 2)),

    ((0, 0), (1, 1), (2, 2)),
    ((0, 2), (1, 1), (2, 0)),
)


# #game starts here
# x,y = map(int,input().split())
# state[y][x] = "X"

def get_the_third_unaccessed_block(player, trio):  # returns (x,y)-->tuple of the third block
    # Player 'player'  has caught the two two boxes of the trio 
    global state
    for box in trio:
        x = box[0]
        y = box[1]

        if state[y][x] != player:
            return box


def block_any_unblocked(player, trio):
    global state
    for box in trio:
        x = box[0]
        y = box[1]

        if state[y][x] == -1:
            state[y][x] = player
            break
    return


def only_one_block_of_player_in_the_trio(player, trio):
    global state
    player_count = 0
    empty_count = 0
    for box in trio:
        x = box[0]
        y = box[1]

        if state[y][x] == player:
            player_count += 1
        elif state[y][x] == -1:
            empty_count += 1

    return player_count == 1 and empty_count == 2


def is_empty(trio):
    global state
    empty_count = 0
    for box in trio:
        x = box[0]
        y = box[1]

        if state[y][x] == -1:
            empty_count += 1

    return empty_count == 3


def two_blocks_caught_by(player, trio):
    global state
    count = 0
    for box in trio:
        x = box[0]
        y = box[1]

        if state[y][x] == player:
            count += 1
    return count == 2


def defend():
    global state
    for trio in winning_trios:
        if two_blocks_caught_by("X", trio):
            x, y = get_the_third_unaccessed_block("X", trio)
            state[y][x] = "O"
            return True
    return


def attack():
    global state
    for trio in winning_trios:
        if two_blocks_caught_by("O", trio):
            x, y = get_the_third_unaccessed_block("O", trio)
            state[y][x] = "O"
            global game_over
            game_over = True
            return True
    return


def neutral_move():
    global state
    one_block_trio_found = False
    for trio in winning_trios:
        if only_one_block_of_player_in_the_trio("O", trio):
            one_block_trio_found = True
            block_any_unblocked("O", trio)
            break
    if not one_block_trio_found:
        for trio in winning_trios:
            if is_empty(trio):
                block_any_unblocked("O", trio)
                break
    return


def playNormal():
    if not defend():
        if not attack():
            neutral_move()

    return

    # that is search for box that lies in a winning trio and is not
    # having a single element of the opponent


def check_for_winner():
    global state
    for trio in winning_trios:
        x_count = 0
        o_count = 0
        for box in trio:
            x = box[0]
            y = box[1]

            if state[y][x] == "X":
                x_count += 1
            elif state[y][x] == "O":
                o_count += 1

        if x_count == 3 or o_count == 3:
            global game_over
            game_over = True
            return max(x_count, o_count)

    return


while not game_over:
    x, y = map(int, input().split())
    state[y][x] = "X"
    playNormal()
    print(state)
    check_for_winner()
