import string
import re

if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    with open('example.txt', 'r', encoding='utf-8') as f:
        text = f.read()

    punctuation = string.punctuation + '«»—…'
    translator = str.maketrans(punctuation, ' ' * len(punctuation))
    cleaned_text = text.translate(translator)
    
    words = cleaned_text.split()
    
    if not words:
        exit()
        
    max_len = max(len(w) for w in words)

    max_words = [w for w in words if len(w) == max_len]

    seen = set()
    for w in max_words:
        if w not in seen:
            print(w)
            seen.add(w)
