#from pandas import pd
import pandas as pd
# This code is from July 2020: Spyder version 4.1.3
# Was getting an error without this line (Dec 2020)
#pd.core.common.is_list_like = pd.api.types.is_list_like
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse

from pybaseball import statcast_pitcher
from pybaseball import playerid_lookup

playerid_lookup('flaherty', 'jack')
playerid_lookup('flaherty', 'jack').values
jack = statcast_pitcher('2019-03-20', '2019-09-20', player_id=656427)
# Some of these columns are no longer used or replaced
# Some are empty columns, using nan
jack.columns
# Reference for all stat acronyms: https://baseballsavant.mlb.com/csv-docs

# His 2019 first half stats
jack1 = statcast_pitcher('2019-03-20', '2019-07-20', player_id=656427)
# His 2019 2nd half stats
jack2 = statcast_pitcher('2019-07-20', '2019-09-20', player_id=656427)
# His 2018 stats, could be useful
jack2018 = statcast_pitcher('2018-03-29', '2019-09-28', player_id=656427)

"""function to see how often he threw each pitch type in percentages"""
def pitchPercentage(player):
    totalPitches = player['pitch_type'].value_counts()
    percent = (totalPitches / totalPitches.sum()) * 100
    return round(percent, 1)

pitchPer2018 = pitchPercentage(jack2018)
pitchPer1 = pitchPercentage(jack1)
pitchPer2 = pitchPercentage(jack2)

# Fig 1
pd.concat([pitchPer2018, pitchPer1, pitchPer2],
          keys=['2018', '1st_Half', '2nd_Half'], axis=1)

# Round functions that work within groupby method
def round_0(x):
    return round(x.mean(), 1)
def round_3(x):
    return round(x.mean(), 3)

results1 = jack1.groupby('pitch_type').agg(
    MPH=('release_speed', round_0),
    xMPH=('effective_speed', round_0),
    xBA=('estimated_ba_using_speedangle', round_3),
    wOBA=('woba_value', round_3),
    xwOBA=('estimated_woba_using_speedangle', round_3),
    spin=('release_spin_rate', round_0))

results2 = jack2.groupby('pitch_type').agg(
    MPH=('release_speed', round_0),
    xMPH=('effective_speed', round_0),
    xBA=('estimated_ba_using_speedangle', round_3),
    wOBA=('woba_value', round_3),
    xwOBA=('estimated_woba_using_speedangle', round_3),
    spin=('release_spin_rate', round_0))

# Fig 2
results2 - results1
# Note: not on written report. Table of results.
pd.concat([results1, results2], keys=['1st_Half', '2nd_Half'])

jack1woba = jack1.groupby('pitch_type').mean()['woba_value'].round(3)
jack2woba = jack2.groupby('pitch_type').mean()['woba_value'].round(3)
jack1xwoba = jack1.groupby('pitch_type').mean()['estimated_woba_using_speedangle'].round(3)
jack2xwoba = jack2.groupby('pitch_type').mean()['estimated_woba_using_speedangle'].round(3)

pitches = ['CH', 'FF', 'FT', 'KC', 'SL']
resultsInd = range(len(pitches))

# width of bars (width), make the bars thinner so they fit
resultsWidth = np.min(np.diff(resultsInd)) / 4.

# https://matplotlib.org/gallery/api/barchart.html
def autolabel(rects, xpos='center'):
    """
    Attach a text label above each bar in *rects*, displaying its height.

    *xpos* indicates which side to place the text w.r.t. the center of
    the bar. It can be one of the following {'center', 'right', 'left'}.
    """

    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0, 'right': 1, 'left': -1}

    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(offset[xpos] * 3, 3),  # use 3 points offset
                    textcoords="offset points",  # in both directions
                    ha=ha[xpos], va='bottom')

