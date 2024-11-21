def text_to_pattern(text):
    result = []
    
    # Vzor pro kódování (střídání # a * podle binárního kódu)
    for char in text:
        # Získání ASCII hodnoty znaku a převod na binární řetězec
        bin_value = bin(ord(char))[2:].zfill(8)
        
        # Vytvoření patternu z binárního řetězce
        pattern = ''.join('#' if bit == '0' else '*' for bit in bin_value)
        
        # Přidání patternu do výsledného seznamu
        result.append(pattern)
    
    # Pokud je méně než 10 řádků, přidáme prázdné řádky pro naplnění
    while len(result) < 10:
        result.append('#' * 16)  # Přidání prázdných řádků s #
    
    return '\n'.join(result)

def pattern_to_text(pattern):
    lines = pattern.split('\n')
    text = ""
    
    for line in lines:
        if len(line) < 8:  # Pokud je řádek příliš krátký, ignorujeme ho
            continue
        # Převedení patternu zpět na binární hodnoty
        bin_value = ''.join('0' if char == '#' else '1' for char in line[:8])  # Používáme prvních 8 znaků
        
        # Převedení binárního řetězce na ASCII hodnotu
        char = chr(int(bin_value, 2))
        text += char
    
    return text

# Testování funkce
jmeno = "Antonín Siska"
pattern = text_to_pattern(jmeno)
print("Pattern:")
print(pattern)

decoded_text = pattern_to_text("""#*#####*
#**#***#
#***#*##
#**#****
#**#***#
***#**#*
#**#***#
##*#####
#*#*##**
#**#*##*
#***##**
#**#*#**
#**####*""")
print("\nDecoded Text:")
print(decoded_text)