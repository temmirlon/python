import re
import time
start = time.time()

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
            continue

        if char in "([{<":
            depth += 1
        elif char in ")]}>":
            depth -= 1

        if char == "," and depth == 0:
            args.append("".join(current).strip())
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
        for part in smart_split(inside):
            parts.append(part)

        text = parts[0]
        args = parts[1:]

        if "[{}]" in text:
            text = text.replace("[{}] ", "").replace("[{}]", "")

        new_args = []
        for a in args:
            if a.replace(" ", "") == "strFN":
                continue
            new_args.append(a)
        args = new_args

        new_inside = ", ".join([text] + args)
        new_log = f"{level}({new_inside})"

        print(new_log)

    end = time.time()
    print("Execution time: ", end - start, "seconds")


if __name__ == "__main__":
    main()