# Note: autolabel does not work with floats as inputs
# Fig 3: woba only
# run all lines together
fig, ax = plt.subplots()
ax.bar(resultsInd - resultsWidth / 2, jack1woba, width=resultsWidth,
       color='r', label='2019 1st Half')
ax.bar(resultsInd + resultsWidth / 2, jack2woba, width=resultsWidth,
       color='navy', label='2019 2nd Half')
ax.set_xticklabels(pitches)
ax.set_xticks(resultsInd)  # x-label will not label CH without this
ax.set_ylabel('wOBA')
ax.set_title("Jack Flaherty's wOBA by Pitch Type")
ax.legend()

# Fig 4: xwOBA only 
fig, ax = plt.subplots()
ax.bar(resultsInd - resultsWidth / 2, jack1xwoba, width=resultsWidth,
       color='r', label='2019 1st Half')
ax.bar(resultsInd + resultsWidth / 2, jack2xwoba, width=resultsWidth,
       color='navy', label='2019 2nd Half')
ax.set_xticklabels(pitches)
ax.set_xticks(resultsInd)  # x-label will not label CH without this
ax.set_ylabel('xwOBA')
ax.set_title("Jack Flaherty's xwOBA by Pitch Type")
ax.legend()

resultsWidth2 = np.min(np.diff(resultsInd)) / 5

# Note: not on written report. woba and xwoba of both halves
# run all lines together
fig, ax = plt.subplots()
ax.bar(resultsInd - (resultsWidth2 / 2) * 3, jack1woba, width=resultsWidth2,
       color='r', label='1st Half wOBA')
ax.bar(resultsInd - resultsWidth2 / 2, jack1xwoba, width=resultsWidth2,
       color='grey', label='1st Half xwOBA')
ax.bar(resultsInd + resultsWidth2 / 2, jack2woba, width=resultsWidth2,
       color='navy', label='2nd Half wOBA')
ax.bar(resultsInd + (resultsWidth2 / 2) * 3, jack2xwoba, width=resultsWidth2,
       color='black', label='2nd Half xwOBA')
ax.set_xticklabels(pitches)
ax.set_xticks(resultsInd)  # x-label will not label CH without this
ax.set_ylabel('wOBA/xwOBA')
ax.set_title("Jack Flaherty's wOBA/xwOBA by Pitch Type")
ax.legend()

# woba and xwoba in table form
pd.concat([jack1woba, jack2woba], keys=['1st_Half', '2nd_Half'])
pd.concat([jack1xwoba, jack2xwoba], keys=['1st_Half', '2nd_Half'])

# MPH changes
jack1mph = jack1.groupby('pitch_type').mean()['release_speed']
jack1mph = jack1mph.round(1)
jack2mph = jack2.groupby('pitch_type').mean()['release_speed']
jack2mph = jack2mph.round(1)
jack2018mph = jack2018.groupby('pitch_type').mean()['release_speed']
jack2018mph = jack2018mph.round(1)

ind = range(len(jack1mph))
width = np.min(np.diff(ind)) / 4.

# Fig 5
# run all these lines together to show the complete graph
fig, ax = plt.subplots()
mph2018 = ax.bar(ind - 2 * width / 2, jack2018mph, width, color='r', label='2018')
mph1st = ax.bar(ind, jack1mph, width, color='navy', label='2019 1st half')
mph2nd = ax.bar(ind + 2 * width / 2, jack2mph, width, color='grey', label="2019 2nd half")
ax.set_ylabel('MPH')
ax.set_ylim(0, 100)
ax.legend(loc='center')
ax.set_xticklabels(pitches)
ax.set_xticks(ind)
ax.set_title("Jack Flaherty's Velocity Changes")
autolabel(mph2018, 'left')
autolabel(mph1st, 'center')
autolabel(mph2nd, 'right')

# velocity change from first half to second
velChange = jack2mph - jack1mph
velChange.mean()  # overall, his velo is up 0.70 mph

