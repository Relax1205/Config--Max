import struct
import json
import argparse

# Размер памяти виртуальной машины
MEMORY_SIZE = 1024

def interpret(input_file, output_file, memory_range):
    # Инициализация памяти и регистра-аккумулятора
    memory = [0] * MEMORY_SIZE
    accumulator = 0

    # Чтение бинарного файла с программой
    with open(input_file, 'rb') as bin_file:
        instructions = bin_file.read()
    
    pc = 0  # Program counter (указатель на текущую команду)
    while pc < len(instructions):
        # Считываем команду
        opcode = instructions[pc]
        operand = struct.unpack("<I", instructions[pc+1:pc+5])[0]
        pc += 5  # Команда занимает 5 байт

        # Выполнение команды
        if opcode == 0x3E:  # LOAD_CONST
            accumulator = operand
            print(f"LOAD_CONST: Loaded {operand} into accumulator.")
        elif opcode == 0x58:  # LOAD_MEMORY
            accumulator = memory[accumulator]
            print(f"LOAD_MEMORY: Loaded value {accumulator} from memory.")
        elif opcode == 0x39:  # STORE_MEMORY
            memory[operand] = accumulator
            print(f"STORE_MEMORY: Stored {accumulator} into memory[{operand}].")
        elif opcode == 0x89:  # NOT
            accumulator = ~accumulator
            print(f"NOT: Accumulator updated to {accumulator}.")
        else:
            print(f"Unknown opcode: {opcode}")
            raise ValueError(f"Unknown opcode: {opcode}")

        # Отладочный вывод текущего состояния памяти (первые 20 адресов)
        print(f"Memory[0:20]: {memory[:20]}")

    # Сохранение указанного диапазона памяти в файл результата
    with open(output_file, 'w') as output:
        json.dump(memory[memory_range[0]:memory_range[1]], output, indent=4)
    print(f"Memory range {memory_range[0]}-{memory_range[1]} saved to {output_file}.")

if __name__ == "__main__":
    # Парсер аргументов командной строки
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Input binary file")
    parser.add_argument("output", help="Output result file")
    parser.add_argument("--range", nargs=2, type=int, help="Memory range to save", default=(0, MEMORY_SIZE))
    args = parser.parse_args()

    # Запуск интерпретатора
    interpret(args.input, args.output, args.range)
