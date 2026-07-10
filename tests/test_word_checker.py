from conftest import make_logic, type_word


def test_can_submit_word_false_when_row_not_full():
    logic = make_logic()
    type_word(logic, "CRAN")
    assert logic.can_submit_word() is False


def test_can_submit_word_true_when_row_full_and_checker_passes():
    logic = make_logic(word_checker=lambda w: True)
    type_word(logic, "CRANE")
    assert logic.can_submit_word() is True


def test_can_submit_word_false_when_checker_rejects():
    logic = make_logic(word_checker=lambda w: False)
    type_word(logic, "CRANE")
    assert logic.can_submit_word() is False


def test_invalid_word_flag_set_when_checker_rejects():
    logic = make_logic(word_checker=lambda w: False)
    type_word(logic, "CRANE")
    logic.can_submit_word()
    assert logic.invalid_word is True


def test_invalid_word_flag_not_set_when_checker_accepts():
    logic = make_logic(word_checker=lambda w: True)
    type_word(logic, "CRANE")
    logic.can_submit_word()
    assert logic.invalid_word is False


def test_submit_word_returns_none_when_row_not_full():
    logic = make_logic()
    type_word(logic, "CRAN")
    assert logic.submit_word() is None


def test_submit_word_returns_none_when_checker_rejects():
    logic = make_logic(word_checker=lambda w: False)
    type_word(logic, "CRANE")
    assert logic.submit_word() is None


def test_word_checker_receives_uppercase_string():
    received = []
    logic = make_logic(word_checker=lambda w: received.append(w) or True)
    type_word(logic, "crane")
    logic.can_submit_word()
    assert received == ["CRANE"]


def test_word_checker_called_with_full_guess():
    received = []
    logic = make_logic("CRANE", word_checker=lambda w: received.append(w) or True)
    type_word(logic, "SLATE")
    logic.submit_word()
    assert received[0] == "SLATE"
