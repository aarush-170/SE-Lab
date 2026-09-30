"""
Brick: a single block in the Breakout game.

Brick types:
- Normal: destroyed after 1 hit
- Strong: requires multiple hits
- Unbreakable: never destroyed
"""

import pygame


class Brick:
    NORMAL = "normal"
    STRONG = "strong"
    UNBREAKABLE = "unbreakable"

    def __init__(
        self,
        x,
        y,
        width,
        height,
        brick_type=NORMAL,
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.brick_type = brick_type

        if brick_type == self.NORMAL:
            self.hits_remaining = 1
            self.color = (200, 90, 90)

        elif brick_type == self.STRONG:
            self.hits_remaining = 3
            self.color = (230, 150, 60)

        elif brick_type == self.UNBREAKABLE:
            self.hits_remaining = None
            self.color = (120, 120, 120)

        else:
            raise ValueError(f"Unknown brick type: {brick_type}")

    def get_rect(self):
        return pygame.Rect(
            int(self.x),
            int(self.y),
            self.width,
            self.height,
        )