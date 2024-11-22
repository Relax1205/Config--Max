import os
import tempfile
import zipfile
import shutil
from shell_emulator import ShellEmulator

def prepare_vfs():
    temp_dir = tempfile.mkdtemp()
    vfs_zip_path = os.path.join(temp_dir, "vfs.zip")

    fs_structure = {
        "file1.txt": "Hello World\nThis is a test file.\n",
        "dir1/": None,
        "dir1/file2.txt": "Another file in a directory.\n"
    }

    with zipfile.ZipFile(vfs_zip_path, 'w') as zf:
        for path, content in fs_structure.items():
            full_path = os.path.join(temp_dir, path)
            if path.endswith('/'):
                os.makedirs(full_path, exist_ok=True)
            else:
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, 'w') as f:
                    f.write(content)
            zf.write(full_path, arcname=path)

    return temp_dir, vfs_zip_path

def run_tests():
    temp_dir, vfs_zip_path = prepare_vfs()
    emulator = ShellEmulator("testhost", vfs_zip_path)

    try:
        print("=== Тест команды ls ===")
        emulator.ls()
        entries = os.listdir(emulator.temp_dir)
        assert "file1.txt" in entries
        assert "dir1" in entries

        print("=== Тест команды cd ===")
        emulator.cd("dir1")
        assert emulator.current_dir.endswith("dir1")
        emulator.cd("..")
        assert emulator.current_dir == emulator.temp_dir
        print("cd работает корректно.")

        print("=== Тест команды wc ===")
        emulator.wc("file1.txt")
        file_path = os.path.join(temp_dir, "file1.txt")
        with open(file_path, 'r') as f:
            content = f.read()
            assert len(content.splitlines()) == 2
            assert len(content.split()) == 7
            assert len(content) == 33
        print("wc работает корректно.")

        print("=== Тест команды rmdir ===")
        # Создаём директорию вручную
        test_dir_path = os.path.join(emulator.current_dir, "test_dir")
        os.makedirs(test_dir_path)
        print(f"Создана директория: {test_dir_path}")
        emulator.rmdir("test_dir")
        assert not os.path.exists(test_dir_path), "Ошибка: директория не была удалена!"
        print("rmdir работает корректно.")

    finally:
        shutil.rmtree(temp_dir)

if __name__ == "__main__":
    run_tests()
    print("Все тесты прошли успешно!")
