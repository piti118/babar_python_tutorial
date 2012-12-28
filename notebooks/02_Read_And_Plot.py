# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# #Reading ROOT file and plotting Stuff
# 
# In this tutorial we will teach you how to read ROOT data file efficiently using [root_numpy](http://rootpy.github.com/root_numpy/), some basic [numpy](http://www.numpy.org/) that you will be using a lot, and how to make pretty plots with ease using [matplotlib](http://matplotlib.org/). For this tutorial, you will find [inumpy](https://github.com/piti118/inumpy) very useful.

# <markdowncell>

# ##Reading ROOT file
# 
# We have our data stored in data directory

# <codecell>

from root_numpy import root2rec
import numpy as np

# <codecell>

%load_ext inumpy
%pylab inline

# <codecell>

ls data

# <markdowncell>

# This is how you read root files. This will read the whole file into your memory(this allows for fast plotting/replotting).

# <codecell>

bb = root2rec('data/B0B0*.root')
cc = root2rec('data/cc*.root')
data = root2rec('data/*.root')

# <markdowncell>

# There are many way you can specify how root2rec should read your file: you can pass array for filenames, you can tell it to read specific branch only to save memory. You can read them all in [root_numpy documentation](http://rootpy.github.com/root_numpy/).

# <markdowncell>

# ####Accessing Data
# If you want to see what's in there
# ```
# bb.dtype.names
# ```
# 
# inumpy provieds auto complete for recarray you can try. You can never remember what's the field names are.

# <codecell>

print bb.dtype.names

# <codecell>

#type bb.<TAB> here

# <markdowncell>

# ####By Element
# Most basic stuff.

# <codecell>

print data.R2All[0]

# <codecell>

#some of them are array
print data.mcLund[0]
print data.mcLund[0][0]

# <markdowncell>

# ##Important information about plotting
# 
# You should visit [matplotlib gallery](http://matplotlib.org/gallery.html) normally what I do when I want to plot something is to find something that resemble what I'm trying to plot and look at their code.

# <codecell>

#you can use loadpy to load the code to try out
#%loadpy http://matplotlib.org/mpl_examples/pylab_examples/integral_demo.py

# <markdowncell>

# ##Basic Histogram
# 
# We usually want to make some plots from data.

# <codecell>

hist(data.R2All); #super basic one

# <codecell>

#try out hist(<TAB> here
#We can't remember all those arguments name right

# <codecell>

#some basic stuff to do with plotting
hist(data.R2All, bins=100, histtype='step', color='green')
title('R2ALL')
xlabel('Some label');
ylabel(r'$\theta \alpha \beta \Upsilon$', fontsize=20)#note the "r" infornt of string this prevent backslash escape (ex \n);
#setting limit
xlim(-1,1)# xlim(xmin=yournumber) works too
#if you want y limit use ylim()
grid(True)

# <markdowncell>

# ####Overlaying histograms

# <codecell>

#you can plot them at the same time and have the binning determined simultaneously
hist([data.R2All, bb.R2All, cc.R2All], bins=100, histtype='step', label=['data','bb','cc'])
legend(loc='upper left')

# <codecell>

#You can plot them one at a time but becareful of binning

#this kinda work but automatic binning will make result hard to interpret.
#notice where red line go over blue line....
#since multiple automatic binning may not get the binsize/edges align.
hist(data.R2All, bins=100, histtype='step', label='data')
hist(bb.R2All, bins=100, histtype='step', label='bb')
hist(cc.R2All, bins=100, histtype='step', label='cc');
legend(fancybox=True, loc='upper left'); #Patented round corner

# <codecell>

#fix the binning #now they are align
h, e, p = hist(data.R2All, bins=100, histtype='step', label='data')
hist(bb.R2All, bins=e, histtype='step', label='bb') #notice bins=e
hist(cc.R2All, bins=e, histtype='step', label='cc');

# <markdowncell>

# ####Plotting Array Type
# Some of the data are store in an array. We need to merge them first before plotting.

# <codecell>

#for example: mass for every D candidate
#notice all the brackets
data.DMass

# <codecell>

#np.hstack flatten our array (there np.flatten but it does something else)
np.hstack(data.DMass)

# <codecell>

hist(np.hstack(data.DMass), bins=100, histtype='stepfilled', alpha=0.5);

# <markdowncell>

# ####Making Simple Cut.
# numpy support boolean indexing. Let me show you what that means.

# <codecell>

#this gives array of boolean
bb.nTracks < 10

# <codecell>

