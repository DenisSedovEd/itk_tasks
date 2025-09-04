# s = "AAABBCCDDD"
# "A3B2C2D3"


def run_encoding(s: str) -> str:
    if not s:
        return ""

    result = []
    count = 1
    current_char = s[0]

    for i in range(1, len(s)):
        if s[i] == current_char:
            count += 1
        else:
            result.append(current_char + str(count))
            current_char = s[i]
            count = 1
    result.append(current_char + str(count))

    return "".join(result)


if __name__ == "__main__":
    assert run_encoding("AAABBCCDDD") == "A3B2C2D3"
    assert run_encoding("AAABBCCDDDAA") == "A3B2C2D3A2"
    assert run_encoding("AAA22BB33CCDDD") == "A322B232C2D3"
    assert run_encoding("ABCD") == "A1B1C1D1"
    assert run_encoding("") == ""
