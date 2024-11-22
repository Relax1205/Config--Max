import json
import subprocess
import os
from datetime import datetime
from pathlib import Path

def load_config(config_path):
    """Загружает конфигурационный файл JSON."""
    with open(config_path, 'r') as f:
        config = json.load(f)
    return config

def get_git_commits(repo_path, since_date):
    """Получает список коммитов из репозитория, начиная с указанной даты."""
    os.chdir(repo_path)
    cmd = ["git", "log", "--since", since_date, "--pretty=format:%H %P"]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
    commits = result.stdout.strip().split("\n")
    return [line.split() for line in commits]

def build_mermaid_graph(commits):
    """Формирует Mermaid-граф зависимостей коммитов."""
    graph_lines = ["graph TD"]
    commit_nodes = set()
    for commit in commits:
        node = commit[0]
        parents = commit[1:]
        commit_nodes.add(node)
        for parent in parents:
            commit_nodes.add(parent)
            graph_lines.append(f"    {node} --> {parent}")
    return "\n".join(graph_lines)

def save_graph_as_png(mermaid_code, output_path, mermaid_cli_path):
    """Сохраняет Mermaid-граф в формате PNG."""
    temp_mermaid_file = "graph.mmd"
    with open(temp_mermaid_file, "w") as f:
        f.write(mermaid_code)
    
    cmd = [mermaid_cli_path, "-i", temp_mermaid_file, "-o", output_path]
    subprocess.run(cmd, check=True)
    os.remove(temp_mermaid_file)

def main(config_path):
    """Основная функция инструмента."""
    config = load_config(config_path)
    repo_path = config["repo_path"]
    since_date = config["since_date"]
    output_path = config["output_path"]
    mermaid_cli_path = config["mermaid_cli_path"]
    
    # Проверяем существование путей
    for path in [repo_path, mermaid_cli_path]:
        if not Path(path).exists():
            raise FileNotFoundError(f"Путь не найден: {path}")

    # Получаем список коммитов
    commits = get_git_commits(repo_path, since_date)
    if not commits:
        print("Нет коммитов для указанного периода.")
        return

    # Формируем Mermaid-граф
    mermaid_graph = build_mermaid_graph(commits)

    # Сохраняем граф в формате PNG
    save_graph_as_png(mermaid_graph, output_path, mermaid_cli_path)
    print(f"Граф зависимостей успешно сохранен в {output_path}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Инструмент для построения графа зависимостей коммитов.")
    parser.add_argument("config", help="Путь к конфигурационному файлу JSON.")
    args = parser.parse_args()

    try:
        main(args.config)
    except Exception as e:
        print(f"Ошибка: {e}")
