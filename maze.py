import random
from collections import deque
from typing import Tuple, List


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

    def solve_maze(self, start: Tuple[int, int], end: Tuple[int, int]) -> None:
        """
        Решение лабиринта методом BFS от стартовой до конечной позиции.

        Args:
            start (Tuple[int, int]): Начальная позиция в виде (строка, столбец).
            end (Tuple[int, int]): Конечная позиция в виде (строка, столбец).

        Returns:
            None
        """
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

        # Очередь для BFS
        queue = deque()
        queue.append((start_real, []))  # Добавляем начальную позицию и пустой путь

        # Множество для отслеживания посещённых клеток
        visited = set()

        # BFS
        while queue:
            current, path = queue.popleft()
            if current in visited:
                continue

            visited.add(current)
            path = path + [current]

            # Если достигли конечной точки, сохраняем путь и выходим
            if current == end_real:
                self.list_way = path
                return

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
                    queue.append((neighbor, path))

        # Если выход из цикла, пути не существует
        self.list_way = []

    def solve_maze2(self, start: Tuple[int, int], end: Tuple[int, int]) -> None:
        """
        Решение лабиринта методом DFS от стартовой до конечной позиции.

        Args:
            start (Tuple[int, int]): Начальная позиция в виде (строка, столбец).
            end (Tuple[int, int]): Конечная позиция в виде (строка, столбец).

        Returns:
            None
        """
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
                return

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



maxe = Maze(20, 20)
maxe.generate_maze()
maxe.solve_maze2((0, 0), (19, 19))
maxe.print_solution()