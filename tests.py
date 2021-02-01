from app import parse_args

def test_parse_args():
    # Do we want the ints to be strings or ints?
    # For now, it's all gonna be string because slack's formatting?
    io = [
        ("name [1,2,3]", "name", ['1','2','3']),
        ("name_1 [1,2,3]", "name_1", ['1','2','3']),
        ("name-1 [1,2,3]", "name-1", ['1','2','3']),
        ("12 [1,2,3]", None, ['1','2','3']),
        ("name 1 [1,2,3]", "name", None),
        ("name ]1,2,3]", "name", None),
        ("name [1,,3]", "name", None),
        ("name [1,3,]", "name", ['1', '3']),
        ("name [1, \,, \2]", "name", ['1', ',', '2']), # Trailing comma is fine, the last empty char gets removed
        ("name [\[, \], \,]", "name", ['[', ']', ',']),
        ("name []", "name", None), # array cannot be empty
        ("name [\2, \3]", "name", ['2', '3']),
        ("name [(Ali\,Shaown),(Shaown\, Ali)]", "name", ['(Ali,Shaown)', '(Shaown, Ali)']),
        ("name [A B, C D]", "name", ["A B", "C D"]),
        ("name [A   B, C D]", "name", ["A   B", "C D"]), # Space chars within the items are preserved
        ("name [A B,     C D]", "name", ["A B", "C D"]), # Space in between the items are NOT
    ]
    for (input_string, arg1, arg2) in io:
        assert parse_args(input_string) == (arg1, arg2)
