import os
import threading
import traceback

from Tkinter import *
from tkFileDialog import askopenfilename, asksaveasfilename
import tkMessageBox
import ttk

import geomath as gm
import datamerge as dm

root = Tk()
root.title("Geography")

MERGE_MODE_DISTANCE = 'DISTANCE'
MERGE_MODE_CLOSEST = 'CLOSEST'

ERROR_EMPTY_PATH = 'ERROR_EMPTY_PATH'
DISTANCE_EMPTY = 'DISTANCE_EMPTY'

ERROR_TO_MESSAGE = dict(
    ERROR_EMPTY_PATH = 'Please specify a path for File %s.',
    DISTANCE_EMPTY = 'Please specify a positive value for distance.',
)

state = dict(
    path1 = None,
    path2 = None,
    merge_mode_var = StringVar(),
    distance_threshold_var = StringVar(),
    k_closest_var = StringVar(),
    path1_error = None,
    path2_error = None,
)

state['merge_mode_var'].set(MERGE_MODE_DISTANCE)

path1_var = StringVar()
path2_var = StringVar()

error_text_var = StringVar()

STYLE = ttk.Style()

STYLE.configure('error_text.TLabel', foreground='red')

def errmsg(code, *args):
    return ERROR_TO_MESSAGE[code] % args

def set_state(updates):
    state.update(updates)

    path1_var.set(state['path1'] and os.path.basename(state['path1']) or '')
    path2_var.set(state['path2'] and os.path.basename(state['path2']) or '')

    if state['merge_mode_var'].get() == MERGE_MODE_DISTANCE:
        distance_threshold_entry['state'] = NORMAL
        k_closest_entry['state'] = DISABLED
    elif state['merge_mode_var'].get() == MERGE_MODE_CLOSEST:
        distance_threshold_entry['state'] = DISABLED
        k_closest_entry['state'] = NORMAL

    STYLE.configure('path1.TButton', foreground='black')
    STYLE.configure('path2.TButton', foreground='black')
    STYLE.configure('path1.TLabel', foreground='black')
    STYLE.configure('path2.TLabel', foreground='black')

    error_texts = []

    path1_error = state.get('path1_error')
    if path1_error:
        STYLE.configure('path1.TButton', foreground='red')
        error_texts.append(errmsg(path1_error, 1))

    path2_error = state.get('path2_error')
    if path2_error:
        STYLE.configure('path2.TButton', foreground='red')
        error_texts.append(errmsg(path1_error, 2))
    
    distance_error = state.get('distance_error')
    if distance_error:
        error_texts.append(errmsg(distance_error))

    error_text_var.set('\n'.join(error_texts))

F = ttk.Frame(root, padding="3 3 12 12")
F.grid(column=0, row=0, sticky=(N, W, E, S))
F.columnconfigure(0, weight=1)
F.rowconfigure(0, weight=1)

def work_thread_fn(fn, *args, **kwargs):
    merge_button['state'] = DISABLED
    try:
        fn(*args, **kwargs)
        1/0
    except Exception as e:
        tkMessageBox.showerror('Error', unicode(e))
    merge_button['state'] = NORMAL

def on_path_selection_1():
    path = askopenfilename()
    if path:
        set_state(dict(
            path1 = path,
            path1_error = None,
        ))

def on_path_selection_2():
    path = askopenfilename()
    if path:
        set_state(dict(
            path2 = path,
            path2_error = None,
        ))

def on_merge_mode_change():
    set_state({})

def on_merge_click():
    path = asksaveasfilename(
        defaultextension='.csv',
        filetypes=[('CSV', '*.csv')]
    )
    if path:

        proceed = True

        if not state['path1']:
            set_state({ 'path1_error': ERROR_EMPTY_PATH })
            proceed = False
        else:
            set_state({ 'path1_error': None })
        if not state['path2']:
            set_state({ 'path2_error': ERROR_EMPTY_PATH })
            proceed = False
        else:
            set_state({ 'path2_error': None })

        if state['merge_mode_var'].get() == MERGE_MODE_DISTANCE:
            ft = state['distance_threshold_var'].get()
            if not ft or float(ft) <= 0:
                set_state({ 'distance_error': DISTANCE_EMPTY })
                proceed = False
            else:
                set_state({ 'distance_error': None })

            if proceed:
                work_thread = threading.Thread(
                    target = work_thread_fn,
                    args = [
                        dm.join_on_distance_threshold,
                        lambda: dm.path_to_coords_iterator(state['path1']),
                        lambda: dm.path_to_coords_iterator(state['path2']),
                        gm.ft_to_m(float(state['distance_threshold_var'].get()))
                    ]
                )
                work_thread.start()

def validate_integer_key_press(action_code, new_char):
    if action_code == '1':
        if new_char in [str(i) for i in xrange(10)]:
            return True
    elif action_code == '0':
        return True
    return False

path_buttons = [None, None]
path_info_labels = [None, None]

for pathi, select_command, path_var in zip(
    [0, 1],
    [on_path_selection_1, on_path_selection_2],
    [path1_var, path2_var],
):
    path_buttons[pathi] = ttk.Button(
        F, text='Open File %s' % (pathi+1),
        command=select_command,
        style='path%s.TButton' % (pathi+1)
    )
    path_buttons[pathi].grid(column=0, row=2*pathi, sticky=(W))
    
    ttk.Label(
        F, textvariable=path_var, width=50
    ).grid(column=1, row=2*pathi, sticky=(W))

ttk.Label(
    F, text='Merge by:'
).grid(column=0, row=2*pathi+2, sticky=(W))

ttk.Radiobutton(
    F, text='Distance',
    value=MERGE_MODE_DISTANCE, variable=state['merge_mode_var'],
    command=on_merge_mode_change
).grid(column=0, row=2*pathi+3, sticky=(W))

distance_threshold_entry = ttk.Entry(
    F, width=10, textvariable=state['distance_threshold_var'],
    validate='key'
)
validate_integer_key_press_cmd = distance_threshold_entry.register(
                                                    validate_integer_key_press)
distance_threshold_entry['validatecommand'] = (
                                          validate_integer_key_press_cmd,
                                          '%d', '%S')
distance_threshold_entry.grid(column=1, row=2*pathi+3, sticky=(W))

ttk.Label(
    F, text='feet'
).grid(column=2, row=2*pathi+3, sticky=(W))

ttk.Radiobutton(
    F, text='Number of points',
    value=MERGE_MODE_CLOSEST, variable=state['merge_mode_var'],
    command=on_merge_mode_change
).grid(column=0, row=2*pathi+4, sticky=(W))

k_closest_entry = ttk.Entry(
    F, width=10, textvariable=state['k_closest_var'],
    validate='key'
)

set_state({}) # To cause the DISABLED state to be set on the correct entry.

validate_integer_key_press_cmd = k_closest_entry.register(
                                                    validate_integer_key_press)
k_closest_entry['validatecommand'] = (validate_integer_key_press_cmd,
                                      '%d', '%S')
k_closest_entry.grid(column=1, row=2*pathi+4, sticky=(W))

ttk.Label(
    F, text='points'
).grid(column=2, row=2*pathi+4, sticky=(W))

merge_button = ttk.Button(
    F, text='Save merged file', command=on_merge_click
)
merge_button.grid(column=0, columnspan=3, sticky=(W, E))

ttk.Label(
    F, textvariable=error_text_var,
    style='error_text.TLabel'
).grid(column=0, columnspan=3, sticky=(W, E))

for child in F.winfo_children(): child.grid_configure(padx=5, pady=5)

root.mainloop()
