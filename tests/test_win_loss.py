from conftest import make_logic, submit, type_word

WRONG_WORDS = ["BITSY", "FLOWN", "JUMPY", "QUAFF", "VEXED", "FIZZY"]


def _lose(logic):
    for word in WRONG_WORDS:
        result = submit(logic, word)
    return result


def test_win_on_first_round():
    logic = make_logic("CRANE")
    result = submit(logic, "CRANE")
    assert result.won is True
    assert result.game_over is True
    assert result.round_index == 0


def test_win_on_last_round():
    logic = make_logic("CRANE")
    for word in WRONG_WORDS[:5]:
        submit(logic, word)
    result = submit(logic, "CRANE")
    assert result.won is True
    assert result.game_over is True
    assert result.round_index == 5


def test_loss_after_all_rounds_exhausted():
    logic = make_logic("CRANE")
    for word in WRONG_WORDS[:5]:
        submit(logic, word)
    result = submit(logic, WRONG_WORDS[5])
    assert result.won is False
    assert result.game_over is True
    assert result.round_index == 5


def test_game_over_property_true_after_win():
    logic = make_logic("CRANE")
    submit(logic, "CRANE")
    assert logic.game_over is True


def test_game_over_property_true_after_loss():
    logic = make_logic("CRANE")
    _lose(logic)
    assert logic.game_over is True


def test_game_over_property_false_mid_game():
    logic = make_logic("CRANE")
    submit(logic, "BITSY")
    assert logic.game_over is False


def test_add_letter_no_op_after_win():
    logic = make_logic("CRANE")
    submit(logic, "CRANE")
    assert logic.add_letter('A') is False
    assert logic.char == 5  # char stays at num_chars after win (not reset)


def test_delete_letter_no_op_after_win():
    logic = make_logic("CRANE")
    submit(logic, "CRANE")
    assert logic.delete_letter() is False


def test_submit_word_returns_none_after_win():
    logic = make_logic("CRANE")
    submit(logic, "CRANE")
    type_word(logic, "SLATE")
    assert logic.submit_word() is None


def test_round_not_incremented_on_win():
    logic = make_logic("CRANE")
    submit(logic, "BITSY")  # round -> 1
    submit(logic, "CRANE")  # win on round 1
    assert logic.round == 1


def test_round_equals_num_rounds_after_loss():
    logic = make_logic("CRANE")
    _lose(logic)
    assert logic.round == logic.num_rounds


def test_stat_index_for_stats_tracking_win():
    # round_index == the 0-based round that was won, which maps to stats[round_index]
    logic = make_logic("CRANE")
    submit(logic, "BITSY")  # round 0
    result = submit(logic, "CRANE")  # win on round 1
    assert result.round_index == 1
    assert result.won is True


def test_stat_index_for_stats_tracking_loss():
    # On loss, Board should use logic.num_rounds (6) as the stats index
    logic = make_logic("CRANE")
    _lose(logic)
    assert logic.round == logic.num_rounds  # Board uses this for the loss bucket


def test_non_winning_result_has_correct_round_index():
    logic = make_logic("CRANE")
    result = submit(logic, "BITSY")
    assert result.round_index == 0
    assert result.won is False
    assert result.game_over is False
    result2 = submit(logic, "FLOWN")
    assert result2.round_index == 1
