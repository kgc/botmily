from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

def bf(message_data, bot):
    jumps_forward = {}
    jumps_backward = {}
    jump_stack = []
    program = message_data["parsed"]
    for command_index in range(len(program)):
        command = program[command_index]
        if command == "[":
            jump_stack.append(command_index)
        if command == "]":
            left = jump_stack.pop()
            jumps_forward[left] = command_index
            jumps_backward[command_index] = left
    command_index = 0
    cells = {0: 0}
    current_cell = 0
    output_buffer = ""
    while command_index < len(program):
        if program[command_index] == ">":
            current_cell += 1
            if current_cell not in cells:
                cells[current_cell] = 0
        if program[command_index] == "<":
            current_cell -= 1
            if current_cell not in cells:
                cells[current_cell] = 0
        if program[command_index] == "+":
            cells[current_cell] += 1
        if program[command_index] == "-":
            cells[current_cell] -= 1
        if program[command_index] == ".":
            output_buffer += unichr(cells[current_cell])
        if program[command_index] == "[" and cells[current_cell] == 0:
            command_index = jumps_forward[command_index]
        if program[command_index] == "]" and cells[current_cell] != 0:
            command_index = jumps_backward[command_index]
        command_index += 1
    return output_buffer

commands = {"bf": bf}
triggers = []

