class GameController:
    def __init__(self, model, view):
        store model
        store view
    def start():
        model.start_game()
        while no winner:
            view.display_boards(current_player)
            row, col = view.get_player_input()
            if input valid:
                result = model.confirm_target(current_player, row, col)
                view.display_result(result)
                model.switch_turn()
            else:
                view.display_invalid_input()
        winner = model.check_winner()
        view.display_winner(winner)
