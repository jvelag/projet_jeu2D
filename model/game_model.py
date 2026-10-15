from constants import GameState, GRID_ROWS, GRID_COLS
from model.car import Car
from model.circuit import Circuit, CIRCUIT_SPECS
from model.road_tile import RoadTile


class GameModel:

    def __init__(self):
        self.state: str = GameState.MENU
        self.circuit: Circuit | None = None
        self.car: Car | None = None
        self.selected_circuit: int = 0

    def select_next_circuit(self) -> None:
        self.selected_circuit = (self.selected_circuit + 1) % len(CIRCUIT_SPECS)

    def select_previous_circuit(self) -> None:
        self.selected_circuit = (self.selected_circuit - 1) % len(CIRCUIT_SPECS)

    def load_circuit(self) -> None:
        color = CIRCUIT_SPECS[self.selected_circuit]["color"]
        grid = [[RoadTile(col=col_idx, row=row_idx, color=color)
                for col_idx in range(GRID_COLS)] for row_idx in range(GRID_ROWS)]
        self.circuit = Circuit(grid=grid)
        self.spawn_car()

    def spawn_car(self) -> None:
        self.car = Car(7, 1)

    def update(self) -> None:
        if self.state != GameState.RACING or self.circuit is None:
            return
        self.car.update_position()
