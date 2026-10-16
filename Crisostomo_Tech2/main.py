import os


# ==========================================
# Task 2: Implement the Rule-Based Agent
# ==========================================
class ReflexVacuumAgent:
    def __init__(self, initial_location='A'):
        self.location = initial_location


    def move(self):
        """Switches the agent's location between room A and room B."""
        self.location = 'B' if self.location == 'A' else 'A'
        return f"Moving to room {self.location}"


    def perceive_and_act(self, environment):
        """Perceives the current room's state and applies rule-based actions."""
        current_state = environment[self.location]


        # Rule 1: If the current room is dirty, clean it.
        if current_state == 'Dirty':
            environment[self.location] = 'Clean'
            action_taken = f"Room {self.location} has been cleaned."
       
        # Rule 2: If the current room is clean, move to the other room.
        else:
            action_taken = self.move()


        return action_taken




# ==========================================
# Task 1: Environment Setup & User Inputs
# ==========================================
state_a = input("Is room A Dirty or Clean? ").strip().capitalize()
state_b = input("Is room B Dirty or Clean? ").strip().capitalize()


environment = {
    'A': state_a,
    'B': state_b
}


# ==========================================
# Task 3: Run the Simulation
# ==========================================
print()
steps = int(input("How many steps should the agent run? "))
print()


# Instantiate the agent starting at Room A
agent = ReflexVacuumAgent(initial_location='A')


for step in range(1, steps + 1):
    # Print agent's location at the start of the step
    print(f"Step {step}: Agent is in room {agent.location}")


    # Agent perceives and chooses action based on Rule 1 or Rule 2
    action = agent.perceive_and_act(environment)
    print(action)


    # Print the current state of the environment
    print(f"Environment state: {environment}")
    print()


os.system("pause")
