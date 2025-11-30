import random
import typing as tp

import pygame as pg
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10) -> None:

        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pg.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

        self.grid = self.create_grid(True)

    def draw_lines(self) -> None:
        """Отрисовать сетку"""
        for x in range(0, self.width, self.cell_size):
            pg.draw.line(self.screen, pg.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pg.draw.line(self.screen, pg.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """Запустить игру"""
        pg.init()
        clock = pg.time.Clock()
        pg.display.set_caption("Game of Life")
        self.screen.fill(pg.Color("white"))

        self.grid = self.create_grid(True)

        running = True
        while running:
            for event in pg.event.get():
                if event.type == QUIT:
                    running = False

            self.draw_lines()
            self.draw_grid()

            self.grid = self.get_next_generation()

            pg.display.flip()
            clock.tick(self.speed)
        pg.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        if randomize:
            return [[random.randint(0, 1) for _ in range(self.cell_width)] for _ in range(self.cell_height)]
        else:
            return [[0 for _ in range(self.cell_width)] for _ in range(self.cell_height)]

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for x, row in enumerate(self.grid):
            for y, cell in enumerate(row):
                if cell == 1:
                    color = pg.Color("green")
                else:
                    color = pg.Color("white")

                pg.draw.rect(
                    self.screen, color, (y * self.cell_size, x * self.cell_size, self.cell_size, self.cell_size)
                )

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

                    if 0 <= x < self.cell_height and 0 <= y < self.cell_width:
                        neighbours.append(self.grid[x][y])

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

        for x, row in enumerate(self.grid):
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
