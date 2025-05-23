# Copyright (c) 2024-2025 iiPython

# Modules
import re
import operator
from pathlib import Path
from argparse import ArgumentParser

from .stack import NullDataInOperation, Stack, StackError
from .construct import construct_program

# Regex assignments
variable_regex = re.compile(r"\&(\w+)")
allocation_regex = re.compile(r":\[(\d+)\]")
string_sub_regex = re.compile(r"(\$\w+)")

# Handle loading file
def process_file(filepath: Path, debug: bool = False) -> None:
    file_lines = [line.strip() for line in filepath.read_text().splitlines() if line.strip()]

    # Initialize
    program = construct_program(file_lines)
    stack = Stack(program.byte_size)

    # Handle values
    def process_value(value: str) -> str | int:
        if value[0] == "&":
            if not value[1:]:
                raise SyntaxError

            return stack.get_variable(value[1:])

        if value.lstrip("-").isnumeric():
            return int(value)

        if not (value[0] == "\"" and value[-1] == "\"" and len(value) > 1):
            raise SyntaxError

        value = value.strip("\"")
        for variable in re.findall(string_sub_regex, value):
            value = value.replace(variable, str(stack.get_variable(variable[1:])))

        return value.encode("latin-1", "backslashreplace").decode("unicode-escape")

    def handle_variable(variable: str, regex: re.Pattern = variable_regex) -> str:
        variable_match = re.match(regex, variable)
        if not variable_match:
            raise SyntaxError

        return variable_match.group(1)

    # Handle iteration
    current_line, comparison_result = 0, None
    while current_line <= len(program.lines) - 1:
        if debug:
            print(f"\033[2J\033[H\033[32m[Execute] {' '.join(program.lines[current_line])}\033[0m")
            for name, register in stack.vars.items():
                value = getattr(register, "value", None)
                if value is None:
                    try:
                        value = stack.get_variable(name)

                    except NullDataInOperation:
                        value = None

                print(f"\033[90m\t[{name}] {value}\033[0m")

            print("\n\033[90m[Stepped]")
            for line in program.lines[:current_line]:
                print(f"\t{' '.join(line)}")

            input("\n\033[33mPress [ENTER] to step.\033[0m")

        try:
            match program.lines[current_line]:
                case ["out", message]:
                    print(process_value(message))

                case ["lbl", _]:
                    pass

                case ["ext", code]:
                    exit(process_value(code))

                case ["cls"]:
                    print("\033[2J\033[H", end = "", flush = True)
            
                case ["alc", variable, allocation]:
                    stack.allocate_variable(
                        handle_variable(variable),
                        int(handle_variable(allocation, allocation_regex))
                    )

                case ["inp", prompt, ">", variable]:
                    value = process_value(prompt)
                    if not isinstance(value, str):
                        raise ValueError("argument to inp must be a STRING")

                    stack.write_variable(handle_variable(variable), input(value))

                case ["add" | "sub" | "mul" | "div" | "pow" as operator_type, num1, num2, ">", variable]:
                    stack.write_variable(
                        handle_variable(variable),
                        getattr(operator, operator_type if operator_type != "div" else "truediv")(process_value(num1), process_value(num2))
                    )

                case ["cst", variable, "STRING" | "INTEGER" as cast_type]:
                    variable = handle_variable(variable)
                    stack.write_variable(
                        variable,
                        {"INTEGER": int, "STRING": str}[cast_type](stack.get_variable(variable))
                    )

                case ["cmp", variable1, variable2]:
                    variable1, variable2 = process_value(variable1), process_value(variable2)
                    if variable1 == variable2:
                        comparison_result = "jeq"

                    elif variable1 != variable2:
                        comparison_result = "jne"

                    # Ensure our types are the same
                    elif type(variable1) is not type(variable2):
                            raise ValueError("comparison variable types must be same when using >/</>=/<=")

                    elif variable1 > variable2:  # type: ignore | Checked above
                        comparison_result = "jgt"

                    elif variable1 < variable2:  # type: ignore | Checked above
                        comparison_result = "jlt"

                    elif variable1 >= variable2:  # type: ignore | Checked above
                        comparison_result = "jge"

                    elif variable1 <= variable2:  # type: ignore | Checked above
                        comparison_result = "jle"

                case ["jeq" | "jne" | "jgt" | "jlt" | "jge" | "jle" as jump_type, label]:
                    if comparison_result == jump_type:
                        current_line = program.labels[label]
                        continue

                case ["drp", variable]:
                    stack.drop_variable(handle_variable(variable))

                case [value, ">", variable]:
                    stack.write_variable(handle_variable(variable), process_value(value))

                case _ as default:
                    raise SyntaxError(default)

        except Exception as e:
            if isinstance(e, (StackError, SyntaxError)):
                raise e

            slx_code = 1

        else:
            slx_code = 0

        stack.write_variable("slx", slx_code, reserved = True)
        current_line += 1

if __name__ == "__main__":
    shell = ArgumentParser(prog = "8255", description = "A programming language.", epilog = "(c) 2024-2025 iiPython")
    shell.add_argument("filepath", type = Path)
    shell.add_argument("-d", "--debug", action = "store_true")
    args = shell.parse_args()
    process_file(args.filepath, args.debug)