#those booleans can be used to indicate which one we want
print bb.R2All.size
print bb.R2All[bb.nTracks < 10].size
#combining cuts
print bb.R2All[(bb.nTracks> 5) & (bb.nTracks<10)].size #you need the parentheses
print bb.R2All[(bb.nTracks< 5) | (bb.nTracks>10)].size

# <codecell>

#you can store it in a variable to save time
less_track = bb.nTracks < 10
hist([bb.R2All, bb.R2All[less_track]], bins=100, histtype='step', label=['>10','<10']);
legend();

# <markdowncell>

# ####Using cuts on Array field

# <codecell>

#dmass of every event that has R2All < 0.25
hist(np.hstack(data.DMass[data.R2All<0.25]), bins=100, histtype='step'); #Select before stack;

# <markdowncell>

# ####The other way around
# 
# If you want to plot R2All of event where at least one D candidate has Mass within (1.86,1.88). This is a little more complicated. Since each element of R2All is a numpy array, we need to write a function and map them over DMass field. Here is one way to do it.

# <codecell>

@np.vectorize
def any_in_DMass(x):
    return np.any((x>1.86) & (x<1.88))

#np.vectorize is a function that returns a function.
#What this does is that it turns your function in to a vectorize version
#Putting it plainly
#g = np.vectorize(f)
#This makes g a fast(and more featureful) version of
#def g(x):
#    ret = np.array(len(x))
#    for i,this_x in enumerate(x):
#        ret[i]=f(this_x)
#    return ret
#
#The decorator is just a short hand:
#@np.vectorize
#def f(x):
#    return something
#
#is equivalent to
#f = np.vectorize(f)
#

# <codecell>

#you can use it like this
data_good_DMass = any_in_DMass(data.DMass)
data_good_DMass

# <codecell>

hist([data.R2All[data_good_DMass], data.R2All], 
    bins=100, histtype='step');

# <markdowncell>

# ####Saving Them to your favorite format with savefig.

# <codecell>

hist([bb.R2All, cc.R2All], bins=100, histtype='stepfilled', alpha=0.5, label=['bb','cc'])
title('Now they are aligned');
legend(loc='upper left');
savefig('bb_cc_r2all_comparison.pdf', bbox_inches='tight'); #bbox tight get rid of all the padding

# <markdowncell>

# ####Making Them bigger

# <codecell>

figure(figsize=(8,6), ) #creates a new figure
hist([bb.R2All, cc.R2All], bins=100, histtype='stepfilled', alpha=0.5, label=['bb','cc'])
legend(loc='upper left');

# <markdowncell>

# ####Showing multiple figure from the same cell

# <codecell>

#if you are tired to typing figsize every time
#you can set rc param http://matplotlib.org/users/customizing.html
rcParams['figure.figsize']=(8,6) #now everything after this will be big size

hist([bb.R2All, cc.R2All], bins=100, histtype='stepfilled', label=['bb','cc'], stacked=True)
legend(loc='upper left');
figure()#create new figure
hist([bb.nTracks, cc.nTracks], bins=15, histtype='step', alpha=0.5, label=['bb','cc'])
legend(loc='upper left');
#click/double click to hide the sidebar

# <markdowncell>

# ####Subplots

# <codecell>

#ROOT/matlab style and some nifty trick to save typing
mystyle= dict(bins=100, histtype='step')
subplot(221)
hist(bb.R2All, **mystyle)#python keyword argument expansion
subplot(222)
hist(bb.nTracks)
subplot(223)
hist(cc.R2All, **mystyle)
subplot(224)
hist(cc.nTracks);
#subplots_adjust(hspace=0.3) #adjust the spacing like this;

# <codecell>

#My favorite way
fig, [[topleft, topright],[bottomleft, bottomright]] = subplots(2,2, figsize=(8,6))
#it returns axes which you can draw stuff on it
topleft.hist(bb.R2All)
bottomleft.hist(cc.R2All)
topright.hist(bb.nTracks)
bottomright.hist(cc.nTracks);

# <markdowncell>

# ###Example of some useful plotting style

# <codecell>

# line plot with dots
x = np.linspace(-1, 1, 20)
y = x**2
print x, y
plot(x,y, marker='^', linestyle='none');

# <markdowncell>

# ####error bar

# <codecell>

h, e = np.histogram(bb.R2All, bins=30)
err = np.sqrt(h)
x = (e[1:]+e[:-1])/2.0
errorbar(x, h, err, ls='none', marker='o' ) #ls stands for linestyle;

# <markdowncell>

# ####fill between

# <codecell>

h, e = np.histogram(bb.R2All, bins=50)
err = np.sqrt(h)
x = (e[1:]+e[:-1])/2.0
plot(x, h) #ls stands for linestyle;
fill_between(x, h-err, h+err, alpha=0.5, color='green')

