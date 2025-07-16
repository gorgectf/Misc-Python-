def validate_input(word, c1, c2, c3) -> bool:
    valid = 0

    if len(word) >= 0:
        valid += 1

    if c1.isdigit():
        valid += 1
    
    if c2.isdigit():
        valid += 1

    if c3.isdigit():
        valid += 1

    if valid == 4: return True
    return False

def worder(word: str, c1: int, c2: int, c3: int) -> list[str]:
    letters: list[str] = ["-X" for _ in range(3)]
    local_word: str = word
    length: int = len(local_word)
    char_one: str = "-X"
    char_two: str = "-X"
    char_thr: str = "-X"

    if 0 <= c1 - 1 <= length - 1:
        char_one = local_word[c1 - 1]

    if 0 <= c2 - 1 <= length - 1:
        char_two = local_word[c2 - 1]

    if 0 <= c3 - 1 <= length - 1:
        char_thr = local_word[c3 - 1]

    letters[0] = char_one
    letters[1] = char_two
    letters[2] = char_thr

    return letters
    
print("Worder App")
print("--------------------------------------------------------------------------------------")
print("If the result shows '-X' then that is not present in the string.")
while True:
    try:
        word: str = input("Input your word: ")
        pos_1: int = input("Position 1: ")
        pos_2: int = input("Position 2: ")
        pos_3: int = input("Position 3: ")
    except Exception as e:
        print("Input valid data.")
        continue
    
    if validate_input(word, pos_1, pos_2, pos_3, ):
        pos_1 = int(pos_1)
        pos_2 = int(pos_2)
        pos_3 = int(pos_3)

        characters = worder(word, pos_1, pos_2, pos_3)

        print(characters)
    else:
        print("Input valid data.")