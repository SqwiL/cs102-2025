from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    """

    :param rows:
    :param cols:
    :return:
    """
    return [["■"] * cols for _ in range(rows)]


def remove_wall(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param coord:
    :return:
    """

    x, y = coord
    index_last_col = len(grid[0]) - 1
    direction = choice(("up", "right"))

    if direction == "up":
        if x > 1:
            grid[x - 1][y] = " "
        elif y < index_last_col - 1:
            grid[x][y + 1] = " "
    else:
        if y < index_last_col - 1:
            grid[x][y + 1] = " "
        elif x > 1:
            grid[x - 1][y] = " "

    return grid


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> List[List[Union[str, int]]]:
    """

    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """

    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    for cur_coord in empty_cells:
        remove_wall(grid, cur_coord)

    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """

    :param grid:
    :return:
    """

    exits = []

    for x in range(len(grid)):
        for y in range(len(grid[x])):
            if grid[x][y] == "X":
                exits.append((x, y))
                if len(exits) == 2:
                    return exits
    return exits


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param k:
    :return:
    """

    number_rows = len(grid)
    number_cols = len(grid[0])

    for x in range(number_rows):
        for y in range(number_cols):
            if grid[x][y] == k:
                k += 1
                neighbors = [(x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)]
                for coord_x, coord_y in neighbors:
                    if 0 <= coord_x < number_rows and 0 <= coord_y < number_cols and (grid[coord_x][coord_y] == 0):
                        grid[coord_x][coord_y] = k
                k -= 1

    return grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """

    :param grid:
    :param exit_coord:
    :return:
    """

    number_rows = len(grid)
    number_cols = len(grid[0])

    x, y = exit_coord
    k = int(grid[x][y])
    path = [(x, y)]

    while grid[x][y] != 1:
        k -= 1
        neighbors = [(x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)]
        for coord_x, coord_y in neighbors:
            if 0 <= coord_x < number_rows and 0 <= coord_y < number_cols:
                if grid[coord_x][coord_y] == k:
                    path.append((coord_x, coord_y))
                    x, y = coord_x, coord_y
                    break

    return path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """

    :param grid:
    :param coord:
    :return:
    """

    number_rows = len(grid)
    number_cols = len(grid[0])
    x, y = coord

    if x in (0, number_rows - 1) and y in (0, number_cols - 1):
        return True

    if x == 0 and grid[x + 1][y] != " ":
        return True

    if x == number_rows - 1 and grid[x - 1][y] != " ":
        return True

    if y == 0 and grid[x][y + 1] != " ":
        return True

    if y == number_cols - 1 and grid[x][y - 1] != " ":
        return True

    return False


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    """

    :param grid:
    :return:
    """

    exits = get_exits(grid)

    if len(exits) == 1:
        return grid, exits

    for poss_exit in exits:
        if encircled_exit(grid, poss_exit):
            return grid, None

    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == " ":
                grid[x][y] = 0

    start_x, start_y = exits[0]
    finish_x, finish_y = exits[1]

    grid[start_x][start_y] = 1
    grid[finish_x][finish_y] = 0
    k = 1

    while grid[finish_x][finish_y] == 0:
        make_step(grid, k)
        k += 1

    path = shortest_path(grid, (finish_x, finish_y))

    return grid, path


def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param path:
    :return:
    """

    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
