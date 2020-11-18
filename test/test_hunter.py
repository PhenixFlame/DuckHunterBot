import hunter
import pytest

s1 = """** MAGAZINE EMPTY ** |
         Ammunition in the weapon: 1 / 2 |
         Magazines remaining: 3 / 4"""

s2 = "{greet} | Ammo in weapon: 1/2 | Magazines left: 3/4"

# pattern = (
#     r"(Ammunition in the weapon:|Ammo in weapon:)\s*"
#     r"(\d)\s*"    r"/\s*"    r"(\d)\s*"
#     r"\|\s*"
#     r"(Magazines remaining:|Magazines left:)\s*"
#     r"(\d)\s*"    r"/\s*"    r"(\d)\s*"
# )

AmmoPattern_test_strings = [s1, s2]


@pytest.mark.parametrize('s', AmmoPattern_test_strings)
def test_Ammo_pattern(s):
    match = hunter.Ammo.pattern.search(s)
    assert match
    assert (match[2], match[3], match[5], match[6]) == ('1', '2', '3', '4')
