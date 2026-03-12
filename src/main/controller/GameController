class GameController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def run_game():
        model.start_game()

        while not model.check_winner():
            current_player = get_current_player()
            target = view.get_player_input()
            if input_is_valid(target):
                model.confirm_target(current_player, target)

            view.refresh_display(model)
            switch_players()

        winner = model.check_winner()
        view.show_winner(winner)
