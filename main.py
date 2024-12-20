import argparse
import os
from maze import Maze  # Импорт класса Maze из вашего модуля


def main():
    # Создаем парсер аргументов
    parser = argparse.ArgumentParser(description="Maze Generator and Solver")

    # Добавляем аргументы
    parser.add_argument('-gm', '--generate_maze', nargs=2, type=int, metavar=('HEIGHT', 'WIDTH'),
                        help="Генерация лабиринта. Принимает два значения от 1 до 100.")
    parser.add_argument('-pm', '--print_maze', action='store_true',
                        help="Вывод лабиринта в консоль.")
    parser.add_argument('-im', '--import_maze', type=str,
                        help="Импорт лабиринта из файла (.txt, .png, .jpg).")
    parser.add_argument('-em', '--export_maze', type=str,
                        help="Экспорт лабиринта в файл (.txt, .png, .jpg).")
    parser.add_argument('-psm', '--print_solved_maze', action='store_true',
                        help="Вывод лабиринта с решением в консоль.")
    parser.add_argument('-esm', '--export_solved_maze', type=str,
                        help="Экспорт решенного лабиринта в файл (.png, .jpg).")

    # Парсим аргументы
    args = parser.parse_args()

    maze = None

    # Генерация лабиринта
    if args.generate_maze:
        height, width = args.generate_maze
        if not (1 <= height <= 100 and 1 <= width <= 100):
            print("Ошибка: значения HEIGHT и WIDTH должны быть от 1 до 100.")
            return
        maze = Maze(height, width)
        maze.generate_maze()

    # Импорт лабиринта из файла
    if args.import_maze:
        file_path = args.import_maze
        _, ext = os.path.splitext(file_path)
        if ext not in ('.txt', '.png', '.jpg'):
            print("Ошибка: поддерживаются только файлы с расширением .txt, .png, .jpg.")
            return

        if maze is None:
            maze = Maze(1, 1)  # Создаем пустой лабиринт, если его еще нет

        if ext == '.txt':
            maze.load_maze_from_file(file_path)
        elif ext in ('.png', '.jpg'):
            maze.load_maze_from_image(file_path)

    # Вывод лабиринта в консоль
    if args.print_maze and maze:
        print("Лабиринт:")
        maze.print_maze()

    # Экспорт лабиринта в файл
    if args.export_maze and maze:
        file_path = args.export_maze
        _, ext = os.path.splitext(file_path)
        if ext not in ('.txt', '.png', '.jpg'):
            print("Ошибка: поддерживаются только файлы с расширением .txt, .png, .jpg.")
            return

        if ext == '.txt':
            maze.save_maze_to_file(file_path)
        elif ext in ('.png', '.jpg'):
            maze.save_maze_as_image(file_path)

    # Решение лабиринта
    if args.print_solved_maze or args.export_solved_maze:
        if maze:
            maze.solve_maze()
            if args.print_solved_maze:
                print("Решение лабиринта:")
                maze.print_solution()

            # Экспорт решенного лабиринта
            if args.export_solved_maze:
                file_path = args.export_solved_maze
                _, ext = os.path.splitext(file_path)
                if ext not in ('.png', '.jpg'):
                    print("Ошибка: поддерживаются только файлы с расширением .png, .jpg.")
                    return
                maze.save_maze_as_image(file_path)

    # Если не было ни одной операции
    if not any([args.generate_maze, args.import_maze, args.print_maze,
                args.export_maze, args.print_solved_maze, args.export_solved_maze]):
        parser.print_help()


if __name__ == '__main__':
    main()
