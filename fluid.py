import pygame
import numpy as np

# Import our FluidEngine class from engine.py
# This is how we "connect" the two files — Python just looks for engine.py
# in the same folder and loads the class from it
from engine import FluidEngine

# --- SETUP ---
pygame.init()

SCREEN_W = 1280
SCREEN_H = 720
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Flow Simulation")
clock = pygame.time.Clock()

# Our grid resolution — 128 columns, 72 rows
# This does NOT have to match screen size. Each grid cell will be scaled up.
GRID_W = 128
GRID_H = 72

# How many pixels does one grid cell take up on screen?
# 1280 / 128 = 10 pixels wide, 720 / 72 = 10 pixels tall
CELL_SIZE = SCREEN_W // GRID_W  # = 10

# Create the fluid engine — this initialises all 6 arrays to zero (calls the __init__ method)
engine = FluidEngine(GRID_W, GRID_H)

# Add some starting density in the middle so we can actually see something
# Without this, everything is 0 and the screen would just be black
engine.add_density(GRID_W // 2, GRID_H // 2, 1.0)  # centre cell, full density


# --- MAIN LOOP ---
running = True
while running:

    # Step 1: Handle events (quit, keyboard, mouse etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Step 2: Advance the simulation by one frame
    engine.step() # copying 1 to 0

    # Step 3: Clear screen to black before drawing the new frame
    screen.fill((0, 0, 0))

    # Step 4: Draw the density grid
    # We loop over every grid cell and draw a coloured rectangle for it
    # density1[x, y] is a float between 0.0 (empty) and 1.0 (full)
    # We multiply by 255 to convert that into a blue channel value (0–255)
    for x in range(GRID_W):
        for y in range(GRID_H):
            density_value = engine.density1[x, y]

            # Only draw cells that actually have some fluid — skip empty ones
            if density_value > 0:
                # Scale density (0.0–1.0) to blue channel brightness (0–255)
                blue = int(density_value * 255)

                # Draw a rectangle for this grid cell
                # pygame.draw.rect(surface, colour, (left, top, width, height))
                # x * CELL_SIZE converts grid column index → pixel x position
                # y * CELL_SIZE converts grid row index    → pixel y position
                pygame.draw.rect(
                    screen,
                    (0, 0, blue),           # RGB: no red, no green, blue only
                    (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                )

    # Step 5: Push what we drew to the actual screen
    pygame.display.flip()

    # Cap the loop at 60 frames per second
    clock.tick(60)

pygame.quit()