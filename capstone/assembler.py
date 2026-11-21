import sys
import re

K = 5  # Roll number ke aakhiri 2 ank: 05

COMP_TABLE = {
    "0": "0101010", "1": "0111111", "-1": "0111010", "D": "0001100",
    "A": "0110000", "M": "1110000", "!D": "0001101", "!A": "0110001",
    "!M": "1110001", "-D": "0001111", "-A": "0110011", "-M": "1110011",
    "D+1": "0011111", "A+1": "0110111", "M+1": "1110111", "D-1": "0001110",
    "A-1": "0110010", "M-1": "1110010", "D+A": "0000010", "D+M": "1000010",
    "D-A": "0010011", "D-M": "1010011", "A-D": "0000111", "M-D": "1000111",
    "D&A": "0000000", "D&M": "1000000", "D|A": "0010101", "D|M": "1010101"
}

DEST_TABLE = {
    "": "000", "M": "001", "D": "010", "MD": "011",
    "A": "100", "AM": "101", "AD": "110", "AMD": "111"
}

JUMP_TABLE = {
    "": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
    "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"
}

def assemble(input_file):
    symbols = {
        "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
        "R0": 0, "R1": 1, "R2": 2, "R3": 3, "R4": 4, "R5": 5, "R6": 6, "R7": 7,
        "R8": 8, "R9": 9, "R10": 10, "R11": 11, "R12": 12, "R13": 13, "R14": 14, "R15": 15,
        "SCREEN": 16384, "KBD": 24576
    }

    with open(input_file, 'r') as f:
        raw_lines = f.readlines()

    # Pass 1: Comments hatana aur labels ka ROM address note karna
    cleaned_lines = []
    rom_address = 0
    seen_labels = set()

    for line_num, raw in enumerate(raw_lines, start=1):
        line = raw.split("//")[0].strip()
        if not line:
            continue
        if line.startswith("(") and line.endswith(")"):
            label = line[1:-1].strip()
            if (K % 3 == 2) and (label in seen_labels):
                print(f"Warning (Line {line_num}): Duplicate label '({label})' defined.")
            seen_labels.add(label)
            symbols[label] = rom_address
        else:
            cleaned_lines.append((line_num, line))
            rom_address += 1

    # Pass 2: Har instruction ko 16-bit binary mein badalna
    next_ram = 16
    binary_output = []

    for line_num, line in cleaned_lines:
        if line.startswith("@"):
            symbol = line[1:]
            if symbol.isdigit():
                val = int(symbol)
            else:
                if not re.match(r'^[A-Za-z_.$:][A-Za-z0-9_.$:]*$', symbol):
                    raise ValueError(f"Invalid symbol at line {line_num}: {line}")
                if symbol not in symbols:
                    symbols[symbol] = next_ram
                    next_ram += 1
                val = symbols[symbol]

            if val < 0 or val > 32767:
                raise ValueError(f"Address out of range at line {line_num}: {line}")
            binary_output.append(f"0{val:015b}")
        else:
            dest, comp, jump = "", line, ""
            if "=" in comp:
                dest, comp = comp.split("=", 1)
            if ";" in comp:
                comp, jump = comp.split(";", 1)

            dest, comp, jump = dest.strip(), comp.strip(), jump.strip()
            if dest not in DEST_TABLE or comp not in COMP_TABLE or jump not in JUMP_TABLE:
                raise ValueError(f"Syntax error at line {line_num}: {line}")

            binary_output.append(f"111{COMP_TABLE[comp]}{DEST_TABLE[dest]}{JUMP_TABLE[jump]}")

    output_file = input_file.replace(".asm", ".hack")
    with open(output_file, 'w') as f:
        f.write("\n".join(binary_output) + "\n")
    print(f"Successfully generated {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python assembler.py <filename.asm>")
    else:
        assemble(sys.argv[1])
