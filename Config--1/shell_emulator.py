import os
import sys
import zipfile
import tempfile
import shutil
import calendar
from pathlib import Path

class ShellEmulator:
    def __init__(self, hostname, vfs_path):
        self.hostname = hostname
        self.vfs_path = vfs_path
        self.temp_dir = tempfile.mkdtemp()
        self.current_dir = self.temp_dir

        # Распаковать архив виртуальной файловой системы
        self._extract_vfs()

    def _extract_vfs(self):
        if not zipfile.is_zipfile(self.vfs_path):
            print(f"Ошибка: {self.vfs_path} не является архивом ZIP.")
            sys.exit(1)

        with zipfile.ZipFile(self.vfs_path, 'r') as zf:
            zf.extractall(self.temp_dir)

    def _prompt(self):
        relative_path = os.path.relpath(self.current_dir, self.temp_dir)
        path_display = "/" if relative_path == "." else relative_path
        return f"{self.hostname}:{path_display}$ "

    def ls(self):
        try:
            entries = os.listdir(self.current_dir)
            for entry in entries:
                print(entry)
        except Exception as e:
            print(f"Ошибка выполнения ls: {e}")

    def cd(self, path):
        new_path = os.path.abspath(os.path.join(self.current_dir, path))
        if os.path.commonpath([new_path, self.temp_dir]) != self.temp_dir or not os.path.isdir(new_path):
            print(f"Ошибка: путь {path} недоступен.")
        else:
            self.current_dir = new_path

    def wc(self, path):
        full_path = os.path.join(self.current_dir, path)
        if not os.path.isfile(full_path):
            print(f"Ошибка: {path} не является файлом.")
            return

        with open(full_path, 'r') as f:
            content = f.read()
            lines = content.splitlines()
            words = content.split()
            characters = len(content)
            print(f" {len(lines)} {len(words)} {characters} {path}")

    def rmdir(self, path):
        full_path = os.path.join(self.current_dir, path)
        if not os.path.isdir(full_path):
            print(f"Ошибка: {path} не является директорией.")
            return

        try:
            shutil.rmtree(full_path)
            print(f"Директория {path} удалена.")
        except Exception as e:
            print(f"Ошибка при удалении директории {path}: {e}")

    def cal(self, month=None, year=None):
        if month is None or year is None:
            cal = calendar.TextCalendar()
            print(cal.formatmonth(year=2023, month=11))
        else:
            try:
                month = int(month)
                year = int(year)
                if not (1 <= month <= 12):
                    raise ValueError
                cal = calendar.TextCalendar()
                print(cal.formatmonth(year, month))
            except ValueError:
                print("Ошибка: укажите правильный месяц (1-12) и год.")

    def run(self):
        try:
            while True:
                command = input(self._prompt()).strip()
                if command == "exit":
                    break
                elif command == "ls":
                    self.ls()
                elif command.startswith("cd "):
                    _, path = command.split(" ", 1)
                    self.cd(path)
                elif command.startswith("wc "):
                    _, path = command.split(" ", 1)
                    self.wc(path)
                elif command.startswith("rmdir "):
                    _, path = command.split(" ", 1)
                    self.rmdir(path)
                elif command.startswith("cal"):
                    parts = command.split()
                    if len(parts) == 3:
                        _, month, year = parts
                        self.cal(month, year)
                    else:
                        self.cal()
                else:
                    print(f"Неизвестная команда: {command}")
        finally:
            # Очистить временные файлы
            shutil.rmtree(self.temp_dir)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Использование: python shell_emulator.py <hostname> <vfs.zip>")
        sys.exit(1)

    hostname = sys.argv[1]
    vfs_path = sys.argv[2]

    emulator = ShellEmulator(hostname, vfs_path)
    emulator.run()
