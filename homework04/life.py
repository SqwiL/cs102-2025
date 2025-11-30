import pathlib
import random
import typing as tp

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self, size: tp.Tuple[int, int], randomize: bool = True, max_generations: tp.Optional[float] = float("inf")
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.
        """
        if randomize:
            return [[random.randint(0, 1) for _ in range(self.cols)] for _ in range(self.rows)]
        else:
            return [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        x0, y0 = cell
        neighbours = []
        shift = (-1, 0, 1)

        for dx in shift:
            for dy in shift:
                if dx != 0 or dy != 0:
                    x, y = x0 + dx, y0 + dy

                    if 0 <= x < self.rows and 0 <= y < self.cols:
                        neighbours.append(self.curr_generation[x][y])

        return neighbours

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        new_grid = self.create_grid()

        for x, row in enumerate(self.curr_generation):
            for y, cell in enumerate(row):
                neighbours = self.get_neighbours((x, y))
                count_live_neighbours = sum(neighbours)
                if cell == 1:
                    if 2 <= count_live_neighbours <= 3:
                        new_grid[x][y] = 1
                    else:
                        new_grid[x][y] = 0
                else:
                    if count_live_neighbours == 3:
                        new_grid[x][y] = 1
                    else:
                        new_grid[x][y] = 0
        return new_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.max_generations is None:
            return False

        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.prev_generation != self.curr_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        grid = []
        with open(filename, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                grid.append([int(s) for s in line])

        rows = len(grid)
        cols = len(grid[0]) if rows else 0

        game = GameOfLife((rows, cols), False)
        game.curr_generation = grid
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        text = []
        for row in self.curr_generation:
            text.append("".join(map(str, row)))

        with open(filename, "w") as f:
            f.write("\n".join(text))
