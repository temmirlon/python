import re

FILE_PATH = "/Users/temmirlon/Documents/все что связано with coding/projects/testcppfiles/SPCreateDrawingPartDFTest.cpp"

def smart_split(s: str):
    args = []
    current = []
    depth = 0
    in_str = False
    esc = False
    quote = None

    for char in s:
        if esc:
            current.append(char)
            esc = False
            continue

        if char == "\\":
            esc = True
            current.append(char)
            continue

        if char in ['"', "'"]:
            if not in_str:
                in_str = True
                quote = char
            elif quote == char:
                in_str = False
            current.append(char)
            continue

        if in_str:
            current.append(char)

        if char in "([{<":
            depth += 1
        elif char in ")]}>":
            depth -= 1

        if char == "," and depth == 0:
            args.append(current)
            current = []
            continue

        current.append(char)

    last = "".join(current).strip()
    if last:
        args.append(last)
    return args

def main():
    with open(FILE_PATH, "r", encoding="latin-1") as f:
        content = f.read()

    pattern = r'l\.(Standard|Error|Warning|Info|Debug|DebugVerbose)\s*\((.+?)\)\s*;'

    matches = re.findall(pattern, content, re.DOTALL)

    for level, inside in matches:
        parts = []
        for part in inside.split(","):
            parts.append(part.strip())

        print(parts)

if __name__ == "__main__":
    main()