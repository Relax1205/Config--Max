import struct
import json
import argparse
import sys

# Команды УВМ
COMMANDS = {
    "LOAD_CONST": 0x3E,
    "LOAD_MEMORY": 0x58,
    "STORE_MEMORY": 0x39,
    "NOT": 0x89,
}

# Тестовые данные
TEST_CASES = [
    # Загрузка константы
    {
        "description": "Загрузка константы (LOAD_CONST) с операндом 38",
        "instruction": {"command": "LOAD_CONST", "operand": 38},
        "expected": b"\x3E\x26\x00\x00\x00"  # 38 в little-endian формате
    },
    # Чтение значения из памяти
    {
        "description": "Чтение значения из памяти (LOAD_MEMORY)",
        "instruction": {"command": "LOAD_MEMORY"},
        "expected": b"\x58\x00\x00\x00\x00"
    },
    # Запись значения в память
    {
        "description": "Запись значения в память (STORE_MEMORY) с адресом 112",
        "instruction": {"command": "STORE_MEMORY", "operand": 112},
        "expected": b"\x39\x70\x00\x00\x00"  # 112 в little-endian формате
    },
    # Унарная операция: побитовое "не"
    {
        "description": "Побитовое 'не' (NOT) с адресом 689",
        "instruction": {"command": "NOT", "operand": 689},
        "expected": b"\x89\xB1\x02\x00\x00"  # 689 в little-endian формате
    },
]

def run_tests():
    """Выполняет тесты и проверяет корректность работы ассемблера."""
    all_tests_passed = True

    print("Запуск тестов...")
    for i, test in enumerate(TEST_CASES):
        description = test["description"]
        instruction = test["instruction"]
        expected = test["expected"]

        # Преобразуем команду в бинарный формат
        cmd = instruction["command"]
        opcode = COMMANDS.get(cmd)
        if opcode is None:
            raise ValueError(f"Unknown command in test: {cmd}")
        
        operand = instruction.get("operand", 0)
        binary_instruction = pack_instruction(opcode, operand)

        # Вывод информации о тесте
        print(f"\nТест {i + 1}: {description}")
        print(f"Предполагалось: {expected}")
        print(f"Получилось:     {binary_instruction}")

        # Сравнение результатов
        if binary_instruction == expected:
            print("Результат: Успешно ✅")
        else:
            print("Результат: Ошибка ❌")
            all_tests_passed = False

    if all_tests_passed:
        print("\nВсе тесты успешно выполнены! ✅")
    else:
        print("\nНекоторые тесты завершились с ошибкой. ❌")
        sys.exit(1)

def pack_instruction(opcode, operand):
    """Упаковывает инструкцию в зависимости от её типа."""
    return struct.pack("<BI", opcode, operand)

def assemble(input_file, output_file, log_file):
    with open(input_file, 'r') as asm_file, open(output_file, 'wb') as bin_file, open(log_file, 'w') as log:
        program = json.load(asm_file)
        log_data = []
        for instruction in program:
            cmd = instruction["command"]
            opcode = COMMANDS.get(cmd)
            if opcode is None:
                raise ValueError(f"Unknown command: {cmd}")
            
            operand = instruction.get("operand", 0)
            binary_instruction = pack_instruction(opcode, operand)
            bin_file.write(binary_instruction)
            
            log_data.append({"command": cmd, "opcode": opcode, "operand": operand})
        
        json.dump(log_data, log, indent=4)

if __name__ == "__main__":
    # Выполняем тесты перед сборкой
    run_tests()

    # Парсер аргументов командной строки
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Input JSON file")
    parser.add_argument("output", help="Output binary file")
    parser.add_argument("log", help="Log file")
    args = parser.parse_args()

    # Сборка программы
    assemble(args.input, args.output, args.log)
