from matplotlib import pyplot as plt
from matplotlib import animation
from numpy import random
import numpy as np
import math
from numpy.core.numerictypes import ScalarType
import pandas as pd

# Creating dot class
class dot(object):

    activity_count = [0, 0, 0 ,0 ,0 ,0 ,0 ,0 ,0 ,0]

    def __init__(self, event):
        
        pos_init = self.get_pos(event[0]-1)
        self.current_event = event[0]
        self.activity_count[event[0]-1] += 1

        # Keep person information in dot
        self.event = event

        # Time state for idicate should we check the position change
        self.current_time_state = 0
        
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
    
    def get_pos(self, i):

        intial_pos = [(4.1, 8.6), (6.2, 8.6), (8.1,7.1), (8.8,5.1), (8.1, 3.2), 
                      (6.2, 1.2), (4.2,1.2), (2.2,3.2), (1.4,5.1), (2.1, 7.1)]

        x_adjust = round(random.uniform(-0.2, 0.2),2)
        y_adjust = round(random.uniform(-0.2, 0.2),2)

        x_pos = intial_pos[i][0] + x_adjust
        y_pos = intial_pos[i][1] + y_adjust

        return((x_pos, y_pos))

    def move(self, time_state):
        
        # check time state change
        if self.current_time_state != time_state:
            self.current_time_state = time_state
            
            # check event state change
            if self.current_event != self.event[time_state]:  
                self.activity_count[self.current_event - 1] -= 1
                self.activity_count[self.event[time_state] - 1] += 1
                
                self.current_event = self.event[time_state]

                self.targetx = self.get_pos(self.event[time_state]-1)[0] 
                self.targety = self.get_pos(self.event[time_state]-1)[1] 

                self.distx = self.get_pos(self.event[time_state]-1)[0] - self.x
                self.disty = self.get_pos(self.event[time_state]-1)[1] - self.y
                self.walk_count = 15

        # The real move of dot. (10 step from start to end)
        if(self.walk_count > 0):
            self.x += (self.distx/15)
            self.y += (self.disty/15)
            self.walk_count -= 1

def get_percentage(activity_count):
    percentage = (activity_count/total_member) * 100
    return str(round(percentage,1)) + '%'
            
def timer_string(i):
    # i is representative of time in minute(s)
    hrs = i//60
    mins = i - (hrs*60)

    hrs_str = str(hrs) if hrs >= 10 else '0'+str(hrs)
    mins_str = str(mins) if mins >= 10 else '0'+str(mins)

    return(f'{hrs_str}:{mins_str}')

# number of person in each event
number_events = [0, 0, 0, 0, 0, 0, 0 ,0 ,0 ,0]

# -----------------------------------------------------------------------------
#                                Main
# -----------------------------------------------------------------------------

df = pd.read_csv('data.csv')
total_member = len(df)

# Select the specific information to add to the dot
data = []
for idx in range(0,len(df)):
    data.append(list(df.iloc[idx][2:]))

# Initializing dots 
dots = [dot(person) for person in data]

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
fig.canvas.set_window_title('A Day in the Life CRM Students')

axtext = fig.add_axes([0.0,0.95,0.1,0.05])
axtext.axis("off")

# Adjust space and hide axis label
ax = plt.axes(xlim=(0, 10), ylim=(0, 10))
ax.axes.xaxis.set_visible(False)
ax.axes.yaxis.set_visible(False)
ax.set_facecolor((1,1,1))
plt.subplots_adjust(left=0.0, bottom=0.0, right=1, top=1)

# Initial timer
timer = ax.text(4.4,5, '00:00', fontname='sans-serif', fontsize=50, color='lightgrey')

# Initial main label
ax.text(3.8, 9.5, 'Sleeping', fontname='sans-serif', fontsize=20, 
        fontstyle='italic', color='black', fontweight='light')

sleeping_percentage = ax.text(4.02, 9.1, '0.1%', fontname='sans-serif',
                              fontsize=12,fontstyle='italic', color='dimgrey')
  
