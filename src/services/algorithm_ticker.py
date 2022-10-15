from util.enums import GridType, ResultType
import time


class AlgorithmTicker:

    def __init__(self, ui_logic, grid, algorithm, step_interval=0.025):
        self.ui_logic = ui_logic
        self.grid = grid
        self.algorithm = algorithm

        # Defaults to 25ms
        self.step_interval = step_interval

        self.time_in_ns = 0
        self.steps_taken = 0

    def instant_find(self):
        """Suorittaa algoritmin välittömästi.
        Hyödyllinen
        """

        # Reset stat variables
        self.time_in_ns = 0
        self.steps_taken = 0

        current_time = time.time_ns()
        while not self.algorithm.final_path:
            self.algorithm.step()
            self.steps_taken += 1
        self.time_in_ns += time.time_ns() - current_time

    def start_ticker(self):
        """Aloittaa algorithmin looppauksen annetulla askelvälillä (def: 25ms)
        Reitti piirretään automaattisesti gridille.
        """

        if self.algorithm.draw:
            # Delete everything unnecessary from grid
            self.reset_grid()

        # Reset stat variables
        self.time_in_ns = 0
        self.steps_taken = 0

        # Loop till final path is found (or not found)
        while not self.algorithm.final_path:
            current_time = time.time_ns()

            # Make the algorithm take its next step
            self.algorithm.step()

            self.time_in_ns += time.time_ns() - current_time
            self.steps_taken += 1

            # Wait some before starting next step so
            # algorithm can be visualized better
            time.sleep(self.step_interval)

        if self.algorithm.final_path == ResultType.NOT_FOUND:
            return

        if self.algorithm.draw:
            self.draw_path(self.algorithm.final_path[0], GridType.FINAL_PATH)

    def get_time_in_ms(self):
        """
        :return: algoritmin suoritusaika millisekunteina
        """
        return self.time_in_ns * 0.000001

    def get_distance(self):
        """
        :return: algoritmin löytämän reitin pituus
        """
        return self.algorithm.final_path[1] \
            if self.algorithm.final_path and self.algorithm.final_path != ResultType.NOT_FOUND \
            else -1

    def draw_at(self, x, y, grid_type):
        """Piirtää yksittäiseen pisteeseen gridille.

        :param x: x koordinaatti
        :param y: y koordinaatti
        :param grid_type: väri millä piirretään
        """
        self.ui_logic.draw_rectangle(x, y, grid_type)

    def draw_path(self, path, grid_type):
        """Piirtää annetun listan gridille.

        :param path: (x, y) tuple lista piirto koordinaateista
        :param grid_type: väri millä piirretään
        """
        for xy in path:
            self.ui_logic.draw_rectangle(xy[0], xy[1], grid_type)

    def reset_grid(self):
        """Piirtää gridistä kaiken muun pois paitsi aloituspisteen,
        lopetuspisteen ja seinät

        """
        for y in range(len(self.ui_logic.grid)):
            for x in range(len(self.ui_logic.grid[y])):
                self.ui_logic.draw_rectangle(x, y, self.ui_logic.grid[y][x])
