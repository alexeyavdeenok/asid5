import random
from collections import deque
from typing import Tuple, List
from PIL import Image

def maze_check(maze: list) -> bool:
    """
    Проверяет корректность лабиринта.

    Условия:
    1. Лабиринт должен быть окружён стенами (значениями '0').
    2. Внутренняя клетка '1' не должна быть полностью окружена стенами.

    Args:
        maze (list): Двумерный массив лабиринта.

    Returns:
        bool: True, если лабиринт корректный, иначе False.

    Raises:
        ValueError: Если лабиринт некорректен.
    """
    rows = len(maze)
    cols = len(maze[0])

    # Проверка, что лабиринт окружён стенами
    if any(cell != '0' for cell in maze[0] + maze[-1]):  # Верхняя и нижняя границы
        raise ValueError("Лабиринт должен быть окружён стенами сверху и снизу.")
    if any(row[0] != '0' or row[-1] != '0' for row in maze):  # Левые и правые границы
        raise ValueError("Лабиринт должен быть окружён стенами слева и справа.")

    # Проверка, что ни одна внутренняя клетка '1' не окружена стенами
    for i in range(1, rows - 1):  # Пропускаем границы
        for j in range(1, cols - 1):
            if maze[i][j] == '1':
                # Проверяем соседей (верх, низ, лево, право)
                neighbors = [
                    maze[i - 1][j],  # Верх
                    maze[i + 1][j],  # Низ
                    maze[i][j - 1],  # Лево
                    maze[i][j + 1],  # Право
                ]
                if all(neighbor == '0' for neighbor in neighbors):
                    raise ValueError(f"Клетка {i, j} окружена стенами со всех сторон.")

    return True


