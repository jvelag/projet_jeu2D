import pygame
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, TILE_SIZE,
    COLOR_BG, COLOR_TEXT, COLOR_ACCENT, COLOR_PANEL, COLOR_PANEL_BORDER,
    GameState
)
from model.game_model import GameModel
from model.circuit import CIRCUIT_SPECS


class GameView:

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 24)

    def draw(self, model: GameModel) -> None:
        self.screen.fill(COLOR_BG)
        if model.state == GameState.MENU:
            self._draw_menu(model)
        elif model.state == GameState.CIRCUIT_SELECT:
            self._draw_circuit_select(model)
        elif model.state == GameState.RACING:
            self._draw_racing(model)
        pygame.display.flip()

    def _draw_circuit_select(self, model: GameModel) -> None:
        cx = WINDOW_WIDTH // 2

        title_surf = self.font.render(
            "Choisissez un circuit (Haut/Bas, Enter)", True, COLOR_ACCENT)
        self.screen.blit(title_surf, title_surf.get_rect(center=(cx, 160)))

        for i, spec in enumerate(CIRCUIT_SPECS):
            selected = i == model.selected_circuit
            rect = pygame.Rect(cx - 140, 295 + i * 80, 280, 50)
            pygame.draw.rect(self.screen, COLOR_PANEL, rect, border_radius=8)
            pygame.draw.rect(self.screen,
                             COLOR_ACCENT if selected else COLOR_PANEL_BORDER,
                             rect, 2, border_radius=8)
            swatch = pygame.Rect(rect.x + 10, rect.y + 10, 30, 30)
            pygame.draw.rect(self.screen, spec["color"], swatch,
                             border_radius=4)
            text_surf = self.font.render(
                spec["name"], True, COLOR_ACCENT if selected else COLOR_TEXT)
            self.screen.blit(text_surf, text_surf.get_rect(
                midleft=(swatch.right + 15, rect.centery)))

    def _draw_menu(self, model: GameModel) -> None:
        cx = WINDOW_WIDTH // 2

        title_surf = self.font.render(
            "Jeu de course 2D", True, COLOR_ACCENT)
        self.screen.blit(title_surf, title_surf.get_rect(center=(cx, 160)))

        options = [("JOUER (Enter)", GameState.RACING),
                   ("QUITTER (Escape)", None)]
        for i, (label, _) in enumerate(options):
            y = 320 + i * 80
            rect = pygame.Rect(cx - 140, y - 25, 280, 50)
            pygame.draw.rect(self.screen, COLOR_PANEL, rect, border_radius=8)
            pygame.draw.rect(self.screen, COLOR_PANEL_BORDER,
                             rect, 2, border_radius=8)
            text_surf = self.font.render(
                label, True, COLOR_ACCENT if i == 0 else COLOR_TEXT)
            self.screen.blit(text_surf, text_surf.get_rect(center=rect.center))

    def _draw_racing(self, model: GameModel) -> None:

        for row_idx, row in enumerate(model.circuit.grid):
            for col_idx, tile in enumerate(row):
                sprite = tile.get_sprite(TILE_SIZE)
                self.screen.blit(
                    sprite, (col_idx * TILE_SIZE, row_idx * TILE_SIZE))

        if model.circuit is None:
            return
        surf, rect = model.car.get_rotated_sprite()
        self.screen.blit(surf, rect)
