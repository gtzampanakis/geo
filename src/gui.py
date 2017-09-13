import cProfile
import os
import Queue
import time
import threading
import traceback

from Tkinter import *
from tkFileDialog import askopenfilename, asksaveasfilename
import tkMessageBox
import ttk

import fileio as fio
import geomath as gm
import datamerge as dm

BASE_DIR = os.path.dirname(__file__)

# TODO: Handle all exceptions.
# TODO: Make it so that buttons can be pressed with Enter key.
# TODO: Check if empty files work
# TODO: Fix appearance using multiple frames
# TODO: Cancel button
# TODO: Disable all buttons while process is running
# TODO: make join functions start with smaller of the two lists
# TODO: report progress while writing files

root = Tk()
root.title('GeoTools')

MERGE_MODE_DISTANCE = 'DISTANCE'
MERGE_MODE_CLOSEST = 'CLOSEST'

ERROR_EMPTY_PATH = 'ERROR_EMPTY_PATH'
DISTANCE_EMPTY = 'DISTANCE_EMPTY'
K_CLOSEST_EMPTY = 'K_CLOSEST_EMPTY'

FN_CALL = 'FN_CALL'
FN_RESULT = 'FN_RESULT'
FN_EXCEPTION = 'FN_EXCEPTION'
EXIT = 'EXIT'
PROGRESS = 'PROGRESS'

ERROR_TO_MESSAGE = dict(
    ERROR_EMPTY_PATH = 'Please specify a path for File %s.',
    DISTANCE_EMPTY = 'Please specify a positive value for distance.',
    K_CLOSEST_EMPTY = 'Please specify a positive value for number of points.',
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
info_text_var = StringVar()

STYLE = ttk.Style()

STYLE.configure('error_text.TLabel', foreground='red')

def errmsg(code, *args):
    return ERROR_TO_MESSAGE[code] % args

def show_progress(rowi):
    info_text_var.set('Processing... Lines processed from File 1: %s' % rowi)

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
    STYLE.configure('distance.TRadiobutton', foreground='black')
    STYLE.configure('k_closest.TRadiobutton', foreground='black')

    error_texts = []

    path1_error = state.get('path1_error')
    if path1_error:
        STYLE.configure('path1.TButton', foreground='red')
        error_texts.append(errmsg(path1_error, 1))

    path2_error = state.get('path2_error')
    if path2_error:
        STYLE.configure('path2.TButton', foreground='red')
        error_texts.append(errmsg(path2_error, 2))
    
    distance_error = state.get('distance_error')
    if distance_error:
        STYLE.configure('distance.TRadiobutton', foreground='red')
        error_texts.append(errmsg(distance_error))

    k_closest_error = state.get('k_closest_error')
    if k_closest_error:
        STYLE.configure('k_closest.TRadiobutton', foreground='red')
        error_texts.append(errmsg(k_closest_error))

    error_text_var.set('\n'.join(error_texts))

F = ttk.Frame(root, padding="3 3 12 12")
F.grid(column=0, row=0, sticky=(N, W, E, S))
F.columnconfigure(0, weight=1)
F.rowconfigure(0, weight=1)

work_load_queue = Queue.Queue()
result_queue = Queue.Queue()

def work_thread_fn():
    while True:
        message = work_load_queue.get()
        print 'received_message', message
        if message['type'] == FN_CALL:
            try:
                iterator = message['fn'](
                    *message['args'],
                    **message['kwargs']
                )
                # profiler = cProfile.Profile()
                # profiler.runcall(fio.get_csv_writer, message['output_path'], iterator)
                # profiler.dump_stats('prof.txt')
                result = fio.get_csv_writer(message['output_path'], iterator)
            except Exception as e:
                result_queue.put({
                    'type': FN_EXCEPTION,
                    'exception': e,
                    'exc_info': sys.exc_info(),
                })
            else:
                result_queue.put({
                    'type': FN_RESULT,
                    'return_value': result
                })
        elif message['type'] == EXIT:
            return

work_thread = threading.Thread(target=work_thread_fn)
work_thread.daemon = True
work_thread.start()

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
    set_state({
        'distance_error': None,
        'k_closest_error': None,
    })

def on_merge_click():
    proceed = True

    state_updates = {}
    if not state['path1']:
        state_updates.update({ 'path1_error': ERROR_EMPTY_PATH })
        proceed = False
    else:
        state_updates.update({ 'path1_error': None })
    if not state['path2']:
        state_updates.update({ 'path2_error': ERROR_EMPTY_PATH })
        proceed = False
    else:
        state_updates.update({ 'path2_error': None })

    state_updates.update({
        'distance_error': None,
        'k_closest_error': None,
    })

    if state['merge_mode_var'].get() == MERGE_MODE_DISTANCE:
        ft = state['distance_threshold_var'].get()
        if not ft or int(ft) <= 0:
            state_updates.update({ 'distance_error': DISTANCE_EMPTY })
            proceed = False
        else:
            state_updates.update({ 'distance_error': None })

    elif state['merge_mode_var'].get() == MERGE_MODE_CLOSEST:
        ft = state['k_closest_var'].get()
        if not ft or int(ft) <= 0:
            state_updates.update({ 'k_closest_error': K_CLOSEST_EMPTY })
            proceed = False
        else:
            state_updates.update({ 'k_closest_error': None })

    set_state(state_updates)

    if proceed:
        path = asksaveasfilename(
            defaultextension='.csv',
            filetypes=[('CSV', '*.csv')]
        )
        if path:
            if state['merge_mode_var'].get() == MERGE_MODE_DISTANCE:
                args = []
                kwargs = {
                    'threshold':
                        gm.ft_to_m(int(state['distance_threshold_var'].get()))
                }
            elif state['merge_mode_var'].get() == MERGE_MODE_CLOSEST:
                args = []
                kwargs = {
                    'k_closest': int(state['k_closest_var'].get())
                }
            kwargs['result_queue'] = result_queue
            message = {
                'type': FN_CALL,
                'fn': dm.join_files,
                'args': (state['path1'], state['path2']),
                'kwargs': kwargs,
                'output_path': path
            }
            info_text_var.set('')
            merge_button['state'] = DISABLED
            work_load_queue.put(message)
            info_text_var.set('Processing...')

def validate_integer_key_press(action_code, new_char, full_text):
    if action_code == '1':
        if new_char in [str(i) for i in xrange(10)]:
            if full_text and int(full_text) > 0:
                set_state({
                    'distance_error': None,
                    'k_closest_error': None,
                })
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
    command=on_merge_mode_change,
    style='distance.TRadiobutton'
).grid(column=0, row=2*pathi+3, sticky=(W))

