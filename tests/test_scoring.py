from conftest import G, R, Y, make_logic, submit
from game_logic import TileResult


def test_all_green_when_guess_equals_answer():
    logic = make_logic("CRANE")
    result = submit(logic, "CRANE")
    assert result.scores == [G, G, G, G, G]


def test_all_red_when_no_shared_letters():
    # BITSY shares no letters with CRANE
    logic = make_logic("CRANE")
    result = submit(logic, "BITSY")
    assert result.scores == [R, R, R, R, R]


def test_mixed_green_red():
    # CRIME vs CRANE: C=G, R=G, I=R, M=R, E=G
    logic = make_logic("CRANE")
    result = submit(logic, "CRIME")
    assert result.scores == [G, G, R, R, G]


def test_yellow_letter_in_word_wrong_position():
    # ACORN vs CRANE: A=Y, C=Y, O=R, R=Y, N=Y
    logic = make_logic("CRANE")
    result = submit(logic, "ACORN")
    assert result.scores == [Y, Y, R, Y, Y]


def test_color_tiles_updated_after_submit():
    logic = make_logic("CRANE")
    submit(logic, "CRIME")
    assert logic.color_tiles[0] == [G, G, TileResult.RED, TileResult.RED, G]


def test_tiles_row_preserved_after_submit():
    logic = make_logic("CRANE")
    submit(logic, "CRIME")
    assert logic.tiles[0] == ['C', 'R', 'I', 'M', 'E']


def test_round_advances_after_non_winning_submit():
    logic = make_logic("CRANE")
    submit(logic, "BITSY")
    assert logic.round == 1


def test_char_resets_to_zero_after_submit():
    logic = make_logic("CRANE")
    submit(logic, "BITSY")
    assert logic.char == 0


def test_round_does_not_advance_after_winning_submit():
    logic = make_logic("CRANE")
    submit(logic, "CRANE")
    assert logic.round == 0


def test_second_round_scores_independently():
    logic = make_logic("CRANE")
    submit(logic, "BITSY")
    result = submit(logic, "CRIME")
    assert result.scores == [G, G, R, R, G]
    assert logic.color_tiles[1] == [G, G, TileResult.RED, TileResult.RED, G]


def test_earlier_rounds_color_tiles_unchanged_by_later_round():
    logic = make_logic("CRANE")
    submit(logic, "BITSY")
    submit(logic, "CRANE")
    assert logic.color_tiles[0] == [R, R, R, R, R]
    assert logic.color_tiles[1] == [G, G, G, G, G]