jack2019mph = jack.groupby('pitch_type').mean()['release_speed']
(jack2019mph - jack2018mph).mean()  # about a 0.45 mph improvement overall
(jack1mph - jack2018mph).mean()  # 0.18 mph jump
(jack2mph - jack2018mph).mean()  # 0.89 mph jump

# looking at arm slot differences
# release_pos_x is horizontal release point from the catcher's perspective
# release_pos_z is vertical release point from the catcher's perspective
# release_pos_y is the release position from the catcher's perspective

slot2018 = jack2018.groupby('pitch_type').agg(
    xAxis=('release_pos_x', 'mean'),
    zAxis=('release_pos_z', 'mean'),
    releasePoint=('release_pos_y', 'mean'),
    releaseExt=('release_extension', 'mean'))

slot1 = jack1.groupby('pitch_type').agg(
    xAxis=('release_pos_x', 'mean'),
    zAxis=('release_pos_z', 'mean'),
    releasePoint=('release_pos_y', 'mean'),
    releaseExt=('release_extension', 'mean'))

slot2 = jack2.groupby('pitch_type').agg(
    xAxis=('release_pos_x', 'mean'),
    zAxis=('release_pos_z', 'mean'),
    releasePoint=('release_pos_y', 'mean'),
    releaseExt=('release_extension', 'mean'))

# Difficult to understand what the numbers mean
slot2 - slot1

""""Scatter plot of his arm slots. Looking at numbers is impossible to
understand what this all means, differences can be seen in a graph."""
# release point height on baseball-savant is called the z-axis
# distance from home plate is their y-axis, release_point_y
xAxis2018 = jack2018.groupby('pitch_type')['release_pos_x']
zAxis2018 = jack2018.groupby('pitch_type')['release_pos_z']
xAxis1st = jack1.groupby('pitch_type')['release_pos_x']
zAxis1st = jack1.groupby('pitch_type')['release_pos_z']
xAxis2nd = jack2.groupby('pitch_type')['release_pos_x']
zAxis2nd = jack2.groupby('pitch_type')['release_pos_z']

# Fig 6
# run all these lines to show complete graph
plt.scatter(xAxis2018.mean(), zAxis2018.mean(), label='2018', c='red')
plt.scatter(xAxis1st.mean(), zAxis1st.mean(), label='2019 1st half', c='blue')
plt.scatter(xAxis2nd.mean(), zAxis2nd.mean(), label='2019 2nd half', c='green')
plt.xlim(-3, 0)
plt.ylim(5, 6)
plt.xlabel('Feet away from his body')
plt.ylabel('Feet off the ground')
plt.legend()
plt.title("Release point of Flaherty's Pitches\n(From catcher's viewpoint)")

# making a scatter plot using ellipses
# 2019 second half info, we need the standard deviation to make ellipses

# works if we use only one pitch
second = Ellipse(xy=(xAxis2nd.mean()['FF'], zAxis2nd.mean()['FF']),
                 width=xAxis2nd.std()['FF'],
                 height=zAxis2nd.std()['FF'], angle=0)
fig, ax = plt.subplots()
ax.add_artist(second)
ax.set_xlim(-3, 0)
ax.set_ylim(5, 6)

def makeEllipses(list):
    for a in list:
        ax.add_artist(a)

# Note: not on report
# had to do each pitch individually
# run all lines together
ff1st = Ellipse(xy=(xAxis1st.mean()['FF'], zAxis1st.mean()['FF']),
                width=xAxis1st.std()['FF'], height=zAxis1st.std()['FF'],
                facecolor='r', edgecolor='black', label='ff1st')
ch1st = Ellipse(xy=(xAxis1st.mean()['CH'], zAxis1st.mean()['CH']),
                width=xAxis1st.std()['CH'], height=zAxis1st.std()['FF'],
                facecolor='blue', edgecolor='black', alpha=.7)
