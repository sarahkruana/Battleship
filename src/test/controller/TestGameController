class TestGameController:
    def test_input_validation():
        controller = GameController(model, view)
        result = controller.input_is_valid(valid_target)
        assert result == True

    def test_turn_switching():
        controller = GameController(model, view)
        current = controller.get_current_player()
        controller.switch_players()
        new_player = controller.get_current_player()
        assert new_player != current
