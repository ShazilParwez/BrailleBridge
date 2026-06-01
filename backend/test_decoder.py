from utils import convert_to_english

def test_decoder():
    # Helper to map a string to 6-bit codes for testing
    # Reverse BRAILLE_MAP
    import json
    with open("full_alphabet_map.json", "r") as f:
        fmap = json.load(f)
    rev_map = {v: k for k, v in fmap.items()}
    
    def encode(text):
        res = []
        for c in text:
            if c.isupper():
                res.append(rev_map['CAPS'])
                res.append(rev_map[c.lower()])
            elif c.isdigit():
                if not res or res[-1] != rev_map['NUM']:
                    res.append(rev_map['NUM'])
                # map digit back to a-j
                num_to_letter = {'1':'a', '2':'b', '3':'c', '4':'d', '5':'e', '6':'f', '7':'g', '8':'h', '9':'i', '0':'j'}
                res.append(rev_map[num_to_letter[c]])
            else:
                res.append(rev_map.get(c, '?'))
        return res

    # 1. Letters
    assert convert_to_english(encode("hello")) == "hello"
    
    # 2. Numbers
    assert convert_to_english(encode("123")) == "123"
    
    # 3. Mixed Alphanumeric
    # Encode "a1b" -> 'a', NUM, '1', 'b' (exits num mode because 'b' encoded normally isn't preceded by NUM in our encode function? 
    # Actually 'b' inside num mode becomes '2'. Let's test the raw arrays.
    mixed_seq = [rev_map['a'], rev_map['NUM'], rev_map['a'], rev_map['b'], rev_map['z']]
    # Should be "a12z" because z exits num mode
    assert convert_to_english(mixed_seq) == "a12z"
    
    # 4. Punctuation
    assert convert_to_english(encode("hi!")) == "hi!"
    
    # 5. Capitalized Words
    assert convert_to_english(encode("Hello")) == "Hello"
    assert convert_to_english(encode("WORLD")) == "WORLD"
    
    print("All decoder tests passed successfully!")

if __name__ == "__main__":
    test_decoder()