ft1st = Ellipse(xy=(xAxis1st.mean()['FT'], zAxis1st.mean()['FT']),
                width=xAxis1st.std()['FT'], height=zAxis1st.std()['FT'],
                facecolor='green', edgecolor='black', alpha=.7)
kc1st = Ellipse(xy=(xAxis1st.mean()['KC'], zAxis1st.mean()['KC']),
                width=xAxis1st.std()['KC'], height=zAxis1st.std()['KC'],
                facecolor='grey', edgecolor='black')
sl1st = Ellipse(xy=(xAxis1st.mean()['SL'], zAxis1st.mean()['SL']),
                width=xAxis1st.std()['SL'], height=zAxis1st.std()['SL'],
                facecolor='purple', edgecolor='black', alpha=.7)
ff2nd = Ellipse(xy=(xAxis2nd.mean()['FF'], zAxis2nd.mean()['FF']),
                width=xAxis2nd.std()['FF'], height=zAxis2nd.std()['FF'],
                color='r')
ch2nd = Ellipse(xy=(xAxis2nd.mean()['CH'], zAxis2nd.mean()['CH']),
                width=xAxis2nd.std()['CH'], height=zAxis2nd.std()['FF'],
                color='blue')
ft2nd = Ellipse(xy=(xAxis2nd.mean()['FT'], zAxis2nd.mean()['FT']),
                width=xAxis2nd.std()['FT'], height=zAxis2nd.std()['FT'],
                color='green', alpha=.9)
kc2nd = Ellipse(xy=(xAxis2nd.mean()['KC'], zAxis2nd.mean()['KC']),
                width=xAxis2nd.std()['KC'], height=zAxis2nd.std()['KC'],
                color='grey')
sl2nd = Ellipse(xy=(xAxis2nd.mean()['SL'], zAxis2nd.mean()['SL']),
                width=xAxis2nd.std()['SL'], height=zAxis2nd.std()['SL'],
                color='purple')
fig, ax = plt.subplots()
pitchList = [ff1st, ch1st, ft1st, kc1st, sl1st,
             ff2nd, ch2nd, ft2nd, kc2nd, sl2nd]
makeEllipses(pitchList), ax.set_xlim(-3, 0), ax.set_ylim(5, 6)
ax.legend(pitchList, ['ff1st', 'ch1st', 'ft1st', 'kc1st', 'sl1st',
                      'ff2nd', 'ch2nd', 'ft2nd', 'kc2nd', 'sl2nd'])
ax.set_xlabel("Feet away from body")
ax.set_ylabel("Inches from home plate")
ax.set_title("Release Point of Flaherty's Pitches\
             \n(From catcher's view)")

# distance from home plate is their y-axis, release_point_y
yAxis2018 = jack2018.groupby('pitch_type')['release_pos_y']
yAxis1st = jack1.groupby('pitch_type')['release_pos_y']
yAxis2nd = jack2.groupby('pitch_type')['release_pos_y']

# The y-axis on this graph is the z-axis on Baseball-Savant
# the z-axis on this graph is the y-axis on Baseball-Savant
# set y-axis from 0 to 7 (y-axis as in feet off the ground)
# run all lines together
# Fig 7
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(xAxis2018.mean(), yAxis2018.mean(), zAxis2018.mean(),
           label='2018', c='red')
ax.scatter(xAxis1st.mean(), yAxis1st.mean(), zAxis1st.mean(),
           label='2019 1st half', c='blue')
ax.scatter(xAxis2nd.mean(), yAxis2nd.mean(), zAxis2nd.mean(),
           label='2019 2nd half', c='green')
ax.legend()
ax.set_xlim(-3, 0)
ax.set_xlabel("Feet away from body")
ax.set_ylabel("Inches from home plate")
ax.set_zlim(0, 6)
ax.set_zlabel("Feet off the ground")
ax.set_title("Release Point of Flaherty's Pitches\
             \n(From catcher's view)")

