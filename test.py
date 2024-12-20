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


if __name__ == "__main__":
    unittest.main()
