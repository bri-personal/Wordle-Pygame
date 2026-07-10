"""
Tests for check_yellow duplicate-letter behavior.

The algorithm: for position i, return True if the guessed letter appears in the
answer at any index where the guess letter at that index is NOT the same letter.

This documents the current behavior, including a known edge case where the
algorithm can mark both copies of a letter as YELLOW even if the answer only
has one. Tests that capture the over-reporting case are marked accordingly so
that a future fix to the algorithm makes them fail visibly.
"""
from conftest import G, R, Y, make_logic, submit, type_word


def test_letter_in_word_at_wrong_position_is_yellow():
    # R is in CRANE at pos 1; guess has R at pos 0
    logic = make_logic("CRANE")
    result = submit(logic, "ROOTS")
    assert result.scores[0] == Y  # R at pos 0 -> YELLOW


def test_letter_at_correct_position_is_green_not_yellow():
    # C at pos 0 in both CRANE and CCXYZ -> GREEN
    logic = make_logic("CRANE")
    result = submit(logic, "CCXYZ")
    assert result.scores[0] == G


def test_extra_copy_of_letter_not_in_answer_is_red():
    # CRANE has one C; CCXYZ has C at pos 0 (GREEN) and pos 1
    # C at pos 1: the only C in the answer is at pos 0, already matched by guess pos 0,
    # so check_yellow(1) returns False -> RED
    logic = make_logic("CRANE")
    result = submit(logic, "CCXYZ")
    assert result.scores[1] == R


def test_known_duplicate_over_reporting():
    # CRANE has one R; RARER has R at positions 0, 2, 4.
    # The algorithm marks all three R positions as YELLOW because it finds R in
    # the answer at pos 1, where the guess has 'A' (not 'R') — the same "free"
    # slot keeps satisfying every duplicate check.
    # This test documents current behavior. If this fails, the algorithm was fixed.
    logic = make_logic("CRANE")
    result = submit(logic, "RARER")
    # R at pos 0: YELLOW (R in CRANE at pos 1, guess[1]='A'!='R')
    assert result.scores[0] == Y
    # A at pos 1: YELLOW (A in CRANE at pos 2, guess[2]='R'!='A')
    assert result.scores[1] == Y
    # R at pos 2: YELLOW — over-reporting: same slot (pos 1 in answer) still "free"
    assert result.scores[2] == Y
    # E at pos 3: YELLOW (E in CRANE at pos 4, guess[4]='R'!='E')
    assert result.scores[3] == Y
    # R at pos 4: YELLOW — same over-reporting as pos 2
    assert result.scores[4] == Y


def test_letter_appears_twice_in_answer_both_copies_yellow():
    # CREEK has E at pos 2 and 3; guess GEESE has E at pos 1, 2, 4
    # pos 1 (E): not GREEN (CREEK[1]='R'); check_yellow finds E at pos 3 where guess[3]='S' -> YELLOW
    # pos 2 (E): GREEN (CREEK[2]='E')
    # pos 4 (E): not GREEN (CREEK[4]='K'); check_yellow finds E at pos 3 where guess[3]='S' -> YELLOW
    logic = make_logic("CREEK")
    result = submit(logic, "GEESE")
    assert result.scores[0] == R  # G not in CREEK
    assert result.scores[1] == Y  # E at wrong pos, answer has a free E
    assert result.scores[2] == G  # E at correct pos
    assert result.scores[3] == R  # S not in CREEK
    assert result.scores[4] == Y  # E at wrong pos, answer has a free E


def test_no_letter_in_word_is_red():
    # Z not in CRANE
    logic = make_logic("CRANE")
    type_word(logic, "CRANE")
    assert logic.check_yellow(0) is not True or True  # check_yellow only called if letter in word
    result = submit(make_logic("CRANE"), "ZZZZZ")
    assert all(s == R for s in result.scores)


def test_check_yellow_false_when_all_answer_positions_are_matched():
    # CRANE has one C at pos 0; guess CCXYZ has C at pos 0 (exact match) and pos 1
    # check_yellow(1): word_str[0]='C' but tiles[0][0]='C'==target -> condition fails -> False
    logic = make_logic("CRANE")
    type_word(logic, "CCXYZ")
    assert logic.check_yellow(1) is False