# TODO: create counter or heat maps to show movement and pitch locations
# Looking at movement of his pitches
move1st = jack1.groupby('pitch_type').agg(
    xMove=('pfx_x', 'mean'),
    yMove=('pfx_z', 'mean'),
    xPlate=('plate_x', 'mean'),
    yPlate=('plate_z', 'mean'))

move2nd = jack2.groupby('pitch_type').agg(
    xMove=('pfx_x', 'mean'),
    yMove=('pfx_z', 'mean'),
    xPlate=('plate_x', 'mean'),
    yPlate=('plate_z', 'mean'))

# Using scatter plots to see movement on pitches
xMove2018 = jack2018.groupby('pitch_type')['pfx_x']
zMove2018 = jack2018.groupby('pitch_type')['pfx_z']
xMove1 = jack1.groupby('pitch_type')['pfx_x']
zMove1 = jack1.groupby('pitch_type')['pfx_z']
xMove2 = jack2.groupby('pitch_type')['pfx_x']
zMove2 = jack2.groupby('pitch_type')['pfx_z']

# Squezzed some things together to not have to run so many lines
fig, ax = plt.subplots()
ff2018 = ax.scatter(xMove2018.mean()['FF'], zMove2018.mean()['FF'], c='r')
ch2018 = ax.scatter(xMove2018.mean()['CH'], zMove2018.mean()['CH'], c='blue')
ft2018 = ax.scatter(xMove2018.mean()['FT'], zMove2018.mean()['FT'], c='green')
kc2018 = ax.scatter(xMove2018.mean()['KC'], zMove2018.mean()['KC'], c='grey')
sl2018 = ax.scatter(xMove2018.mean()['SL'], zMove2018.mean()['SL'], c='purple')
ff1 = ax.scatter(xMove1.mean()['FF'], zMove1.mean()['FF'],
                 fc='r', ec='black')
ch1 = ax.scatter(xMove1.mean()['CH'], zMove1.mean()['CH'],
                 facecolor='blue', edgecolor='black')
ft1 = ax.scatter(xMove1.mean()['FT'], zMove1.mean()['FT'],
                 facecolor='green', edgecolor='black')
kc1 = ax.scatter(xMove1.mean()['KC'], zMove1.mean()['KC'],
                 facecolor='grey', edgecolor='black')
sl1 = ax.scatter(xMove1.mean()['SL'], zMove1.mean()['SL'],
                 facecolor='purple', edgecolor='black')
ff2 = ax.scatter(xMove2.mean()['FF'], zMove2.mean()['FF'],
                 facecolor='white', edgecolor='r')
ch2 = ax.scatter(xMove2.mean()['CH'], zMove2.mean()['CH'],
                 facecolor='white', edgecolor='blue')
ft2 = ax.scatter(xMove2.mean()['FT'], zMove2.mean()['FT'],
                 facecolor='white', edgecolor='green')
kc2 = ax.scatter(xMove2.mean()['KC'], zMove2.mean()['KC'],
                 facecolor='white', edgecolor='grey')
sl2 = ax.scatter(xMove2.mean()['SL'], zMove2.mean()['SL'],
                 facecolor='white', edgecolor='purple')
pitchList = [ff2018, ch2018, ft2018, kc2018, sl2018,
             ff1, ch1, ft1, kc1, sl1, ff2, ch2, ft2, kc2, sl2]
makeEllipses(pitchList), ax.set_xlim(-1.5, 1.5), ax.set_ylim(-1.5, 1.5)
l1 = ax.legend([ff2018, ch2018, ft2018, kc2018, sl2018],
               ['FF2018', 'CH2018', 'KC2018', 'SL2018'], loc=1)
l2 = ax.legend([ff1, ch1, ft1, kc1, sl1],
               ['FF1st', 'CH1st', 'FT1st', 'KC1st', 'Sl1st'], loc=3)
l3 = ax.legend([ff2, ch2, ft2, kc2, sl2],
               ['FF2nd', 'CH2nd', 'FT2nd', 'KC2nd', 'Sl2nd'], loc=8)
