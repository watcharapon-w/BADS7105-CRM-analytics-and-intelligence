from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.animation import FuncAnimation
from numpy import random
import numpy as np
import math
import pandas as pd

# Creating dot class
class dot(object):

    NUMBER_OF_DOT = 0

    def __init__(self, event):
        
        pos_init = self.get_pos(event[0]-1)

        # Keep person information in dot
        self.event = event

        # Time state for idicate should we check the position change
        self.current_time_state = 0
        self.current_event = 0

        # Expected position
        self.target_pos = (0,0)

        # Current position of dot (x, y)
        self.x = pos_init[0] 
        self.y = pos_init[1] 

        # Distance between current to target
        self.distx = 0
        self.disty = 0

        # Walk count
        self.walk_count = 0

        # Target point
        self.targetx = 0
        self.targety = 0
       
        # Future position of dot (x, y)
        self.velx = 0
        self.vely = 0
    
    def current_pos(self):
        return (self.x, self.y)
    
    def get_pos(self, i):

        intial_pos = [(4, 9), (6.1, 9), (8,7.5), (9,5.1), (8, 3), (6.1, 1), 
                      (4,1), (2,3), (2, 7.5), (1,5.1)]

        x_adjust = round(random.uniform(-0.2, 0.2),2)
        y_adjust = round(random.uniform(-0.2, 0.2),2)

        x_pos = intial_pos[i][0] + x_adjust
        y_pos = intial_pos[i][1] + y_adjust

        return((x_pos, y_pos))

    def generate_new_vel(self):
        return 0 #(np.random.random_sample() - 0.5) / 5

    def move(self, time_state):
        
        # check time state change
        if self.current_time_state != time_state:
            self.current_time_state = time_state
            

            # check event state change
            if self.current_event != self.event[time_state]:
                # print('firstCheck')
                # print(self.current_event)
                # print(self.event[time_state])
                
                self.current_event = self.event[time_state]


                self.targetx = self.get_pos(self.event[time_state]-1)[0] 
                self.targety = self.get_pos(self.event[time_state]-1)[1] 

                self.distx = self.get_pos(self.event[time_state]-1)[0] - self.x
                self.disty = self.get_pos(self.event[time_state]-1)[1] - self.y
                self.walk_count = 10

        if(self.walk_count > 0):
            self.x += (self.distx/10)
            self.y += (self.disty/10)
            self.walk_count -= 1
            
def timer_string(i):
    # i is representative of time in minute(s)

    hrs = i//60
    mins = i - (hrs*60)

    hrs_str = str(hrs) if hrs >= 10 else '0'+str(hrs)
    mins_str = str(mins) if mins >= 10 else '0'+str(mins)

    return(f'{hrs_str}:{mins_str}')


# -----------------------------------------------------------------------------
#                                Main
# -----------------------------------------------------------------------------

df = pd.read_csv('data.csv')
data = []

for idx in range(0,len(df)):
    data.append(list(df.iloc[idx][2:]))

# Initializing dots 
dots = [dot(person) for person in data]

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()

axtext = fig.add_axes([0.0,0.95,0.1,0.05])
axtext.axis("off")
time = axtext.text(4.8, 0.5, str(0), ha="left", va="top", 
                   fontweight='bold', fontsize='x-large')

# Adjust space and hide axis label
ax = plt.axes(xlim=(0, 10), ylim=(0, 10))
ax.axes.xaxis.set_visible(False)
ax.axes.yaxis.set_visible(False)
plt.subplots_adjust(left=0.015, bottom=0.015, right=0.985, top=0.920)

# Setup main label
ax.text(3.8, 9.5, 'Sleeping')
ax.text(5.8, 9.5, 'DailyRoutine')
ax.text(7.8, 8, 'Travel')
ax.text(9.2, 5, 'Eating')
ax.text(7.8, 2.5, 'Coffee')
ax.text(5.8, 0.5, 'OfficeWork')
ax.text(3.8, 0.5, 'Meeting')
ax.text(1.8, 2.5, 'Entertainment')
ax.text(0.4, 5, 'Exercise')
ax.text(1.8, 8, 'Learning')






d, = ax.plot([dot.x for dot in dots],
             [dot.y for dot in dots], 'ro')

# animation function.  This is called sequentially
def animate(i):
    # print(i)
    for dot in dots:

        dot.move(i//30)
        
        d.set_data([dot.x for dot in dots],
                   [dot.y for dot in dots])

        time.set_text(timer_string(i * 1))
    return d,

# frames is number 
anim = animation.FuncAnimation(fig, animate, frames=1440, interval=100)

plt.show()