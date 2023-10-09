# Langton's ant

import numpy as np
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.patches as patches
import tkinter as tk
from tkinter import ttk
import matplotlib.ticker as ticker


def skip_step(step_skip):
    global cnt, tx_step
    for i in range(step_skip):
        next_step()
        cnt += 1
    tx_step.set_text("Step=" + str(cnt))
    update_ant()
    update_scat()


def next_step():
    global cells
    value_cell = cells[x_center_ant][y_center_ant]
    if value_cell == 0:
        turn_right()
        cells[x_center_ant][y_center_ant] = 1
        forward()
    else:
        turn_left()
        cells[x_center_ant][y_center_ant] = 0
        forward()


def turn_right():
    global angle_ant
    angle_ant -= 90
    if angle_ant < 0:
        angle_ant = 270
    update_ant()


def turn_left():
    global angle_ant
    angle_ant += 90
    if angle_ant > 270:
        angle_ant = 0
    update_ant()


def forward():
    global center_ant, x_center_ant, y_center_ant
    if angle_ant == 0:
        x_center_ant += 1
        if x_center_ant > num_of_cells_x - 1:
            x_center_ant = 0
    elif angle_ant == 90:
        y_center_ant += 1
        if y_center_ant > num_of_cells_y - 1:
            y_center_ant = 0
    elif angle_ant == 180:
        x_center_ant -= 1
        if x_center_ant < 0:
            x_center_ant = num_of_cells_x - 1
    elif angle_ant == 270:
        y_center_ant -= 1
        if y_center_ant < 0:
            y_center_ant = num_of_cells_y - 1
    else:
        pass
    update_ant()


def update_ant():
    global xx_body_ant, yy_body_ant, xx_legs_ant, yy_legs_ant, xy_head_ant, xy_belly_ant, body_ant
    global body_ant, legs_ant, head_ant, belly_ant
    if angle_ant == 0:
        xx_body_ant = [x_center_ant - length_ant / 2., x_center_ant + length_ant / 2.]
        yy_body_ant = [y_center_ant, y_center_ant]
        xx_legs_ant = [x_center_ant, x_center_ant]
        yy_legs_ant = [y_center_ant - length_ant / 2., y_center_ant + length_ant / 2.]
        xy_head_ant = [x_center_ant + length_ant / 2., y_center_ant]
        xy_belly_ant = [x_center_ant - length_ant / 2., y_center_ant]
    elif angle_ant == 90:
        xx_body_ant = [x_center_ant, x_center_ant]
        yy_body_ant = [y_center_ant - length_ant / 2., y_center_ant + length_ant / 2.]
        xx_legs_ant = [x_center_ant - length_ant / 2., x_center_ant + length_ant / 2.]
        yy_legs_ant = [y_center_ant, y_center_ant]
        xy_head_ant = [x_center_ant, y_center_ant + length_ant / 2.]
        xy_belly_ant = [x_center_ant, y_center_ant - length_ant / 2.]
    elif angle_ant == 180:
        xx_body_ant = [x_center_ant - length_ant / 2., x_center_ant + length_ant / 2.]
        yy_body_ant = [y_center_ant, y_center_ant]
        xx_legs_ant = [x_center_ant, x_center_ant]
        yy_legs_ant = [y_center_ant - length_ant / 2., y_center_ant + length_ant / 2.]
        xy_head_ant = [x_center_ant - length_ant / 2., y_center_ant]
        xy_belly_ant = [x_center_ant + length_ant / 2., y_center_ant]
    elif angle_ant == 270:
        xx_body_ant = [x_center_ant, x_center_ant]
        yy_body_ant = [y_center_ant - length_ant / 2., y_center_ant + length_ant / 2.]
        xx_legs_ant = [x_center_ant - length_ant / 2., x_center_ant + length_ant / 2.]
        yy_legs_ant = [y_center_ant, y_center_ant]
        xy_head_ant = [x_center_ant, y_center_ant - length_ant / 2.]
        xy_belly_ant = [x_center_ant, y_center_ant + length_ant / 2.]
    else:
        pass
    body_ant.set_data(xx_body_ant, yy_body_ant)
    legs_ant.set_data(xx_legs_ant, yy_legs_ant)
    head_ant.set_center(xy_head_ant)
    belly_ant.angle = angle_ant
    belly_ant.set_center(xy_belly_ant)


def set_angle_ant(value):
    global angle_ant
    angle_ant = int(value)
    update_ant()


