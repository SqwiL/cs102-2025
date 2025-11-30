import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """Отобразить рамку."""

        rows, cols = self.life.rows, self.life.cols

        top_left = "┌"
        top_right = "┐"
        bottom_left = "└"
        bottom_right = "┘"
        horizontal = "─"
        vertical = "│"

        screen.addstr(0, 0, top_left + horizontal * cols + top_right)

        for r in range(1, rows + 1):
            screen.addstr(r, 0, vertical)
            screen.addstr(r, cols + 1, vertical)

        screen.addstr(rows + 1, 0, bottom_left + horizontal * cols + bottom_right)

    def draw_grid(self, screen) -> None:
        """Отобразить состояние клеток."""

        alive = "█"
        dead = " "
        for i, row in enumerate(self.life.curr_generation):
            for j, cell in enumerate(row):
                symbol = alive if cell == 1 else dead
                screen.addch(i + 1, j + 1, symbol)

    def run(self) -> None:
        """Запустить игру"""
        screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        screen.nodelay(True)

        try:
            while self.life.is_changing and not self.life.is_max_generations_exceeded:
                screen.clear()
                self.draw_borders(screen)
                self.draw_grid(screen)
                screen.refresh()

                key = screen.getch()
                if key == ord("q"):
                    break

                self.life.step()
                curses.napms(150)

        finally:
            curses.nocbreak()
            curses.echo()
            curses.endwin()


if __name__ == "__main__":
    game = GameOfLife(size=(10, 40), randomize=True)
    ui = Console(game)
    ui.run()