ax.add_artist(l1), ax.add_artist(l2)
ax.set_ylabel("Inches"), ax.set_xlabel("Inches")
ax.set_title("Flaherty's Movement by Pitch Type")

# 2019 halves in ellipses
fig, ax = plt.subplots()
ff1 = Ellipse(xy=(xMove1.mean()['FF'], zMove1.mean()['FF']),
              width=xMove1.std()['FF'], height=zMove1.std()['FF'],
              facecolor='r', edgecolor='black')
ch1 = Ellipse(xy=(xMove1.mean()['CH'], zMove1.mean()['CH']),
              width=xMove1.std()['CH'], height=zMove1.std()['FF'],
              facecolor='blue', edgecolor='black')
ft1 = Ellipse(xy=(xMove1.mean()['FT'], zMove1.mean()['FT']),
              width=xMove1.std()['FT'], height=zMove1.std()['FT'],
              facecolor='green', edgecolor='black')
kc1 = Ellipse(xy=(xMove1.mean()['KC'], zMove1.mean()['KC']),
              width=xMove1.std()['KC'], height=zMove1.std()['KC'],
              facecolor='grey', edgecolor='black')
sl1 = Ellipse(xy=(xMove1.mean()['SL'], zMove1.mean()['SL']),
              width=xMove1.std()['SL'], height=zMove1.std()['SL'],
              facecolor='purple', edgecolor='black')
ff2nd = Ellipse(xy=(xMove2.mean()['FF'], zMove2.mean()['FF']),
                width=xMove2.std()['FF'], height=zMove2.std()['FF'],
                color='r')
ch2nd = Ellipse(xy=(xMove2.mean()['CH'], zMove2.mean()['CH']),
                width=xMove2.std()['CH'], height=zMove2.std()['FF'],
                color='blue')
ft2nd = Ellipse(xy=(xMove2.mean()['FT'], zMove2.mean()['FT']),
                width=xMove2.std()['FT'], height=zMove2.std()['FT'],
                color='green', alpha=.9)
kc2nd = Ellipse(xy=(xMove2.mean()['KC'], zMove2.mean()['KC']),
                width=xMove2.std()['KC'], height=zMove2.std()['KC'],
                color='grey')
sl2nd = Ellipse(xy=(xMove2.mean()['SL'], zMove2.mean()['SL']),
                width=xMove2.std()['SL'], height=zMove2.std()['SL'],
                color='purple')
pitchList = [ff1, ch1, ft1, kc1, sl1, ff2nd, ch2nd, ft2nd, kc2nd, sl2nd]
makeEllipses(pitchList), ax.set_xlim(-1.5, 1.5), ax.set_ylim(-1.5, 1.5)
ax.legend(pitchList, ['ff1st', 'ch1st', 'ft1st', 'kc1st', 'sl1st',
                      'ff2nd', 'ch2nd', 'ft2nd', 'kc2nd', 'sl2nd'])
ax.set_xlabel("X-movement"), ax.set_ylabel("Y-movement")
ax.set_title("Movement from catcher's view")

# Looking at his batted ball percentages
"""This function coverts batted ball types from counting sum to percentages. 
Baseball Savant/pyBaseball gives all pitches thrown with their batted ball 
results (if the ball was put in play)."""

def battedBallsProfile(player):
    battedballs = player['launch_speed_angle'].value_counts()
    per = (battedballs / battedballs.sum()) * 100
    return round(per, 1)

hitType1 = battedBallsProfile(jack1)
hitType2 = battedBallsProfile(jack2)

#Below are charts
hitType1.rename(index={1: 'Weak', 2: 'Topped', 3: 'Under',
                       4: 'Flare/Burner', 5: 'Solid Contact',
                       6: 'Barrel'}, inplace=True)
hitType2.rename(index={1: 'Weak', 2: 'Topped', 3: 'Under',
                       4: 'Flare/Burner', 5: 'Solid Contact',
                       6: 'Barrel'}, inplace=True)
