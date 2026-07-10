from conftest import make_logic, submit, type_word
from wordle.game_logic import TileResult


def test_reset_clears_tiles():
    logic = make_logic("CRANE")
    type_word(logic, "BITSY")
    logic.reset("SLATE")
    assert all(cell is None for row in logic.tiles for cell in row)


def test_reset_clears_color_tiles():
    logic = make_logic("CRANE")
    submit(logic, "BITSY")
    logic.reset("SLATE")
    assert all(cell == TileResult.EMPTY for row in logic.color_tiles for cell in row)


def test_reset_sets_new_word():
    logic = make_logic("CRANE")
    logic.reset("SLATE")
    assert logic.word_str == "SLATE"


def test_reset_uppercases_new_word():
    logic = make_logic("CRANE")
    logic.reset("slate")
    assert logic.word_str == "SLATE"


def test_reset_resets_round_to_zero():
    logic = make_logic("CRANE")
    submit(logic, "BITSY")
    assert logic.round == 1
    logic.reset("SLATE")
    assert logic.round == 0


def test_reset_resets_char_to_zero():
    logic = make_logic("CRANE")
    type_word(logic, "BIT")
    logic.reset("SLATE")
    assert logic.char == 0


def test_reset_clears_game_over_flag_after_win():
    logic = make_logic("CRANE")
    submit(logic, "CRANE")
    assert logic.game_over is True
    logic.reset("SLATE")
    assert logic.game_over is False


def test_reset_clears_game_over_flag_after_loss():
    logic = make_logic("CRANE")
    for word in ["BITSY", "FLOWN", "JUMPY", "QUAFF", "VEXED", "FIZZY"]:
        submit(logic, word)
    assert logic.game_over is True
    logic.reset("SLATE")
    assert logic.game_over is False


def test_reset_clears_invalid_word_flag():
    logic = make_logic(word_checker=lambda w: False)
    type_word(logic, "CRANE")
    logic.can_submit_word()
    assert logic.invalid_word is True
    logic.reset("SLATE")
    assert logic.invalid_word is False


def test_can_play_full_game_after_reset():
    logic = make_logic("CRANE")
    submit(logic, "CRANE")
    logic.reset("SLATE")
    result = submit(logic, "SLATE")
    assert result is not None
    assert result.won is True


def test_tiles_dimensions_preserved_after_reset():
    logic = make_logic("CRANE", num_rounds=6, num_chars=5)
    submit(logic, "BITSY")
    logic.reset("SLATE")
    assert len(logic.tiles) == 6
    assert all(len(row) == 5 for row in logic.tiles)
