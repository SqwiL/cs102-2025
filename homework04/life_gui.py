from pathlib import Path

import pygame as pg
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size

        self.width = self.cell_size * self.life.rows
        self.height = self.cell_size * self.life.cols

        self.screen = pg.display.set_mode((self.width, self.height))

        self.speed = speed
        self.paused = False

    def draw_lines(self) -> None:
        """Отрисовать сетку"""
        for x in range(0, self.width, self.cell_size):
            pg.draw.line(self.screen, pg.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pg.draw.line(self.screen, pg.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for x, row in enumerate(self.life.curr_generation):
            for y, cell in enumerate(row):
                if cell == 1:
                    color = pg.Color("green")
                else:
                    color = pg.Color("white")

                pg.draw.rect(
                    self.screen, color, (y * self.cell_size, x * self.cell_size, self.cell_size, self.cell_size)
                )

    def handle_mouse(self, pos) -> None:
        """Меняем состояние клетки по клику мыши (только на паузе)"""
        x, y = pos
        row = y // self.cell_size
        col = x // self.cell_size
        if 0 <= row < self.life.rows and 0 <= col < self.life.cols:
            self.life.curr_generation[row][col] ^= 1

    def run(self) -> None:
        """Запустить игру"""
        pg.init()
        clock = pg.time.Clock()
        pg.display.set_caption("Game of Life")
        self.screen.fill(pg.Color("white"))
        running = True

        while running:
            for event in pg.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_q:
                        running = False
                    elif event.key == K_SPACE:
                        self.paused = not self.paused
                    elif event.key == K_w:
                        self.life.save(Path("save.txt"))
                    elif event.key == K_l:
                        self.life = GameOfLife.from_file(Path("save.txt"))
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1 and self.paused:
                        self.handle_mouse(event.pos)

            if not self.paused:
                self.life.step()

            self.draw_grid()
            self.draw_lines()
            pg.display.flip()

            clock.tick(self.speed)

        pg.quit()


if __name__ == "__main__":
    game = GameOfLife(size=(50, 50))
    gui = GUI(game)
    gui.run()
