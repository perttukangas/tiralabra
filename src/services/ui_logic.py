from entities.dijkstra import Dijkstra
from entities.idastar import IDAStar
from util.enums import GridType
from util.coordinates_helper import y_out_of_bounds, x_out_of_bounds, normalize


class UILogic:

    def __init__(self, width=400, height=400, grid_size=25):
        self.draw_rectangle = None

        self.current_type = GridType.WALL
        self.start_position = None
        self.end_position = None

        self.width = width
        self.height = height
        self.grid_size = grid_size

        grid_rows = int(self.width / self.grid_size)
        grid_cols = int(self.height / self.grid_size)

        self.grid = [[GridType.NONE for _ in range(grid_cols)] for _ in range(grid_rows)]

    def start_dijkstra(self):
        print(self.start_position, self.end_position)
        print(Dijkstra(self, self.grid, self.start_position, self.end_position).find())
        return -1

    def start_idastar(self):
        print(self.start_position, self.end_position)
        print(IDAStar(self, self.grid, self.start_position, self.end_position).find())
        return -1

    def handle_motion(self, event):
        """Käsittelee canvasin motion eventin.
        Päivittää gridin ja canvasin.

        :param event: canvasin motion event
        """
        x, y = normalize(self.grid_size, event.x), normalize(self.grid_size, event.y)
        if x_out_of_bounds(self.grid, x) or y_out_of_bounds(self.grid, y):
            return

        if self.current_type == GridType.START:
            self.change_start(x, y)
        elif self.current_type == GridType.END:
            self.change_end(x, y)
        else:
            self.grid[y][x] = self.current_type
            self.draw_rectangle(x, y, self.current_type)

    def change_start(self, x, y):
        """Poistaa vanhan aloituspaikan sekä asettaa uuden annettuihin koordinaatteihin

        :param x: x koordinaatti
        :param y: y koordinaatti
        """
        if self.start_position:
            self.grid[self.start_position[1]][self.start_position[0]] = GridType.NONE
            self.draw_rectangle(self.start_position[0], self.start_position[1], GridType.NONE)

        self.start_position = (x, y)
        self.grid[y][x] = GridType.START
        self.draw_rectangle(x, y, GridType.START)

    def change_end(self, x, y):
        """Poistaa vanhan loppupaikan sekä asettaa uuden annettuihin koordinaatteihin

        :param x: x koordinaatti
        :param y: y koordinaatti
        """
        if self.end_position:
            self.grid[self.end_position[1]][self.end_position[0]] = GridType.NONE
            self.draw_rectangle(self.end_position[0], self.end_position[1], GridType.NONE)

        self.end_position = (x, y)
        self.grid[y][x] = GridType.END
        self.draw_rectangle(x, y, GridType.END)

    def wall_type(self):
        """Vaihtaa nykyisen canvasissa käytetyn värin loppupisteen väriin
        """
        self.current_type = GridType.WALL

    def start_type(self):
        """Vaihtaa nykyisen canvasissa käytetyn värin alkupisteen väriin
        """
        self.current_type = GridType.START

    def end_type(self):
        """Vaihtaa nykyisen canvasissa käytetyn värin loppupisteen väriin
        """
        self.current_type = GridType.END