ax.text(5.8, 9.5, 'DailyRoutine', fontname='sans-serif', fontsize=20, 
        fontstyle='italic', color='black', fontweight='light')

daily_percentage = ax.text(6.15, 9.1, '0.0%', fontname='sans-serif',
                           fontsize=12,fontstyle='italic', color='dimgrey')

ax.text(7.8, 8, 'Traveling', fontname='sans-serif', fontsize=20, 
        fontstyle='italic', color='black', fontweight='light')

travel_percentage = ax.text(8.05, 7.6, '0.0%', fontname='sans-serif',
                            fontsize=12,fontstyle='italic', color='dimgrey')

ax.text(9.2, 5, 'Eating', fontname='sans-serif', fontsize=20, 
        fontstyle='italic', color='black', fontweight='light')

eating_percentage = ax.text(9.35, 4.6, '0.0%', fontname='sans-serif',
                       fontsize=12,fontstyle='italic', color='dimgrey')

ax.text(7.8, 2.5, 'CoffeeTime', fontname='sans-serif', fontsize=20, 
        fontstyle='italic', color='black', fontweight='light')

coffee_percentage = ax.text(8.15, 2.1, '0.0%', fontname='sans-serif',
                       fontsize=12,fontstyle='italic', color='dimgrey')

ax.text(5.8, 0.5, 'Working', fontname='sans-serif', fontsize=20, 
        fontstyle='italic', color='black', fontweight='light')

office_percentage = ax.text(6.05, 0.1, '0.0%', fontname='sans-serif',
                       fontsize=12,fontstyle='italic', color='dimgrey')

ax.text(3.8, 0.5, 'Meeting', fontname='sans-serif', fontsize=20, 
        fontstyle='italic', color='black', fontweight='light')

meeting_percentage = ax.text(4.0, 0.1,'0.0%', fontname='sans-serif',
                       fontsize=12,fontstyle='italic', color='dimgrey')

ax.text(1.8, 2.5, 'Relaxing', fontname='sans-serif', fontsize=20, 
        fontstyle='italic', color='black', fontweight='light')

relaxing_percentage = ax.text(2, 2.1, '0.0%', fontname='sans-serif',
                       fontsize=12,fontstyle='italic', color='dimgrey')

ax.text(0.4, 5, 'Learning', fontname='sans-serif', fontsize=20, 
        fontstyle='italic', color='black', fontweight='light')

learning_percentage = ax.text(0.6, 4.6, '0.0%', fontname='sans-serif',
                       fontsize=12,fontstyle='italic', color='dimgrey')

ax.text(1.8, 8, 'Exercise', fontname='sans-serif', fontsize=20, 
        fontstyle='italic', color='black', fontweight='light')

exercise_percentage = ax.text(2, 7.6, '0.0%', fontname='sans-serif',
                       fontsize=12,fontstyle='italic', color='dimgrey')

d, = ax.plot([dot.x for dot in dots],
             [dot.y for dot in dots], 'o', color='forestgreen')

def animate(i):
    # print(i)
    for dot in dots:

        dot.move(i//30)
        
        d.set_data([dot.x for dot in dots],
                   [dot.y for dot in dots])

        sleeping_percentage.set_text(get_percentage(dot.activity_count[0]))
        daily_percentage.set_text(get_percentage(dot.activity_count[1]))
        travel_percentage.set_text(get_percentage(dot.activity_count[2]))
        eating_percentage.set_text(get_percentage(dot.activity_count[3]))
        coffee_percentage.set_text(get_percentage(dot.activity_count[4]))
        office_percentage.set_text(get_percentage(dot.activity_count[5]))
        meeting_percentage.set_text(get_percentage(dot.activity_count[6]))
        relaxing_percentage.set_text(get_percentage(dot.activity_count[7]))
        learning_percentage.set_text(get_percentage(dot.activity_count[8]))
        exercise_percentage.set_text(get_percentage(dot.activity_count[9]))
        
        timer.set_text(timer_string(i * 1))
    return d,

anim = animation.FuncAnimation(fig, animate, frames=1440, interval=25)

plt.show()