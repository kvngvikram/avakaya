###############################################################################
# Written by Vikram KVNG (kvngvikram@pm.me)
# Copy paste this file in ~/.ipython/profile_default/startup/ folder and you
# can use the %save_mpl_fig magic function to save the currently active
# matplotlib figure as a pickle file or a standalone executable file.
###############################################################################
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import os
from IPython.core.magic import register_line_magic
try:
    import dill as pickle
    dill_present = True
except ModuleNotFoundError:
    import pickle
    dill_present = False

our_extension = "pp"


shell_script = f'''
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
python3 -c '
#python_begin
import io
import os
import sys
import re
from sys import argv
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
saving_file_with_dill = {dill_present}
if saving_file_with_dill:
    try:
        import dill as pickle
    except ModuleNotFoundError:
        print("Hey, I was saved as pickle using dill package,")
        print("not the native pickle package.")
        print("And you do not have dill installed.")
        print("So install it !")
        print("dill can help me work with secondary axis and maybe more")
        print("Anyway, aborting gracefully..")
        sys.exit()
else:
    import pickle
    try:
        import dill
    except ModuleNotFoundError:
        print("Please install dill package for more features")
        print("like secondary axis feature, and maybe more")

self_filename = argv[1]
our_extension = self_filename.split(".")[-1]
save_key = "ctrl+k"  # small k

with open(self_filename, "rb") as f:
    payload_flag, ba, script_bytes = False, b"", b""
    for i in f:
        script_bytes = script_bytes + i if not payload_flag else script_bytes
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
                with open(filename, "wb") as pickle_file:
                    pickle.dump(fig, pickle_file)

            else:
                with open(filename, "wb") as script_file:
                    script_file.write(script_bytes)

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
print("    ||       Press Ctrl+k to save any changes !!       ||")
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
    # to work with both functions and magic
    arg = args[0] if len(args) > 0 else ""

    fig_nums = plt.get_fignums()
    fig_labels = plt.get_figlabels()

    if len(fig_nums) > 0:
        if len(arg) > 0:
            if arg in fig_labels:
                fig = plt.figure(arg)
                fig_name = arg
            elif arg in [str(i) for i in fig_nums]:
                fig = plt.figure(int(arg))
                fig_name = arg
            else:
                print("wrong argument, getting the current figure")
                fig = plt.gcf()
                # fig_name = fig.canvas.get_window_title()
                fig_name = ""
        else:
            fig = plt.gcf()
            # fig_name = fig.canvas.get_window_title()
            fig_name = ""

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
