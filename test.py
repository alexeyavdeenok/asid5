import unittest
from maze import Maze


class TestMazeFunctions(unittest.TestCase):
    def setUp(self):
        """
        Настройка окружения для тестов: создание пустого лабиринта.
        """
        self.maze = Maze(3, 3)

    def test_solve_maze_default(self):
        """
        Проверка решения лабиринта по умолчанию.
        """
        self.maze.generate_maze()
        path = self.maze.solve_maze()
        self.assertTrue(path, "Путь должен существовать.")
        self.assertEqual(path[0], (1, 1), "Начальная точка пути некорректна.")
        self.assertEqual(path[-1], (5, 5), "Конечная точка пути некорректна.")

    def test_solve_maze_invalid_start(self):
        """
        Проверка обработки недопустимой стартовой позиции.
        """
        with self.assertRaises(ValueError):
            self.maze.solve_maze(start=(-1, 0))

    def test_solve_maze_invalid_end(self):
        """
        Проверка обработки недопустимой конечной позиции.
        """
        with self.assertRaises(ValueError):
            self.maze.solve_maze(end=(10, 10))

    def test_generate_maze_structure(self):
        """
        Проверка структуры сгенерированного лабиринта.
        """
        self.maze.generate_maze()
        list_maze = self.maze.list_maze

        # Лабиринт должен быть полностью окружен стенами
        for row in list_maze[0] + list_maze[-1]:
            self.assertEqual(row, '0', "Границы лабиринта должны быть стенами.")
        for row in list_maze:
            self.assertEqual(row[0], '0', "Левые границы лабиринта должны быть стенами.")
            self.assertEqual(row[-1], '0', "Правые границы лабиринта должны быть стенами.")

        # Проверка наличия проходимых клеток
        self.assertTrue(any('1' in row for row in list_maze), "Лабиринт должен содержать проходимые клетки.")

    def test_generate_maze_connectivity(self):
        """
        Проверка соединенности сгенерированного лабиринта.
        """
        self.maze.generate_maze()
        path = self.maze.solve_maze()
        self.assertTrue(path, "Сгенерированный лабиринт должен быть проходимым.")

    def test_generate_maze_size(self):
        """
        Проверка размеров лабиринта.
        """
        self.maze.generate_maze()
        self.assertEqual(len(self.maze.list_maze), 7, "Высота лабиринта должна быть корректной.")
        self.assertEqual(len(self.maze.list_maze[0]), 7, "Ширина лабиринта должна быть корректной.")

    def test_maze_surrounded_by_walls(self):
        """
        Проверка, что лабиринт окружён стенами.
        """
        self.maze.generate_maze()

        # Верхняя и нижняя границы
        for cell in self.maze.list_maze[0] + self.maze.list_maze[-1]:
            self.assertEqual(cell, '0', "Лабиринт должен быть окружён стенами сверху и снизу.")

        # Левая и правая границы
        for row in self.maze.list_maze:
            self.assertEqual(row[0], '0', "Лабиринт должен быть окружён стенами слева.")
            self.assertEqual(row[-1], '0', "Лабиринт должен быть окружён стенами справа.")

    def test_path_contains_start_and_end(self):
        """
        Проверка, что путь содержит начальную и конечную точку, если они корректны.
        """
        start = (0, 0)
        end = (2, 2)
        self.maze.generate_maze()
        self.maze.solve_maze(start, end)
        # Преобразуем начальную и конечную позиции в координаты реального лабиринта
        start_real = (2 * start[0] + 1, 2 * start[1] + 1)
        end_real = (2 * end[0] + 1, 2 * end[1] + 1)

        # Проверяем наличие начальной и конечной точки в пути
        self.assertIn(start_real, self.maze.list_way, "Начальная точка должна быть в пути.")
        self.assertIn(end_real, self.maze.list_way, "Конечная точка должна быть в пути.")


if __name__ == "__main__":
    unittest.main()
