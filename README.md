# avakaya
Saving matplotlib figure pickle as a standalone executable

have you ever faced an issue where you have to show your boss/guide/collegue some plot you did in python, share it in a png format. but when you show them, you wish you can actually zoom the plot instead of zoomig the image file. 
You want to show somehting you saw in your own system, but others can't see that unless they come to your place.
Or maybe felt the title was wrong
Wouldn't it be good if you just share a file for a plot, but the file opens in a matplotlib figure window instead of a image viewer.
And you can drag, zoom , change title, and everything, have your shared axes in subplots etc ?
Presenting you "avakaya" (mango pickle in telugu)

Add the startup file in ipython startup folder, and then you can use %save_mpl_fig magic inside ipython prompt to save the current active figure.
To run the figure just enter ./figure.pp in terminal, same as a shell script (it is a shell script, where pp stands for pickle plot). 

This is made in linux, for linux systems. Before opening the figure file, make sure that there is python and matplotlib installed.
