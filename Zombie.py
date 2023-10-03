import random
import pandas as pd
import matplotlib.pyplot as plt

class Agent:
    def __init__(self, agent_id, energy_range):
        self.agent_id = agent_id
        self.energy = random.randint(energy_range[0], energy_range[1])
        self.state = "ALIVE"
        self.neighbors = []

    def reduce_energy(self, amount):
        self.energy -= amount
        if self.energy <= 0:
            self.state = "DEAD"

    def increase_energy(self, amount):
        self.energy += amount

    def change_state(self, new_state):
        self.state = new_state

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def remove_neighbor(self, neighbor):
        self.neighbors.remove(neighbor)

class Human(Agent):
    def __init__(self, agent_id, energy_range):
        super().__init__(agent_id, energy_range)

class Zombie(Agent):
    def __init__(self, agent_id, energy_range):
        super().__init__(agent_id, energy_range)

    def bite_human(self):
        if self.neighbors:
            human = random.choice(self.neighbors)
            human.reduce_energy(10)
            if human.state != "INFECTED":
                human.change_state("INFECTED")
                self.increase_energy(10)

class Doctor(Human):
    def __init__(self, agent_id, energy_range):
        super().__init__(agent_id, energy_range)

    def cure_infected_human(self):
        if self.neighbors:
            infected_human = random.choice(self.neighbors)
            if infected_human.state == "INFECTED":
                infected_human.change_state("ALIVE")

# Simulation parameters
num_agents = 100
energy_range = (0, 100)
num_iterations = 100

# Create agents
agents = []
for i in range(num_agents):
    if i % 3 == 0:
        agent = Zombie(i, energy_range)
    elif i % 3 == 1:
        agent = Doctor(i, energy_range)
    else:
        agent = Human(i, energy_range)
    agents.append(agent)

# Randomly assign neighbors
for agent in agents:
    num_neighbors = random.randint(0, num_agents)
    for _ in range(num_neighbors):
        neighbor = random.choice(agents)
        if neighbor != agent:
            agent.add_neighbor(neighbor)

# Simulation loop
statuses = []
alive_humans = []
infected_humans = []
dead_humans = []
alive_doctors = []
infected_doctors = []
dead_doctors = []
alive_zombies = []
dead_zombies = []

for _ in range(num_iterations):
    # Update agent statuses
    status = {}
    for agent in agents:
        status[agent.agent_id] = {
            "Energy": agent.energy,
            "State": agent.state,
            "Neighbors": [neighbor.agent_id for neighbor in agent.neighbors]
        }
    statuses.append(status)

    # Count populations
    alive_humans.append(len([agent for agent in agents if isinstance(agent, Human) and agent.state == "ALIVE"]))
    infected_humans.append(len([agent for agent in agents if isinstance(agent, Human) and agent.state == "INFECTED"]))
    dead_humans.append(len([agent for agent in agents if isinstance(agent, Human) and agent.state == "DEAD"]))
    alive_doctors.append(len([agent for agent in agents if isinstance(agent, Doctor) and agent.state == "ALIVE"]))
    infected_doctors.append(len([agent for agent in agents if isinstance(agent, Doctor) and agent.state == "INFECTED"]))
    dead_doctors.append(len([agent for agent in agents if isinstance(agent, Doctor) and agent.state == "DEAD"]))
    alive_zombies.append(len([agent for agent in agents if isinstance(agent, Zombie) and agent.state == "ALIVE"]))
    dead_zombies.append(len([agent for agent in agents if isinstance(agent, Zombie) and agent.state == "DEAD"]))

    # Simulate agent interactions
    for agent in agents:
        if isinstance(agent, Zombie):
            agent.bite_human()
        elif isinstance(agent, Doctor):
            agent.cure_infected_human()

# Output agent statuses to file
df_statuses = pd.DataFrame(statuses)
df_statuses.to_csv("agent_statuses.csv", index=False)

# Plot population dynamics
time_steps = range(num_iterations)
plt.plot(time_steps, alive_humans, label="Alive Humans")
plt.plot(time_steps, infected_humans, label="Infected Humans")
plt.plot(time_steps, dead_humans, label="Dead Humans")
plt.plot(time_steps, alive_doctors, label="Alive Doctors")
plt.plot(time_steps, infected_doctors, label="Infected Doctors")
plt.plot(time_steps, dead_doctors, label="Dead Doctors")
plt.plot(time_steps, alive_zombies, label="Alive Zombies")
plt.plot(time_steps, dead_zombies, label="Dead Zombies")
plt.xlabel("Time Steps")
plt.ylabel("Population")
plt.legend()
plt.savefig("population_dynamics.png")
plt.show()