def mouse_motion(event):
    global lbl_info_cell, cells, x_center_ant, y_center_ant
    if event.dblclick == 1:
        # print("double click")
        pass
    elif event.button == 1:
        # print("left click")
        if str(event.xdata) != "None" and str(event.ydata) != "None":
            # print(event.xdata, event.ydata)
            if 0 <= round(event.xdata) <= num_of_cells_x - 1 and 0 <= round(event.ydata) <= num_of_cells_y - 1:
                # print(round(event.xdata), round(event.ydata))
                x_rd = round(event.xdata)
                y_rd = round(event.ydata)
                if var_radio_click_option.get() == 1:
                    if cells[x_rd][y_rd] == 0:
                        cells[x_rd][y_rd] = 1
                    else:
                        cells[x_rd][y_rd] = 0
                else:
                    x_center_ant = x_rd
                    y_center_ant = y_rd
                    # print(x_center_ant, y_center_ant)
                    update_ant()
                lbl_info_cell['text'] = "Cell(x" + str(x_rd) + ", y" + str(y_rd) + ")=" + str(cells[x_rd][y_rd])
                update_scat()
    elif event.button == 3:
        # print("right click")
        pass


def update_scat():
    global scat0, x_scat0, y_scat0, size_scat0, color_scat0
    x_scat0.clear()
    y_scat0.clear()
    size_scat0.clear()
    color_scat0.clear()
    for i in range(num_of_cells_y):
        for j in range(num_of_cells_x):
            if cells[j][i] != 0.:
                y_scat0.append(i)
                x_scat0.append(j)
                size_scat0.append(size_maker)
                color_scat0.append(cells[j][i])
    scat0.set_offsets(np.column_stack([x_scat0, y_scat0]))
    scat0.set_sizes(size_scat0)
    scat0.set_array(np.array(color_scat0))


def clear_cells():
    global is_play, cnt, tx_step, cells
    is_play = False
    cnt = 0
    tx_step.set_text("Step=" + str(cnt))
    cells = np.zeros((num_of_cells_x, num_of_cells_y))
    update_scat()


def adjust_size_marker():
    global size_maker
    area_fig = fig.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    width_fig = area_fig.width * fig.dpi
    height_fig = area_fig.height * fig.dpi
    # print((width, height))
    size_x = width_fig / (x_max - x_min)
    size_maker = size_x
    update_scat()


def on_change_window(e):
    adjust_size_marker()


def step():
    global cnt
    cnt += 1
    tx_step.set_text("Step=" + str(cnt))
    next_step()
    update_ant()
    update_scat()


def switch():
    global is_play
    if is_play:
        is_play = False
    else:
        is_play = True
    tx_step.set_text("Step=" + str(cnt))


def update(f):
    global tx_step, cnt
    if is_play:
        tx_step.set_text("Step=" + str(cnt))
        cnt += 1
        update_ant()
        update_scat()
        next_step()


# Global variables

# Animation control
cnt = 0
is_play = False

# Parameters
num_of_cells_x = 80
num_of_cells_y = 80

# Data array
cells = np.zeros((num_of_cells_x, num_of_cells_y))

# Generate figure and axes
title_ax0 = "Langton's ant"
title_tk = title_ax0
x_min = 0.
x_max = num_of_cells_x
y_min = 0.
y_max = num_of_cells_y

fig = Figure()
ax0 = fig.add_subplot(111)
ax0.set_title(title_ax0)
ax0.set_xlabel("x")
ax0.set_ylabel("y")
ax0.set_xlim(x_min, x_max)
ax0.set_ylim(y_min, y_max)
ax0.set_aspect("equal")
ax0.grid()
# ax0.invert_yaxis()
x_ticks = []
for ix in range(num_of_cells_x):
    x_ticks.append(ix)
ax0.xaxis.set_major_locator(ticker.FixedLocator(x_ticks))
y_ticks = []
for iy in range(num_of_cells_y):
    y_ticks.append(iy)
ax0.yaxis.set_major_locator(ticker.FixedLocator(y_ticks))
ax0.set_xticklabels(x_ticks, fontsize=5)
ax0.set_yticklabels(y_ticks, fontsize=5)

# Generate graphic items
tx_step = ax0.text(x_min, y_max * 0.95, "Step=" + str(0))
x_scat0 = []
y_scat0 = []
size_scat0 = []
color_scat0 = []
size_maker = 40
# Color maps: seismic, binary
scat0 = ax0.scatter(x_scat0, y_scat0, marker='s', s=size_maker, c=color_scat0, cmap='binary', vmin=0., vmax=1.)