# <markdowncell>

# ####2D histogram

# <codecell>

subplot(121)
hist2d(bb.R2All,bb.thrustMagAll, bins=30);
title('bb')
colorbar()
subplot(122)
hist2d(cc.R2All,cc.thrustMagAll, bins=30, cmap='hot_r');
title('cc')
colorbar()

# <markdowncell>

# ####Scatter and Bubble Plot

# <codecell>

scatter(bb.R2All,bb.thrustMagAll, marker='.')

# <codecell>

hs = np.hstack
scatter(hs(bb.BCosSphr), hs(bb.BLegendreP2), c=hs(bb.BCosThetaT), s=hs(bb.BPFlow0)*100, alpha=0.7 )
colorbar()
xlabel('cosSphr')
ylabel('LegendreP2')
#See only big blue/red appear on the top
#This shows legendre correlates with size variable(Flow0)
#and legendre correlates with |CosThetT|

# <markdowncell>

# ##Tips
# Again the best way to figure out how to plot your stuff is to look at 
# [gallery](http://matplotlib.org/gallery.html) and find one that resemble what's in your mind

# <markdowncell>

# ###Note on importing pylab and pyplot
# 
# 
# %pylab magic already import matplotlib for us. But if you want to import it manually there are two ways either
# 
# * import a most numerical stuff(numpy numpy.random pyplot) into current namespace:
# ```
# from matplotlib.pylab import * 
# ```
# * or just using pyplot
# ```
# from matplotlib import pyplot as plt
# ```

# <markdowncell>

# ##Advance Stuff I just pull off gallery

# <codecell>

%loadpy http://matplotlib.org/mpl_examples/axes_grid/scatter_hist.py

# <codecell>

import numpy as np
import matplotlib.pyplot as plt

# the random data
x = np.random.randn(1000)
y = np.random.randn(1000)


fig = plt.figure(1, figsize=(5.5,5.5))

from mpl_toolkits.axes_grid1 import make_axes_locatable

# the scatter plot:
axScatter = plt.subplot(111)
axScatter.scatter(x, y)
axScatter.set_aspect(1.)

# create new axes on the right and on the top of the current axes
# The first argument of the new_vertical(new_horizontal) method is
# the height (width) of the axes to be created in inches.
divider = make_axes_locatable(axScatter)
axHistx = divider.append_axes("top", 1.2, pad=0.1, sharex=axScatter)
axHisty = divider.append_axes("right", 1.2, pad=0.1, sharey=axScatter)

# make some labels invisible
plt.setp(axHistx.get_xticklabels() + axHisty.get_yticklabels(),
         visible=False)

# now determine nice limits by hand:
binwidth = 0.25
xymax = np.max( [np.max(np.fabs(x)), np.max(np.fabs(y))] )
lim = ( int(xymax/binwidth) + 1) * binwidth

bins = np.arange(-lim, lim + binwidth, binwidth)
axHistx.hist(x, bins=bins)
axHisty.hist(y, bins=bins, orientation='horizontal')

# the xaxis of axHistx and yaxis of axHisty are shared with axScatter,
# thus there is no need to manually adjust the xlim and ylim of these
# axis.

#axHistx.axis["bottom"].major_ticklabels.set_visible(False)
for tl in axHistx.get_xticklabels():
    tl.set_visible(False)
axHistx.set_yticks([0, 50, 100])

#axHisty.axis["left"].major_ticklabels.set_visible(False)
for tl in axHisty.get_yticklabels():
    tl.set_visible(False)
axHisty.set_xticks([0, 50, 100])

plt.draw()
plt.show()

# <codecell>

%loadpy http://matplotlib.org/mpl_examples/mplot3d/contour3d_demo3.py

# <codecell>

from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import cm

fig = plt.figure()
ax = fig.gca(projection='3d')
X, Y, Z = axes3d.get_test_data(0.05)
ax.plot_surface(X, Y, Z, rstride=8, cstride=8, alpha=0.3)
cset = ax.contour(X, Y, Z, zdir='z', offset=-100, cmap=cm.coolwarm)
cset = ax.contour(X, Y, Z, zdir='x', offset=-40, cmap=cm.coolwarm)
cset = ax.contour(X, Y, Z, zdir='y', offset=40, cmap=cm.coolwarm)

ax.set_xlabel('X')
ax.set_xlim(-40, 40)
ax.set_ylabel('Y')
ax.set_ylim(-40, 40)
ax.set_zlabel('Z')
ax.set_zlim(-100, 100)

plt.show()


# <codecell>


