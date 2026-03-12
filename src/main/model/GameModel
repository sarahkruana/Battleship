class GameModel:
    def __init__(self):
        create_board_for_player1()
        create_board_for_player2()
        initialize_ships()
        initialize_scores()

    def start_game(self):
        place_ships_for_each_player()

    def place_ship(player, coordinates):
        if placement_is_valid(coordinates):
            add_ship_to_board(player)

    def confirm_target(player, target_coord):
        if target_is_valid(target_coord):
            result = check_hit_or_miss(player, target_coord)
            update_board(result)
            update_score(result)

    def check_winner():
        if all_ships_sunk(player1):
            return player2
        if all_ships_sunk(player2):
            return player1