# Ant
x_center_ant = int(num_of_cells_x / 2)
y_center_ant = int(num_of_cells_y / 2)
center_ant = [y_center_ant, y_center_ant]
angle_ant = 0
length_ant = 1.
size_ant = 0.2

xx_body_ant = [x_center_ant - length_ant / 2., x_center_ant + length_ant / 2.]
yy_body_ant = [y_center_ant, y_center_ant]
body_ant, = ax0.plot(xx_body_ant, yy_body_ant, color='red', linewidth=3)
xx_legs_ant = [x_center_ant, x_center_ant]
yy_legs_ant = [y_center_ant - length_ant / 2., y_center_ant + length_ant / 2.]
legs_ant, = ax0.plot(xx_legs_ant, yy_legs_ant, color='red', linewidth=1)
xy_head_ant = [x_center_ant + length_ant / 2., y_center_ant]
head_ant = patches.Circle(xy=xy_head_ant, radius=size_ant, color='red')
ax0.add_patch(head_ant)
xy_belly_ant = [x_center_ant - length_ant / 2., y_center_ant]
belly_ant = patches.Ellipse(xy=xy_belly_ant, width=size_ant * 2 * 1.5, height=size_ant * 2 * 1.2,
                            angle=angle_ant, color='red')
ax0.add_patch(belly_ant)


# Tkinter
root = tk.Tk()
root.title(title_tk)
canvas = FigureCanvasTkAgg(fig, root)
canvas.get_tk_widget().pack(expand=True, fill='both')
canvas.mpl_connect('button_press_event', mouse_motion)

toolbar = NavigationToolbar2Tk(canvas, root)
canvas.get_tk_widget().pack()

# Animation control
# Frame
frm_ac = ttk.Labelframe(root, relief="ridge", text="Animation control", labelanchor="n", width=100)
frm_ac.pack(side='left', fill=tk.Y)
# Play and pause button
btn_pp = tk.Button(frm_ac, text="Play/Pause", command=switch)
btn_pp.pack()
# Step button
btn_pp = tk.Button(frm_ac, text="Step", command=step)
btn_pp.pack()
# Clear button
btn_clr = tk.Button(frm_ac, text="Clear cells", command=clear_cells)
btn_clr.pack()

# Ant setting
frm_parameter = ttk.Labelframe(root, relief="ridge", text="Ant control", labelanchor="n")
frm_parameter.pack(side='left', fill=tk.Y)
'''
lbl_angle = tk.Label(frm_parameter, text="Starting angle:")
lbl_angle.pack()
var_angle = tk.StringVar(root)  # variable for spinbox-value
var_angle.set(angle_ant)  # Initial value
spn_angle = tk.Spinbox(
    frm_parameter, textvariable=var_angle, format="%.0f", from_=0, to=270, increment=90,
    command=lambda: set_angle_ant(var_angle.get()), width=6
)
spn_angle.pack()
'''
# Turn right button
btn_tr = tk.Button(frm_parameter, text="Turn right", command=turn_right)
btn_tr.pack()
# Turn left button
btn_tl = tk.Button(frm_parameter, text="turn left", command=turn_left)
btn_tl.pack()
# Forward button
btn_fd = tk.Button(frm_parameter, text="Forward", command=forward)
btn_fd.pack()
# Skip button
btn_skp = tk.Button(frm_parameter, text="Skip 1000 steps", command=lambda: skip_step(1000))
btn_skp.pack()

# Option
# Frame
frm_cp = ttk.Labelframe(root, relief="ridge", text="Option", labelanchor="n")
frm_cp.pack(side='left', fill=tk.Y)
var_radio_click_option = tk.IntVar(root)
# Radio button 1st
rd_increase = tk.Radiobutton(frm_cp, text="Move ant", value=0, var=var_radio_click_option)
rd_increase.pack()
# Radio button 2st
rd_increase = tk.Radiobutton(frm_cp, text="On/off cell", value=1, var=var_radio_click_option)
rd_increase.pack()
# Set default of radio buttons
var_radio_click_option.set(0)

# Information of a cell clicked
# Frame
frm_info = ttk.Labelframe(root, relief="ridge", text="Information", labelanchor="n")
frm_info.pack(side='left', fill=tk.Y)
# Information label
lbl_info_cell = tk.Label(frm_info, text="Cell(x0, y0)=0")
lbl_info_cell.pack(side='left')

# Initialize data
adjust_size_marker()
update_ant()
update_scat()

# Draw animation
anim = animation.FuncAnimation(fig, update, interval=50)
root.bind('<Configure>', on_change_window)
root.mainloop()