pd.merge(hitType1, hitType2, how='outer', left_index=True,
         right_index=True, suffixes=('_1st', '_2nd'))

hitType2018 = battedBallsProfile(jack2018)
hitType2018.rename(index={1: 'Weak', 2: 'Topped', 3: 'Under',
                          4: 'Flare/Burner', 5: 'Solid Contact',
                          6: 'Barrel'}, inplace=True)

pd.merge(hitType2018, hitType2, how='outer', left_index=True,
         right_index=True, suffixes=('_2018', '_2nd'))
pd.concat([hitType2018, hitType1, hitType2],
          keys=['2018', '1st_Half', '2nd_Half'], axis=1)

# Defined what each batted ball means, easier for everyday fan to understand
"""Need two arrays. Pie graphs are organized by decreasing %,
which messes up the labeling on the graphs"""
hitTypeLabels = ['Topped (Ground Ball)', 'Under (Pop Up)',
                 'Flare/Burner (Bloop Hit)', 'Barrel (Hard Hit)',
                 'Solid Contact (Line Drive)', 'Weak (Poorly Hit)']
hitTypeLabels2nd = ['Topped (Ground Ball)', 'Under (Pop Up)',
                    'Flare/Burner (Bloop Hit)', 'Weak (Poorly Hit)',
                    'Barrel (Hard Hit)', 'Solid Contact (Line Drive)']

# Pie graph
fig, axarr = plt.subplots(1, 3)
fig.set_size_inches(8, 7)
ax0 = axarr[0]
ax1 = axarr[1]
ax2 = axarr[2]

ax0.pie(hitType2018, autopct='%1.1f%%')
ax0.axis('equal')
ax0.set_title('2018', y=0.7)
ax0.legend(hitTypeLabels, loc='lower center')

ax1.pie(hitType1, autopct='%1.1f%%')
ax1.axis('equal')
ax1.set_title('2019 1st Half', y=0.7)
ax1.legend(hitTypeLabels, loc='lower center')

ax2.pie(hitType2, autopct='%1.1f%%')
ax2.axis('equal')
ax2.set_title('2019 2nd Half', y=0.7)
ax2.legend(hitTypeLabels2nd, loc='lower center')

fig.suptitle("Flaherty's Batted Balls%", fontweight='bold', y=.9)
fig.subplots_adjust(top=1.0, bottom=0.05, left=0.0, right=1.0, hspace=0.205,
                    wspace=0.068)

# x_label
hitTypeLabelsBars = ['Topped \n(Ground Ball) \n Higher=Better',
                     'Under \n(Pop Up) \n Higher=Better',
                     'Flare/Burner \n(Bloop Hit)',
                     'Barrel \n(Hard Hit) \n Lower= Better',
                     'Solid Contact \n(Line Drive) \n Lower= Better',
                     'Weak \n(Poorly Hit) \n Higher=Better']

widthBars = 0.8

# run all these lines together
fig, ax = plt.subplots()
fig.set_size_inches(8, 5)
bbBar2018 = ax.bar(hitTypeLabelsBars, hitType2018, label='2018',
                   width=widthBars, color='red')
bbBar1 = ax.bar(hitTypeLabelsBars, hitType1, label='2019 1st Half',
                width=widthBars / 1.5, color='grey')
bbBar2 = ax.bar(hitTypeLabelsBars, hitType2, label='2019 2nd Half',
                width=widthBars / 2, color='navy')
ax.set_xticklabels(hitTypeLabelsBars)
ax.set_ylabel("Batted Ball%")
ax.set_xlabel("Batted Ball Types")
ax.legend(loc='best')
ax.set_title("Flaherty's Batted Balls%")
fig.subplots_adjust(top=0.926, bottom=0.189, left=0.076, right=0.982,
                    hspace=0.2, wspace=0.2)
