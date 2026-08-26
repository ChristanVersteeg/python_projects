import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from random import uniform
from copy import deepcopy
from scipy import constants

# ediss wurde willkürlich gewählt, t0 entsprechend angepasst (physikalisch nicht unbedingt sinnvoll)
ediss = 500*constants.proton_mass
alpha = 1
deq = 1
t0 = 0.001
damping = 0.3

class particle:
    def __init__(self, index):
        self.index = index
        self.pos = [uniform(-0.5,0.5), uniform(-0.5,0.5)]
        self.prev = []
        self.mass = constants.proton_mass * 10
        self.velocity = [uniform(-1, 1), uniform(-1, 1)]
        self.v_prev = [0,0]
        self.acceleration = [0,0]
        self.F = [0,0]
        self.limits = [[10, -10] , [10, -10]]
    
    def calc_forces(self, particles):
        for i,p in enumerate(particles):
           if id(self) != id(p):
               r = [p.pos[0] - self.pos[0], p.pos[1] - self.pos[1]]
               d = np.sqrt(r[0]**2+r[1]**2)
               Force = r/(d*(1/(2*ediss*alpha*np.e**(-alpha*(d - deq))*(1 - np.e**(-alpha*(d - deq))))))
               self.F += Force
        self.acceleration = self.F / self.mass
    
    def sum_energy(self):
           return(0.5* self.mass * np.sqrt(self.velocity[0]**2+self.velocity[1]**2)) 
           
    def adj_vel(self, friction):
        self.velocity[0] *= friction
        self.velocity[1] *= friction
    
    def propagate(self, dt):
        
        self.velocity[0] += self.acceleration[0] * dt
        self.velocity[1] += self.acceleration[1] * dt
        
        self.prev.append(deepcopy(self.pos))
        
        def limit_position(pos_index, v_index, limit_1, limit_2):
            self.pos[pos_index] = self.limits[limit_1][limit_2] - (self.velocity[v_index]*dt-(self.limits[limit_1][limit_2]-self.pos[pos_index]))
            self.velocity[v_index] *= -1
        
        if ((self.velocity[0]*dt + self.pos[0]) > self.limits[0][0]):
            limit_position(0, 0, 0, 0)
        elif ((self.velocity[0]*dt + self.pos[0]) < self.limits[0][1]):
            limit_position(0, 0, 0, 1)
        else:
            self.pos[0] += self.velocity[0]*dt
        if ((self.velocity[1]*dt + self.pos[1]) > self.limits[1][0]):
            limit_position(1, 1, 1, 0)
        elif ((self.velocity[1]*dt + self.pos[1]) < self.limits[1][1]):
            limit_position(1, 1, 1, 1)
        else:
            self.pos[1] += self.velocity[1]*dt
        self.F = [0,0]
        self.v_prev = self.velocity
    
particles = []
for i in range(2):
    particles.append(particle(i))
for j in particles:   
    for i in range(3):
        j.propagate(1)       

fig, axes = plt.subplots(1,1, figsize =(10,5))

axes.set_xlim(-10, 10)
axes.set_ylim(-10, 10)

lines = []

for i in range(len(particles)):
    lines.append(axes.plot(particles[i].prev[0][0], particles[i].prev[0][1], 'o')[0])

def update(i):
    e_kin_tot = 0
    for j in range(len(particles)):
        particles[j].calc_forces(particles)
    for j in range(len(particles)):    
        particles[j].propagate(0.02)
        
        lines[j].set_xdata([particles[j].pos[0]])
        lines[j].set_ydata([particles[j].pos[1]])        
    for j in particles:
        e_kin_tot =+ j.sum_energy()
    
    friction = 1.0 - damping*np.clip((((e_kin_tot)/(len(particles)*constants.Boltzmann)-t0)/(t0)), -1, 1)**3
    for j in particles:
        j.adj_vel(friction)
        
    return lines

ani1 = animation.FuncAnimation(fig     = fig,
                              func     = update,
                              frames   = 180,
                              interval = 60,
                              repeat = True,
                              blit=True)

plt.show()
