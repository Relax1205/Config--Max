import json
import subprocess
from assembler import assemble  # Импорт только функции сборки программы
from interpreter import interpret  # Импорт только функции интерпретации

def create_test_program():
    """Создаёт входной файл с программой для выполнения побитового 'НЕ' над вектором."""
    vector = [1, 2, 3, 4, 5, 6]
    program = []
    for i, value in enumerate(vector):
        program.append({"command": "LOAD_CONST", "operand": value})  # Загрузить значение
        program.append({"command": "NOT", "operand": 100 + i})      # Побитовый 'НЕ'
        program.append({"command": "STORE_MEMORY", "operand": 100 + i})  # Сохранить результат
    
    # Сохранение программы в input_test.json
    with open("input_test.json", "w") as f:
        json.dump(program, f, indent=4)

    print("Тестовая программа создана в 'input_test.json'.")

def run_assembler():
    """Запускает ассемблер для компиляции программы."""
    input_file = "input_test.json"
    output_file = "program_test.bin"
    log_file = "log_test.json"
    assemble(input_file, output_file, log_file)
    print("Программа успешно скомпилирована в 'program_test.bin'.")

def run_interpreter():
    """Запускает интерпретатор для выполнения программы."""
    input_file = "program_test.bin"
    output_file = "result_test.json"
    memory_range = (100, 106)  # Диапазон адресов для сохранения результата
    interpret(input_file, output_file, memory_range)
    print("Программа выполнена. Результаты сохранены в 'result_test.json'.")

def check_results():
    """Проверяет результаты выполнения программы."""
    with open("result_test.json", "r") as f:
        results = json.load(f)
    print("Результат выполнения программы:")
    for i, value in enumerate(results):
        print(f"Элемент {i}: {value}")

if __name__ == "__main__":
    try:
        create_test_program()
        run_assembler()
        run_interpreter()
        check_results()
    except Exception as e:
        print(f"Произошла ошибка: {e}")
