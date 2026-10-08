import numpy as np

class FluidEngine:
    def __init__(self, nx, ny):
        self.nx = nx  # number of grid columns (width)
        self.ny = ny  # number of grid rows (height)

        # --- CURRENT STATE arrays (what the fluid looks like RIGHT NOW) ---
        # density1 stores how much "fluid stuff" is at each grid cell
        # u1 stores horizontal velocity at each cell (positive = moving right)
        # v1 stores vertical velocity at each cell (positive = moving down)
        self.density1 = np.zeros((nx, ny), dtype=np.float32)
        self.u1       = np.zeros((nx, ny), dtype=np.float32)
        self.v1       = np.zeros((nx, ny), dtype=np.float32)

        # --- PREVIOUS STATE arrays (what the fluid looked like LAST FRAME) ---
        # We read from these to compute the next state, then swap at end of step
        # Renamed from u2/v2 -> u0/v0 so the naming is consistent: 0 = old, 1 = new
        self.density0 = np.zeros_like(self.density1)
        self.u0       = np.zeros_like(self.u1)
        self.v0       = np.zeros_like(self.v1)

    def add_density(self, x, y, amount): # function that adds density where we want 
        """
        Inject fluid density at grid cell (x, y).
        This simulates a source — like a smoke machine pumping out smoke.
        We clamp it to 1.0 so it never goes above full density.
        """
        self.density1[x, y] = min(self.density1[x, y] + amount, 1.0)

    def step(self):
        """
        Advance the simulation by one time step.
        Right now this is a stub — it just copies current into previous.
        Later this is where diffuse(), advect(), project() will go.
        """
        # Save current state as previous state for next frame
        # np.copyto copies values from density1 INTO density0 (no new array created)
        np.copyto(self.density0, self.density1)
        np.copyto(self.u0, self.u1)
        np.copyto(self.v0, self.v1)