distance_threshold_entry = ttk.Entry(
    F, width=10, textvariable=state['distance_threshold_var'],
    validate='key'
)
validate_integer_key_press_cmd = distance_threshold_entry.register(
                                                    validate_integer_key_press)
distance_threshold_entry['validatecommand'] = (
                                          validate_integer_key_press_cmd,
                                          '%d', '%S', '%P')
distance_threshold_entry.grid(column=1, row=2*pathi+3, sticky=(W))

ttk.Label(
    F, text='feet'
).grid(column=2, row=2*pathi+3, sticky=(W))

ttk.Radiobutton(
    F, text='Number of points',
    value=MERGE_MODE_CLOSEST, variable=state['merge_mode_var'],
    command=on_merge_mode_change,
    style='k_closest.TRadiobutton'
).grid(column=0, row=2*pathi+4, sticky=(W))

k_closest_entry = ttk.Entry(
    F, width=10, textvariable=state['k_closest_var'],
    validate='key'
)

set_state({}) # To cause the DISABLED state to be set on the correct entry.

validate_integer_key_press_cmd = k_closest_entry.register(
                                                    validate_integer_key_press)
k_closest_entry['validatecommand'] = (validate_integer_key_press_cmd,
                                      '%d', '%S', '%P')
k_closest_entry.grid(column=1, row=2*pathi+4, sticky=(W))

ttk.Label(
    F, text='points'
).grid(column=2, row=2*pathi+4, sticky=(W))

merge_button = ttk.Button(
    F, text='Save merged file', command=on_merge_click
)
merge_button.grid(column=0, columnspan=3, sticky=(W, E))

Label(
    F, textvariable=info_text_var,
    anchor=NW,
    justify=LEFT
).grid(column=0, columnspan=3, sticky=(W, E))

Label(
    F, textvariable=error_text_var,
    height=4,
    foreground='red',
    anchor=NW,
    justify=LEFT,
    #style='error_text.TLabel',
).grid(column=0, columnspan=3, sticky=(W, E))

for child in F.winfo_children(): child.grid_configure(padx=5, pady=5)

def check_result_queue():
    try:
        result_dict = result_queue.get(block=False)
        if result_dict['type'] == FN_RESULT:
            merge_button['state'] = NORMAL
            return_value = result_dict['return_value']
            info_text_var.set(info_text_var.get() + '\n' + 'Done.')
        elif result_dict['type'] == FN_EXCEPTION:
            merge_button['state'] = NORMAL
            exception = result_dict['exception']
            tkMessageBox.showerror(
                'Error',
                'Unexpected error: %s\n%s' % (
                    exception,
                    ''.join(traceback.format_tb( result_dict['exc_info'][2]))
                )
            )
            info_text_var.set(info_text_var.get() + '\n' + 'Error.')
        elif result_dict['type'] == PROGRESS:
            show_progress(result_dict['payload'])

    except Queue.Empty as e:
        pass
    root.after(10, check_result_queue)

root.after(100, check_result_queue)

root.wm_iconbitmap(os.path.join(BASE_DIR, 'favicon.ico'))
root.mainloop()

work_load_queue.put({'type': EXIT})

