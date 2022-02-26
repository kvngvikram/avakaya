###############################################################################
# Written by Vikram KVNG (kvngvikram@pm.me)
# Copy paste this file in ~/.ipython/profile_default/startup/ folder and you
# can use the %save_mpl_fig magic function to save the currently active
# matplotlib figure as a pickle file or a standalone executable file.
###############################################################################
import pickle
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import os
from IPython.core.magic import register_line_magic

our_extension = "pp"


shell_script = '''
#/usr/bin/sh
###############################################################################
#
# I am an executable to show python matplotlib figure
# Just run me like ./my_name.pp and I will show you those plots you want to see
#
# About myself:
#     Vikram KVNG is my maker and god. You can pray to him via kvngvikram@pm.me
# I start with some ASCII script but after the line __PAYLOAD_BEGIN__, I am
# just what the pickle file is of the figure
#
###############################################################################
python -c '
#python_begin
import pickle
import io
import os
from sys import argv
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog

self_filename = argv[1]
our_extension = self_filename.split(".")[-1]
save_key = "ctrl+S"

with open(self_filename, "rb") as f:
    payload_flag, ba, bs = False, b"", b""
    for i in f:
        bs = bs + i if not payload_flag else bs
        ba = ba + i if payload_flag else ba
        payload_flag = True if (i == b"__PAYLOAD_BEGIN__\\n") else payload_flag

fig = pickle.load(io.BytesIO(ba))
# fig = pickle.load(io.BytesIO(ba))
# fig_name = fig.canvas.get_window_title()

def save_as(event):
    if event.key == save_key:
        root = tk.Tk()
        root.withdraw()
        filename = filedialog.asksaveasfilename(
                initialdir=os.getcwd(),
                initialfile=self_filename,
                filetypes=((f"{our_extension} files", f"*.{our_extension}"),
                           ("pickle files", "*.pickle"),
                           ("all files", "*.*")))

        if len(filename) > 0:

            entered_extension = filename.split(".")[-1]

            if entered_extension == "pickle":
                # just save the pickle
                with open(filename, "wb") as script_file:
                    pickle.dump(fig, script_file)

            else:
                with open(filename, "wb") as script_file:
                    script_file.write(bs)

                with open(filename, "ab") as script_file:
                    pickle.dump(fig, script_file)

                os.chmod(filename, 0o777)






fig.canvas.mpl_connect("key_release_event", save_as)
print("")
print("")
print("")
print("       _______________________________________________")
print("      /_______________________________________________\\\\")
print("     //                                               \\\\\\\\")
print("    ||                                                 ||")
print("    ||    Press Ctrl+Shift+S to save any changes !!    ||")
print("    ||                                                 ||")
print("     \\\\\\\\_______________________________________________//")
print("      \\\\_______________________________________________/")


plt.show()
#python_end
' "$0"; exit
__PAYLOAD_BEGIN__
'''


@register_line_magic
def save_mpl_fig(*args):
    fig_nums = plt.get_fignums()
    fig_labels = plt.get_figlabels()

    arg = args[0]

    if len(fig_nums) > 0:
        if len(arg) > 0:
            if arg in fig_labels:
                fig = plt.figure(arg)
                fig_name = arg
            elif int(arg) in fig_nums:
                fig = plt.figure(int(arg))
                fig_name = arg
            else:
                print("wrong argument, getting the current figure")
                fig = plt.gcf()
                fig_name = fig.canvas.get_window_title()
        else:
            fig = plt.gcf()
            fig_name = fig.canvas.get_window_title()

        root = tk.Tk()
        root.withdraw()

        filename = filedialog.asksaveasfilename(
                initialdir=os.getcwd(),
                initialfile=f"{fig_name}.{our_extension}",
                filetypes=((f"{our_extension} files", f"*.{our_extension}"),
                           ("pickle files", "*.pickle"),
                           ("all files", "*.*")))

        if len(filename) > 0:

            entered_extension = filename.split(".")[-1]

            if entered_extension == "pickle":
                # just save the pickle
                with open(filename, "wb") as script_file:
                    pickle.dump(fig, script_file)

            else:
                with open(filename, "w") as script_file:
                    script_file.write(shell_script)

                with open(filename, "ab") as script_file:
                    pickle.dump(fig, script_file)

                os.chmod(filename, 0o777)
    else:
        print("no figures to save")
