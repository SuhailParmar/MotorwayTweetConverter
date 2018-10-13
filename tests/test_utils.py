from lib.utils import Utils


class TestUtils:

    u = Utils()

    def test_extract_contents_of_one_bracket(self):
        s = "J6 (Birmingham)"
        assert self.u.extract_contents_of_nested_brackets(s) ==\
            ["Birmingham"]

    def test_extract_contents_of_multiple_brackets(self):
        s = "J6 (Birmingham) and J7 (Birmingham (N) / Walsall)"
        assert self.u.extract_contents_of_nested_brackets(s) ==\
            ["Birmingham", "Birmingham (N) / Walsall"]

    def test_extract_contents_of_multiple_brackets2(self):
        s = "J6 (Birmingham) and J7 (Birmingham (N) / Walsall (S))"
        assert self.u.extract_contents_of_nested_brackets(s) ==\
            ["Birmingham", "Birmingham (N) / Walsall (S)"]

    def test_extract_contents_of_multiple_brackets3(self):
        s = "J6 (Birmingham (S)) and J7 (Birmingham (N) / Walsall (S))"
        assert self.u.extract_contents_of_nested_brackets(s) ==\
            ["Birmingham (S)", "Birmingham (N) / Walsall (S)"]