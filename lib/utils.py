class Utils:

    @staticmethod
    def extract_contents_of_nested_brackets(s):
        """
        string:    J6 (Birmingham) and J7 (Birmingham (N) / Walsall)
        should be: ["Birmingham", "Birmingham (N) / Walsall"]
        """
        contents = []
        index = 0
        last_index = len(s)

        while index < last_index:
            # Scan through the string looking for an open bracket
            char = s[index]
            index += 1

            if char == '(':
                word = ""

                index2 = index  # Prevent scanning from the start
                while index2 < last_index:
                    char2 = s[index2]
                    index2 += 1

                    if char2 == ')':
                        # Check if all of the nested brackets are accounted for meaning
                        # The scanner has found the outmost bracket
                        if word.count('(') == word.count(')'):
                            contents.append(word)
                            index = index2
                            break

                    word += char2  # The bracket is nested so include it
                    continue

        return contents