class Maze:
    def __init__(self, height: int, width: int):
        self.height = height
        self.width = width
        self.list_maze = []
        self.list_way = []
        self.init_base_data()

    def init_base_data(self):
        """Инициализация пустого лабиринта с внешними стенами."""
        # Создаем лабиринт размером (2*height + 1) на (2*width + 1)
        self.list_maze = [['0'] * (2 * self.width + 1) for _ in range(2 * self.height + 1)]

        # Заполнение внутренней части лабиринта пустыми клетками
        for y in range(self.height):
            for x in range(self.width):
                self.list_maze[2 * y + 1][2 * x + 1] = '1'

    def generate_maze(self):
        """Генерация лабиринта с использованием алгоритма бинарного дерева."""
        for y in range(self.height):
            for x in range(self.width):
                # Для каждой клетки выбираем, куда удалить стену: вниз или вправо
                if x == self.width - 1 and y == self.height - 1:
                    # В правом нижнем углу ничего не делаем
                    continue
                elif x == self.width - 1:  # Если мы в последнем столбце, удаляем стену вниз
                    self.list_maze[2 * y + 2][2 * x + 1] = '1'
                elif y == self.height - 1:  # Если мы в последней строке, удаляем стену вправо
                    self.list_maze[2 * y + 1][2 * x + 2] = '1'
                else:
                    # Выбираем случайное направление (вправо или вниз)
                    if random.choice([True, False]):
                        self.list_maze[2 * y + 1][2 * x + 2] = '1'  # Удаляем стену вправо
                    else:
                        self.list_maze[2 * y + 2][2 * x + 1] = '1'  # Удаляем стену вниз

    def print_maze(self):
        """Вывод лабиринта."""
        for row in self.list_maze:
            print(' '.join(row).replace('0', '#').replace('1', ' '))

    def solve_maze(self, start: Tuple[int, int] = None, end: Tuple[int, int] = None) -> List:
        """
        Решение лабиринта методом DFS от стартовой до конечной позиции.

        Args:
            start (Tuple[int, int]): Начальная позиция в виде (строка, столбец).
            end (Tuple[int, int]): Конечная позиция в виде (строка, столбец).

        Returns:
            None
        """
        if start is None:
            start = (1, 1)
        if end is None:
            end = (self.height - 1, self.width - 1)
        # Преобразование стартовой и конечной позиции в реальные координаты
        start_real = (2 * start[0] + 1, 2 * start[1] + 1)
        end_real = (2 * end[0] + 1, 2 * end[1] + 1)

        # Размеры лабиринта
        rows, cols = len(self.list_maze), len(self.list_maze[0])

        # Проверяем, что стартовая и конечная позиции корректны
        if not (0 <= start_real[0] < rows and 0 <= start_real[1] < cols):
            raise ValueError("Недопустимая стартовая позиция.")
        if not (0 <= end_real[0] < rows and 0 <= end_real[1] < cols):
            raise ValueError("Недопустимая конечная позиция.")
        if self.list_maze[start_real[0]][start_real[1]] == '0' or self.list_maze[end_real[0]][end_real[1]] == '0':
            raise ValueError("Стартовая или конечная позиция находится в стене.")

        # Стек для DFS
        stack = deque()
        stack.append((start_real, []))  # Добавляем начальную позицию и пустой путь

        # Множество для отслеживания посещённых клеток
        visited = set()

        # DFS
        while stack:
            current, path = stack.pop()
            if current in visited:
                continue

            visited.add(current)
            path = path + [current]

            # Если достигли конечной точки, сохраняем путь и выходим
            if current == end_real:
                self.list_way = path
                return path

            # Проверяем соседей (вверх, вниз, влево, вправо)
            neighbors = [
                (current[0] - 1, current[1]),  # вверх
                (current[0] + 1, current[1]),  # вниз
                (current[0], current[1] - 1),  # влево
                (current[0], current[1] + 1),  # вправо
            ]

            for neighbor in neighbors:
                n_row, n_col = neighbor
                if (
                        0 <= n_row < rows and
                        0 <= n_col < cols and
                        self.list_maze[n_row][n_col] == '1' and
                        neighbor not in visited
                ):
                    stack.append((neighbor, path))

        # Если выход из цикла, пути не существует
        self.list_way = []

    def load_maze_from_file(self, file_path: str) -> list:
        """
        Загружает лабиринт из текстового файла с проверкой на валидность.

        Args:
            file_path (str): Путь к файлу для загрузки лабиринта.

        Returns:
            list: Двумерный массив, представляющий лабиринт.

        Raises:
            ValueError: Если строки имеют разную длину или содержат символы, отличные от '0' и '1'.
        """
        maze = []
        with open(file_path, 'r') as file:
            for line in file:
                stripped_line = line.strip()
                if not stripped_line:  # Пропускаем пустые строки
                    continue

                # Проверка на допустимые символы
                if not all(char in '01' for char in stripped_line):
                    raise ValueError(f"Строка содержит недопустимые символы: {stripped_line}")

                maze.append(list(stripped_line))

        # Проверка на одинаковую длину строк
        if len(set(len(row) for row in maze)) > 1:
            raise ValueError("Строки в лабиринте имеют разное количество символов.")

        if maze_check(maze):
            self.list_maze = maze

        return maze

    def save_maze_to_file(self, file_path: str) -> None:
        """
        Сохраняет лабиринт в текстовый файл.

        Args:
            file_path (str): Путь к файлу для сохранения лабиринта.
        """
        with open(file_path, 'w') as file:
            for row in self.list_maze:
                file.write(''.join(row) + '\n')  # Преобразуем каждую строку в строку текста

    def save_maze_as_image(self, output_path: str, cell_size: int = 20):
        """
        Сохраняет лабиринт в виде изображения.

        Args:
            maze (list): Двумерный массив лабиринта.
            output_path (str): Путь для сохранения изображения.
            cell_size (int): Размер клетки в пикселях.
        """
        # Размеры изображения
        rows = len(self.list_maze)
        cols = len(self.list_maze[0])
        img_width = cols * cell_size
        img_height = rows * cell_size

        # Создаем пустое изображение
        img = Image.new('RGB', (img_width, img_height), 'white')
        pixels = img.load()

        # Заполняем изображение в соответствии с лабиринтом
        for i in range(rows):
            for j in range(cols):
                color = (0, 0, 0) if self.list_maze[i][j] == '0' else (255, 255, 255)  # Черный или белый
                for x in range(cell_size):
                    for y in range(cell_size):
                        pixels[j * cell_size + x, i * cell_size + y] = color

        # Сохранение изображения
        img.save(output_path)

    def build_right_walls(self):
        pass

    def build_bottom_walls(self):
        pass

    def check_walls(self):
        pass

    def print_solution(self):
        """Отображение решения в лабиринте."""
        for y, x in self.list_way:
            if self.list_maze[y][x] == '1':
                self.list_maze[y][x] = '.'
        self.print_maze()


def load_maze_from_image(image_path: str, cell_size: int = 20) -> list:
    """
    Импортирует лабиринт из изображения.

    Args:
        image_path (str): Путь к изображению лабиринта.
        cell_size (int): Размер клетки в пикселях.

    Returns:
        list: Двумерный массив, представляющий лабиринт.
    """
    # Открыть изображение и перевести в черно-белый режим
    img = Image.open(image_path).convert('L')  # Переводим в grayscale

    # Получаем размеры лабиринта в клетках
    rows = img.height // cell_size
    cols = img.width // cell_size

    # Создаем пустой массив для лабиринта
    maze = []

    for i in range(rows):
        row = []
        for j in range(cols):
            # Определяем верхний левый угол клетки
            top_left_x = j * cell_size
            top_left_y = i * cell_size

            # Проверяем средний пиксель клетки для определения ее цвета
            mid_x = top_left_x + cell_size // 2
            mid_y = top_left_y + cell_size // 2
            color = img.getpixel((mid_x, mid_y))

            # Черный цвет (0-127) — стена, белый (128-255) — проход
            row.append('0' if color < 128 else '1')
        maze.append(row)

    return maze



if __name__ == '__main__':
    maze = Maze(10, 10)
    maze.list_maze = load_maze_from_image('maze.png')
    maze.save_maze_as_image('maze.jpg')

