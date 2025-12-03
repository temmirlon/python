from tree_sitter import Language, Parser
import os

cpp_grammar_path = r'/Users/temmirlon/Documents/все что связано with coding/projects/python/tree-sitter-cpp-master'

build_path = 'build/my-language.so'
if not os.path.exists(build_path):
    Language.build_library(
        build_path,
        [cpp_grammar_path]
    )

CPP_LANG = Language(build_path, 'cpp')
parser = Parser()
parser.set_language(CPP_LANG)


# func for search of log calls
def FindLogCalls(node):
    if node.type == "call_expression":
        args_node = node.child_by_field_name("arguments")
        if args_node:
            for arg in args_node.children:
                if arg.type == "string_literal":
                    arg_text = arg.text.decode("latin-1")

                    if "%s" in arg_text or "[{}]" in arg_text or "[%s]" in arg_text:
                        yield node
                        break  # Found

    for child in node.children:
        yield from FindLogCalls(child)


# get pattern
def GetArguments(call_node):
    args_node = call_node.child_by_field_name("arguments")

    result = []
    for arg in args_node.children:
        if arg.type in (',', '(', ')') or arg.type == "comment":
            continue
        result.append(arg)

    return result


def LogRefactor(func_name, args):
    if not args:
        return func_name + "()"

    fmt = args[0]

    if fmt.startswith('"') and fmt.endswith('"'):
        new_fmt = fmt.replace("[{}]", "").replace("[{} ]", "")
    else:
        new_fmt = fmt

    new_args = [new_fmt]
    for a in args[1:]:
        if a.strip() in ("strFN", "strFn"):
            continue
        new_args.append(a)

    return f"{func_name}({', '.join(new_args)});"


def main():
    FILE_PATH = 'E:\\cpp\\practice\\SPCreateDrawingPartDF.cpp'

    with open(FILE_PATH, 'r', encoding='latin-1') as f:
        content = f.read()

    tree = parser.parse(bytes(content, 'latin-1'))
    root_node = tree.root_node

    num = 0

    for call in FindLogCalls(root_node):
        func_name = call.child_by_field_name("function").text.decode("latin-1")
        args_nodes = GetArguments(call)

        args_text = [arg.text.decode('latin-1') for arg in args_nodes]

        new_log = LogRefactor(func_name, args_text)

        num += 1

        print("\n === ORIGINAL ===")
        print(f"{func_name}({', '.join(args_text)});")
        print("\n === REFACTORED ===")
        print(new_log)

    print(f"FOUNDS: {num}")


if __name__ == "__main__":
    main()