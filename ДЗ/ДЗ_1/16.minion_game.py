def minion_game(string):
    vowels = 'AEIOU'
    kevin_score = 0
    stuart_score = 0
    length = len(string)
    
    for i in range(length):
        if string[i] in vowels:
            kevin_score += (length - i)
        else:
            stuart_score += (length - i)

    if kevin_score > stuart_score:
        print(f"Кевин {kevin_score}")
    elif stuart_score > kevin_score:
        print(f"Стюарт {stuart_score}")
    else:
        print("Draw")

if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    s = input()
    minion_game(s)
