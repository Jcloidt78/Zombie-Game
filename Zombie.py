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

    def bite(self, human):
        if human.state != "INFECTED":
            human.change_state("INFECTED")
            human.reduce_energy(10)
            self.increase_energy(10)

class Doctor(Human):
    def __init__(self, agent_id, energy_range):
        super().__init__(agent_id, energy_range)

    def cure(self, human):
        if human.state == "INFECTED":
            human.change_state("ALIVE")

# Create agents
humans = [Human(i, [0, 100]) for i in range(10)]
zombies = [Zombie(i, [0, 100]) for i in range(5)]
doctors = [Doctor(i, [0, 100]) for i in range(3)]

# Add neighbors randomly
for human in humans:
    human.add_neighbor(random.choice(humans + zombies + doctors))
for zombie in zombies:
    zombie.add_neighbor(random.choice(humans + zombies + doctors))
for doctor in doctors:
    doctor.add_neighbor(random.choice(humans + zombies + doctors))

# Simulate the game over time
time_series = []
alive_humans = []
infected_humans = []
dead_humans = []
alive_doctors = []
infected_doctors = []
dead_doctors = []
alive_zombies = []
dead_zombies = []

for t in range(100):
    # Update agent statuses
    time_series.append([agent.__dict__ for agent in humans + zombies + doctors])

    # Count populations
    alive_humans.append(len([human for human in humans if human.state == "ALIVE"]))
    infected_humans.append(len([human for human in humans if human.state == "INFECTED"]))
    dead_humans.append(len([human for human in humans if human.state == "DEAD"]))
    alive_doctors.append(len([doctor for doctor in doctors if doctor.state == "ALIVE"]))
    infected_doctors.append(len([doctor for doctor in doctors if doctor.state == "INFECTED"]))
    dead_doctors.append(len([doctor for doctor in doctors if doctor.state == "DEAD"]))
    alive_zombies.append(len([zombie for zombie in zombies if zombie.state == "ALIVE"]))
    dead_zombies.append(len([zombie for zombie in zombies if zombie.state == "DEAD"]))

    # Perform actions
    for human in humans:
        if random.random() < 0.5:
            human.reduce_energy(5)
    for zombie in zombies:
        if random.random() < 0.5:
            zombie.reduce_energy(5)
            if zombie.neighbors:
                zombie.bite(random.choice(zombie.neighbors))
    for doctor in doctors:
        if random.random() < 0.5:
            doctor.increase_energy(5)
            if doctor.neighbors:
                doctor.cure(random.choice(doctor.neighbors))

# Save agent statuses to file
df = pd.DataFrame(time_series)
df.to_csv("agent_statuses.csv", index=False)

# Plot population dynamics
plt.plot(alive_humans, label="Alive Humans")
plt.plot(infected_humans, label="Infected Humans")
plt.plot(dead_humans, label="Dead Humans")
plt.plot(alive_doctors, label="Alive Doctors")
plt.plot(infected_doctors, label="Infected Doctors")
plt.plot(dead_doctors, label="Dead Doctors")
plt.plot(alive_zombies, label="Alive Zombies")
plt.plot(dead_zombies, label="Dead Zombies")
plt.xlabel("Time")
plt.ylabel("Population")
plt.legend()
plt.savefig("population_dynamics.png")