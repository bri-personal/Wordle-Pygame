from conftest import make_logic, submit, type_word


def test_add_letter_stores_in_tiles():
    logic = make_logic()
    logic.add_letter('c')
    assert logic.tiles[0][0] == 'C'


def test_add_letter_uppercases_input():
    logic = make_logic()
    logic.add_letter('a')
    assert logic.tiles[0][0] == 'A'


def test_add_letter_increments_char():
    logic = make_logic()
    logic.add_letter('C')
    assert logic.char == 1


def test_add_letter_fills_row():
    logic = make_logic("CRANE")
    for ch in "CRANE":
        logic.add_letter(ch)
    assert logic.tiles[0] == ['C', 'R', 'A', 'N', 'E']
    assert logic.char == 5


def test_add_letter_returns_true_when_space_available():
    logic = make_logic()
    assert logic.add_letter('A') is True


def test_add_letter_at_capacity_returns_false():
    logic = make_logic()
    type_word(logic, "CRANE")
    result = logic.add_letter('X')
    assert result is False


def test_add_letter_at_capacity_does_not_change_tiles():
    logic = make_logic()
    type_word(logic, "CRANE")
    logic.add_letter('X')
    assert logic.tiles[0] == ['C', 'R', 'A', 'N', 'E']


def test_add_letter_returns_false_after_game_over():
    logic = make_logic("CRANE")
    submit(logic, "CRANE")
    assert logic.add_letter('A') is False


def test_delete_letter_removes_last():
    logic = make_logic()
    type_word(logic, "CR")
    logic.delete_letter()
    assert logic.tiles[0][1] is None
    assert logic.char == 1


def test_delete_letter_returns_true_when_char_gt_zero():
    logic = make_logic()
    logic.add_letter('A')
    assert logic.delete_letter() is True


def test_delete_letter_on_empty_row_returns_false():
    logic = make_logic()
    assert logic.delete_letter() is False


def test_delete_letter_on_empty_row_does_nothing():
    logic = make_logic()
    logic.delete_letter()
    assert logic.char == 0
    assert logic.tiles[0][0] is None


def test_delete_letter_clears_invalid_word_flag():
    logic = make_logic(word_checker=lambda w: False)
    type_word(logic, "CRANE")
    logic.can_submit_word()
    assert logic.invalid_word is True
    logic.delete_letter()
    assert logic.invalid_word is False


def test_delete_letter_returns_false_after_game_over():
    logic = make_logic("CRANE")
    submit(logic, "CRANE")
    logic.add_letter('A')
    assert logic.delete_letter() is False


def test_can_add_letter_true_when_space_available():
    logic = make_logic()
    assert logic.can_add_letter() is True


def test_can_add_letter_false_when_row_full():
    logic = make_logic()
    type_word(logic, "CRANE")
    assert logic.can_add_letter() is False


def test_can_add_letter_false_after_game_over():
    logic = make_logic("CRANE")
    submit(logic, "CRANE")
    assert logic.can_add_letter() is False


def test_can_delete_letter_true_when_char_gt_zero():
    logic = make_logic()
    logic.add_letter('A')
    assert logic.can_delete_letter() is True


def test_can_delete_letter_false_when_char_is_zero():
    logic = make_logic()
    assert logic.can_delete_letter() is False


def test_can_delete_letter_false_after_game_over():
    logic = make_logic("CRANE")
    submit(logic, "CRANE")
    assert logic.can_delete_letter() is False
