import random
import agentpy as ap
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np


# -------- Get user input from console --------
num_agents = int(input("Enter number of agents: "))
grid_size = int(input("Enter grid size (e.g., 10 for 10x10): "))
num_steps = int(input("Enter number of steps: "))


DIRECTIONS = {
    "RIGHT": (1, 0),
    "UP": (0, 1),
    "DOWN": (0, -1),
    "LEFT": (-1, 0),
    "STAY": (0, 0),
}


# -------- Agent Definition -----------
class SmartWalker(ap.Agent):
    def setup(self):
        self.history = []
        self.move_options = ["RIGHT", "UP", "DOWN", "LEFT", "STAY"]
        self.move_weights = [0.60, 0.15, 0.15, 0.05, 0.05]


    def choose_move(self, reserved_positions):
        x, y = self.position
        candidates = random.choices(
            self.move_options,
            weights=self.move_weights,
            k=len(self.move_options) * 2
        )
        unique_candidates = list(dict.fromkeys(candidates))


        for move in unique_candidates:
            dx, dy = DIRECTIONS[move]
            nx, ny = x + dx, y + dy


            within_bounds = (0 <= nx < self.model.p.grid_size[0]) and (0 <= ny < self.model.p.grid_size[1])
            is_free = (nx, ny) not in reserved_positions or (nx == x and ny == y)


            if within_bounds and is_free:
                return (nx, ny)


        return self.position


# -------- Model Definition -----------
class AvoidanceWalkModel(ap.Model):
    def setup(self):
        max_agents = min(self.p.agents, self.p.grid_size[0] * self.p.grid_size[1])
        self.agents = ap.AgentList(self, max_agents, SmartWalker)


        all_cells = [(x, y) for x in range(self.p.grid_size[0]) for y in range(self.p.grid_size[1])]
        starting_spots = random.sample(all_cells, max_agents)


        for i, agent in enumerate(self.agents):
            agent.position = starting_spots[i]
            agent.history.append(agent.position)


    def step(self):
        reserved = set()
        for agent in self.agents:
            next_pos = agent.choose_move(reserved)
            reserved.add(next_pos)
            agent.position = next_pos
            agent.history.append(agent.position)


# -------- Setup Model -----------
parameters = {
    'agents': num_agents,
    'grid_size': (grid_size, grid_size),
    'steps': num_steps
}


model = AvoidanceWalkModel(parameters)
model.setup()


# -------- Interactive Animation -----------
fig_anim, ax_anim = plt.subplots(figsize=(6, 6))
ax_anim.set_xlim(-0.5, model.p.grid_size[0] - 0.5)
ax_anim.set_ylim(-0.5, model.p.grid_size[1] - 0.5)
ax_anim.set_xticks(range(model.p.grid_size[0]))
ax_anim.set_yticks(range(model.p.grid_size[1]))
ax_anim.grid(True, linestyle="--", alpha=0.5)


cmap = plt.colormaps.get_cmap('tab10' if len(model.agents) <= 10 else 'viridis').resampled(len(model.agents))
colors = [cmap(i) for i in range(len(model.agents))]


lines = [ax_anim.plot([], [], color=colors[i], alpha=0.5, linewidth=1.5)[0] for i in range(len(model.agents))]
init_x = [agent.position[0] for agent in model.agents]
init_y = [agent.position[1] for agent in model.agents]
scat = ax_anim.scatter(init_x, init_y, s=120, c=colors, edgecolors='black', zorder=3)


def update(frame):
    model.step()
    for i, agent in enumerate(model.agents):
        hx = [p[0] for p in agent.history]
        hy = [p[1] for p in agent.history]
        lines[i].set_data(hx, hy)
    coords = [agent.position for agent in model.agents]
    scat.set_offsets(coords)
    ax_anim.set_title(f"Simulation — Step {frame + 1} / {model.p.steps}")
    return lines + [scat]


ani = animation.FuncAnimation(
    fig_anim, update, frames=model.p.steps, interval=150, blit=False, repeat=False
)
plt.show()  # Close this window when finished to trigger the analysis phase


# ==============================================================
# -------- POST-SIMULATION: RECORD & ANALYZE POSITIONS ---------
# ==============================================================


# 1. Extract Initial vs. Final Positions
initial_positions = np.array([agent.history[0] for agent in model.agents])
final_positions = np.array([agent.history[-1] for agent in model.agents])


final_x = final_positions[:, 0]
final_y = final_positions[:, 1]


# 2. Statistical Computations
mean_x, mean_y = np.mean(final_x), np.mean(final_y)
std_x, std_y = np.std(final_x), np.std(final_y)


# Net Euclidean displacement per agent
displacements = np.linalg.norm(final_positions - initial_positions, axis=1)
mean_disp = np.mean(displacements)


print("\n" + "=" * 45)
print("       FINAL DISTRIBUTION ANALYSIS")
print("=" * 45)
print(f"Total Agents Simulated  : {len(model.agents)}")
print(f"Grid Dimensions         : {grid_size} x {grid_size}")
print(f"Total Steps Executed    : {num_steps}")
print("-" * 45)
print(f"Center of Mass (Mean)   : X = {mean_x:.2f}, Y = {mean_y:.2f}")
print(f"Spatial Spread (Std Dev): X = {std_x:.2f}, Y = {std_y:.2f}")
print(f"Mean Net Displacement   : {mean_disp:.2f} grid units")
print(f"Agents at Right Wall (X={grid_size-1}): {np.sum(final_x == grid_size - 1)} / {len(model.agents)}")
print("=" * 45 + "\n")


# 3. Distribution Visualizations
fig_analysis, axes = plt.subplots(1, 3, figsize=(16, 5))


# (A) Final 2D Density Heatmap
density_grid = np.zeros((grid_size, grid_size), dtype=int)
for x, y in final_positions:
    density_grid[y, x] += 1  # Rows: Y, Cols: X


im = axes[0].imshow(density_grid, origin='lower', cmap='YlOrRd', extent=[-0.5, grid_size - 0.5, -0.5, grid_size - 0.5])
axes[0].scatter(final_x, final_y, color='blue', s=40, alpha=0.6, label='Agents')
axes[0].scatter([mean_x], [mean_y], color='lime', marker='X', s=180, edgecolors='black', label='Center of Mass')
axes[0].set_title("2D Final Density Map")
axes[0].set_xlabel("X (East)")
axes[0].set_ylabel("Y (North)")
axes[0].legend(loc="upper left")
plt.colorbar(im, ax=axes[0], label="Agent Count per Cell")


# (B) Marginal X Distribution (Direction of Bias)
axes[1].hist(final_x, bins=np.arange(-0.5, grid_size + 0.5, 1), color='skyblue', edgecolor='black')
axes[1].axvline(mean_x, color='red', linestyle='--', linewidth=2, label=f'Mean X ({mean_x:.1f})')
axes[1].set_title("X-Axis Distribution (East Drift)")
axes[1].set_xlabel("X Coordinate")
axes[1].set_ylabel("Number of Agents")
axes[1].legend()


# (C) Net Displacement Distribution
axes[2].hist(displacements, bins=12, color='salmon', edgecolor='black')
axes[2].axvline(mean_disp, color='black', linestyle='--', linewidth=2, label=f'Mean ({mean_disp:.1f})')
axes[2].set_title("Net Displacement Magnitude")
axes[2].set_xlabel("Euclidean Distance from Start")
axes[2].set_ylabel("Frequency")
axes[2].legend()


plt.tight_layout()
plt.show()