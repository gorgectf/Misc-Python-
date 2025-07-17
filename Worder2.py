def word_check(word: str) -> bool:
    return " " not in word and len(word) >= 1

def character_format(pos_1: str, pos_2: str, pos_3: str, characters: list[str]) -> tuple[str, str, str]:
    string_one = f"Char {pos_1}: {characters[0]}"
    string_two = f"Char {pos_2}: {characters[1]}"
    string_thr = f"Char {pos_3}: {characters[2]}"

    return string_one, string_two, string_thr
 
def validate_numbers(c1: str, c2: str, c3: str) -> bool:
    return c1.isdigit() and c2.isdigit() and c3.isdigit()

def validate_word_positions(word: str, c1: int, c2: int, c3: int) -> tuple[bool, list[int]]:
    length = len(word)
    c1 = int(c1)
    c2 = int(c2)
    c3 = int(c3)

    expression: bool = (0 <= c1 - 1 <= length - 1) or (0 <= c2 - 1 <= length - 1) or (0 <= c3 - 1 <= length - 1)
    final: tuple[bool, list[int]] = (expression, [c1, c2, c3])
    return final

def assign_letters(word: str, c1: int, c2: int, c3: int) -> list[str]:
    letters: list[str] = ["-X" for _ in range(3)]
    result: tuple[bool, list[int]] = validate_word_positions(word, c1, c2, c3)

    if result[0]:
        numbers: list[int] = result[1]

        for i in range(len(numbers)):
            if numbers[i] - 1 > len(numbers):
                continue
            else:
                letters[i] = word[numbers[i] - 1]   
    return letters
    
def main() -> None:

    print("Worder App")
    print("--------------------------------------------------------------------------------------")
    print("Valid data: No spaces, and greater than 1 character long. Character positions must be within the word length.")
    print("'-X' signifies the character is not in the string.")

    while True:
        word: str = input("Input your word: ")
        if word_check(word):
            print(f"Word length: {len(word)}")

            while True:
                pos_1: str = input("Position 1: ")
                pos_2: str = input("Position 2: ")
                pos_3: str = input("Position 3: ")

                if validate_numbers(pos_1, pos_2, pos_3) != True:
                    print(f"Input positions within the word length: {len(word)}")
                    continue
                else:
                    break
        else:
            print("Word must be present and contain no spaces.")
            continue

        try:
            characters: list[str] = assign_letters(word, pos_1, pos_2, pos_3)

            print("-> Characters in order: ")
            strings: tuple[str, str, str] = character_format(pos_1, pos_2, pos_3, characters)
            
            for i in range(len(strings)):
                print(strings[i])
        except Exception as e:
            print(f"Exception occured {e}.")
            continue

if __name__ == "__main__":
    main()
