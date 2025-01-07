def convert_md_to_inline_text(input_file, output_file):
    try:
        # Načtení obsahu vstupního Markdown souboru
        with open(input_file, "r", encoding="utf-8") as file:
            content = file.readlines()
        
        # Přidání '\n' na konec každého řádku a odstranění skutečných zalomení
        converted_content = "\\n".join(line.strip() for line in content)
        
        # Uložení konvertovaného obsahu do výstupního souboru
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(converted_content)
        
        print(f"Obsah z '{input_file}' byl úspěšně převeden a uložen do '{output_file}'.")
    except FileNotFoundError:
        print(f"Soubor '{input_file}' nebyl nalezen.")
    except Exception as e:
        print(f"Došlo k chybě: {e}")

# Cesty ke vstupnímu a výstupnímu souboru
input_file = "/Users/antoninsiska/Documents/Projekty/Gravel-app/help/essential.md"  # Nahraď názvem svého vstupního souboru
output_file = "vystupni_soubo_docs.txt"  # Název výstupního souboru

# Zavolání funkce
convert_md_to_inline_text(input_file, output_file)