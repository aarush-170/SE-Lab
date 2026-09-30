"""
GameEngine: owns the paddle, ball, and bricks.

Task 1:
- Bricks are removed when their hits_remaining reaches 0.

Task 2:
- Player starts with 3 lives.
- Losing the ball costs one life.
- Ball resets after losing a life.
- Game over occurs when all lives are lost.
- Press R to restart after game over.

Task 3:
- Normal bricks require 1 hit.
- Strong bricks require multiple hits.
- Unbreakable bricks can never be destroyed.
"""

import pygame

from game.paddle import Paddle
from game.ball import Ball
from game.brick import Brick
from game.collision import handle_ball_brick_collision
from game.renderer import WIDTH, HEIGHT

BRICK_ROWS = 4
BRICK_COLS = 8
BRICK_WIDTH = 68
BRICK_HEIGHT = 22
BRICK_GAP = 6
BRICK_TOP_MARGIN = 50

STARTING_LIVES = 3


class GameEngine:
    def __init__(self):
        self.paddle = Paddle(x=WIDTH / 2, y=HEIGHT - 30)
        self.ball = Ball(x=WIDTH / 2, y=HEIGHT - 50)

        self.lives = STARTING_LIVES
        self.game_over = False

        self.bricks = self._build_bricks()

    def _build_bricks(self):
        bricks = []

        total_width = BRICK_COLS * (BRICK_WIDTH + BRICK_GAP) - BRICK_GAP
        start_x = (WIDTH - total_width) / 2

        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                x = start_x + col * (BRICK_WIDTH + BRICK_GAP)
                y = BRICK_TOP_MARGIN + row * (BRICK_HEIGHT + BRICK_GAP)

                if row == 0:
                    brick_type = Brick.UNBREAKABLE
                elif row == 1:
                    brick_type = Brick.STRONG
                else:
                    brick_type = Brick.NORMAL

                bricks.append(
                    Brick(
                        x,
                        y,
                        BRICK_WIDTH,
                        BRICK_HEIGHT,
                        brick_type=brick_type,
                    )
                )

        return bricks

    def _reset_ball(self):
        self.ball = Ball(x=WIDTH / 2, y=HEIGHT - 50)

    def _restart_game(self):
        self.paddle = Paddle(x=WIDTH / 2, y=HEIGHT - 30)
        self.ball = Ball(x=WIDTH / 2, y=HEIGHT - 50)

        self.lives = STARTING_LIVES
        self.game_over = False

        self.bricks = self._build_bricks()

    def handle_input(self, keys_pressed):
        # Don't allow paddle movement after game over.
        if self.game_over:
            return

        dx = 0

        if keys_pressed[pygame.K_LEFT]:
            dx -= self.paddle.speed

        if keys_pressed[pygame.K_RIGHT]:
            dx += self.paddle.speed

        self.paddle.move(dx, WIDTH)

    def handle_keydown(self, key):
        # Restart the game when R is pressed after game over.
        if self.game_over and key == pygame.K_r:
            self._restart_game()

    def update(self):
        # Don't update the game after game over.
        if self.game_over:
            return

        self.ball.update()
        self.ball.bounce_off_walls(WIDTH)

        # Ball-paddle collision
        if (
            self.ball.get_rect().colliderect(self.paddle.get_rect())
            and self.ball.vy > 0
        ):
            self.ball.bounce_off_paddle(self.paddle.get_rect())

        # Ball-brick collision
        for brick in self.bricks:
            if handle_ball_brick_collision(self.ball, brick):

                # Unbreakable bricks are never destroyed.
                if brick.brick_type == Brick.UNBREAKABLE:
                    break

                # Normal and strong bricks lose one hit.
                brick.hits_remaining -= 1

                # Remove the brick when all required hits are used.
                if brick.hits_remaining <= 0:
                    self.bricks.remove(brick)

                break

        # Ball falls below the screen.
        if self.ball.is_below(HEIGHT):
            self.lives -= 1

            if self.lives > 0:
                # Player gets another attempt.
                self._reset_ball()
            else:
                # All lives have been used.
                self.game_over = True

    def draw(self, surface, font):
        from game import renderer

        renderer.draw_scene(
            surface,
            self.paddle,
            self.ball,
            self.bricks
        )

        # Display bricks remaining.
        renderer.draw_text(
            surface,
            font,
            f"Bricks left: {len(self.bricks)}",
            (10, 10)
        )

        # Display remaining lives.
        renderer.draw_text(
            surface,
            font,
            f"Lives: {self.lives}",
            (10, 35)
        )

        # Display game-over message.
        if self.game_over:
            renderer.draw_banner(
                surface,
                font,
                "GAME OVER - Press R to Restart"
            )