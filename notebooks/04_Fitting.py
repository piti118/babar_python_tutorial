# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# ##Fitting
# 
# A lot of time in our analysis we need to extract observable by fitting to a shape function. In this tutorial we will show you how to fit this in Python. The tools we will focus in this tutorial is iminuit, and probfit. They are heavily influenced by [ROOFIT](http://roofit.sourceforge.net/) and [ROOT's MINUIT](http://root.cern.ch/root/html/TMinuit.html)(and also [PyMinuit](http://code.google.com/p/pyminuit/)).
# 
# The basic idea of fitting is quite simple
# 
# 1. We have PDF and data.
# 2. We build our cost function.
# 3. We use minimizer to find shape parameters and one of those is our observable.

# <markdowncell>

# ###Minimizer
# 
# We will start this tutorial with minimizer. Minuit is hands down(for me) the best minimizer there is for HEP.
# There are couple wrapper for Minuit in Python. The one we will show here is [iminuit](https://github.com/iminuit/iminuit). It's relatively new. It might not have your favorite feature; but, you are welcome to implement it(I'll point you in the right direction).
# 
# iminuit has its own [quick start tutorial](http://nbviewer.ipython.org/urls/raw.github.com/iminuit/iminuit/master/tutorial/tutorial.ipynb) that givens you an overview of its feature and [hard core tutorial](http://nbviewer.ipython.org/urls/raw.github.com/iminuit/iminuit/master/tutorial/hard-core-tutorial.ipynb) that teach you how to complex stuff like using cython, make your own costfunction fast, and even parallel computing. We will be showing here basic feature of iminuit. If you need to do advance stuff take a look at those tutorials.

# <markdowncell>

# ####Quick Start

# <codecell>

from iminuit import Minuit, describe

# <codecell>

%load_ext inumpy

# <codecell>

#define a functino to minimize
def f(x,y,z):
    return (x-2)**2 + (y-3)**2 + (z-4)**2

# <codecell>

#iminuit relies on python introspection to read function signature
describe(f) # one of the most useful function from iminuit

# <codecell>

#notice here that it automatically knows about x,y,z
#no RooRealVar etc. needed here
m = Minuit(f)
#it warns about every little thing that might go wrong

# <codecell>

#the most frequently asked question is Does my fit converge
#also look at your console it print progress if you use print_level=2
m.migrad();

# <markdowncell>

# ####Accessing Value/Error

# <codecell>

print m.values
print m.errors
print m.fval

# <codecell>

#correlation matrix
#Only Chrome/safari gets the vertical writing mode right.
m.print_matrix() 

# <markdowncell>

# ####Checking convergence
# More details on this in the tip section at the end. Basically return value of migrad tells you a bunch of fit status.

# <codecell>

print m.migrad_ok()
print m.matrix_accurate()

# <markdowncell>

# ####minos

# <codecell>

m.minos(); #do m.minos('x') if you need just 1 of them

# <codecell>

m.merrors

# <markdowncell>

# ####Initial value, Limit, initial error, fixing

# <codecell>

m = Minuit(f, x=2, y=4, fix_y=True, limit_z=(-10,10), error_z=0.1)

# <codecell>

m.migrad();

# <markdowncell>

# ##Building cost fuction using probfit
# 
# You could write your always own cost function(see iminuit hardcore tutorial for example). But why should you. probfit provide convenience functor for you to build a simple cost function like UnbinnedLH, BinnedLH, BinnedChi2, Chi2Regression.
# 
# Let's try to fit a simple gaussian with unbinned likelihood.

# <codecell>

from math import exp, pi, sqrt
from probfit import UnbinnedLH
from iminuit import Minuit

# <codecell>

seed(0)
gdata = randn(1000)
hist(gdata,bins=100, histtype='step');

# <codecell>

#you can define your pdf manually like this
def my_gauss(x, mu, sigma):
    return exp(-0.5*(x-mu)**2/sigma**2)/(sqrt(2*pi)*sigma)

# <codecell>

#probfit use the same describe magic as iminuit
#Build your favorite cost function like this
#Notice no RooRealVar etc. It use introspection to
#find parameters
#the only requirement is that the first argument is
#in independent variable the rest are parameters
ulh = UnbinnedLH(my_gauss, gdata)
describe(ulh)

# <codecell>

m = Minuit(ulh, mu=0.2, sigma=1.5)
m.set_up(0.5) #remember up is 0.5 for likelihood and 1 for chi^2
ulh.show(m)

# <codecell>

m.migrad();
ulh.show(m)

# <markdowncell>

# ####Another way to fit gaussian
# probfit comes with a bunch of builtin functions so you don't have to write your own pdf. If you can't find your favorite function there is nothing preventing you from doing:
# ```
# def my_secret_pdf(x,y,z):
#     return secret_formula(x,y,z)
# ```
# But, it's better if you fork our project, implement it and submit a pull request.

# <codecell>

from probfit import gaussian

# <codecell>

ulh = UnbinnedLH(gaussian, gdata)
describe(ulh)

# <codecell>

m = Minuit(ulh, mean=0.2, sigma =0.3)
m.set_up(0.5)
m.migrad()
ulh.show(m)

# <markdowncell>

# ##Other Cost functions

# <markdowncell>

# ####Binned $\chi^2$
# Just a $\chi^2$ with symmetric poisson error assumption. Binned $\chi^2$ doesn't make much sense for non extended one. 

# <codecell>

from probfit import Extended, BinnedChi2
seed(0)
gdata = randn(10000)

# <codecell>

mypdf = Extended(gaussian)
describe(mypdf) # just basically N*gaussian(x,mean,sigma)

# <codecell>

bx2 = BinnedChi2(mypdf, gdata, bound=(-3,3))#create cost function
bx2.show(args={'mean':1.0, 'sigma':1.0, 'N':10000}) #another way to draw it

# <codecell>

m = Minuit(bx2, mean=1.0, sigma=1.0, N=1000.)
m.migrad()
bx2.show(m)

# <markdowncell>

# ####Binned Likelihood
# Poisson binned log likelihood with minimum subtractacted(aka likelihood ratio).

# <codecell>

from probfit import Extended, BinnedLH
seed(0)
gdata = randn(10000)

# <codecell>

mypdf = gaussian
describe(mypdf) # just basically N*gaussian(x,mean,sigma)

# <codecell>

blh = BinnedLH(mypdf, gdata, bound=(-3,3))#create cost function
#it can also do extended one if you pass it an extended pdf and pass extended=True to BinnedLH
blh.show(args={'mean':1.0, 'sigma':1.0})

# <codecell>

m = Minuit(blh, mean=1.0, sigma=1)
m.set_up(0.5)
m.migrad()
blh.show(m)

# <markdowncell>

# ####$\chi^2$ Regression
# Some time you just want a simple line fit as opposed to fitting pdf.

# <codecell>

from probfit import Chi2Regression

# <codecell>

x = linspace(-10,10,30)
y = 3*x**2 +2*x + 1
#add some noise
y = y+randn(30)*10
errorbar(x,y,10, fmt='b.')

# <codecell>

#there is a poly2 builtin but just to remind you that you can do this
def my_poly(x, a, b, c):
    return a*x**2+ b*x+ c

# <codecell>

err = np.array([10]*30)
x2reg= Chi2Regression(my_poly, x, y, error=err)
x2reg.draw(args={'a':1,'b':2,'c':3})

# <codecell>

m = Minuit(x2reg, a=1, b=2, c=3)
m.migrad()
x2reg.show(m)

# <markdowncell>

# ###Let's do some physics
# Remeber the D mass?? Let's try to fit relativistic Breit-Wigner to it.

# <codecell>

from root_numpy import root2rec

# <codecell>

data = root2rec('data/*.root')
bb = root2rec('data/B*.root')
cc = root2rec('data/cc*.root')

# <codecell>

hs = np.hstack
hist([hs(data.DMass), hs(bb.DMass), hs(cc.DMass)], bins=50, histtype='step');

# <markdowncell>

# ###Simple fit
# First lets fit bb's DMass alone with a Breit-Wigner.

# <codecell>

from probfit import UnbinnedLH, draw_compare_hist,\
                    vector_apply, Normalized, breitwigner,\
                    linear, rename, AddPdfNorm
from iminuit import Minuit

# <codecell>

bb_dmass = hs(bb.DMass)
print bb.DMass.size

# <codecell>

#you can compare them like this
draw_compare_hist(breitwigner, {'m':1.87, 'gamma':0.01}, bb_dmass, normed=True);

# <codecell>

#Our DMass is a truncated one so we need to have it normalized properly
#this is easy with Normalized functor which normalized your pdf
#this might seems a bit unusual if you never done functinal programming
#but normalize just wrap the function around and return a new function
signalpdf = Normalized(breitwigner,(1.83,1.91))

# <codecell>

ulh = UnbinnedLH(signalpdf, bb_dmass)

# <codecell>

m = Minuit(ulh, m=1.875, gamma=0.01)#I shift it on purpose
m.set_up(0.5)
ulh.show(m) #you can see it before the fit begins;

# <codecell>

%timeit -n1 -r1 m.migrad(); #we will talk about speed later;

# <codecell>

ulh.show(m) #looks good

# <codecell>

m.minos();#do m.minos('m') if you need just 1 parameter

# <codecell>

m.print_param()

# <markdowncell>

# ###More ComplexPDF
# 
# Now let's add the background and fit it. Looks like a job for linear + breitwigner.

# <codecell>

bound = (1.83,1.91)
bgpdf = Normalized(linear,bound)

# <codecell>

describe(bgpdf)

# <codecell>

#remember our breit wigner also has m argument which means different thing
describe(breitwigner)

# <codecell>

#renaming is easy
signalpdf = Normalized(rename(breitwigner,['x','mass','gamma']),(1.83,1.91))

# <codecell>

describe(signalpdf)

# <codecell>

#now we can add them
total_pdf = AddPdfNorm(signalpdf,bgpdf)
#if you want to just directly add them up with out the factor(eg. adding extended pdf)
#use AddPdf
describe(total_pdf)

# <codecell>

ulh = UnbinnedLH(total_pdf, np.hstack(data.DMass))
m = Minuit(ulh, mass=1.87, gamma=0.01, m=0., c=1, f_0=0.7)
ulh.show(m)

# <codecell>

m.migrad();

# <codecell>

ulh.show(m, parts=True)

# <codecell>

m.print_matrix()

# <codecell>

m.draw_contour('mass','f_0', show_sigma=False);
#not exactly minos contour though just a 2d scan
#Matt Bellis already signed up for this task.;

# <markdowncell>

# ####Note on complex PDF
# There is nothing preventing you from doing something like this:
# ```
# def mypdf(x,mass, gamma, m, c, f_0):
#     return brietwigner(x, mass, gamma) + f_0*(m*x+c)/normalization
# ulh=UnbinnedLH(mypdf, data)
# m=Minuit(ulh, **initial_values)
# m.migrad()
# ```
# 
# If your PDF is more complicated than what you can do with AddPDF and AddPDFNorm. It might be
# easier to write it out manually.

# <markdowncell>

# ###Simultaneous Fit
# Let try to simultaneous fit 2 gaussians with the same width but different mean.

# <codecell>

from probfit import SimultaneousFit

# <codecell>

data1 = randn(10000)
data2 = randn(10000)+10
hist([data1,data2], histtype='step', bins=100);

# <codecell>

#note here that they share the same sigma
g1 = rename(gaussian, ['x','mu1','sigma'])
g2 = rename(gaussian, ['x','mu2','sigma'])
print describe(g1)
print describe(g2)

# <codecell>

#make two likelihood and them up
ulh1 = UnbinnedLH(g1,data1)
ulh2 = UnbinnedLH(g2,data2)
sim = SimultaneousFit(ulh1,ulh2)
print describe(sim) #note the sigma merge

# <codecell>

sim.draw(args=(0.5, 1.5, 10.5))

# <codecell>

m = Minuit(sim, mu1=0.5, sigma=1.5, mu2=10.5)

# <codecell>

m.migrad();

# <codecell>

sim.show(m)

# <markdowncell>

# ####Note on simultaneous fit
# Again there is nothing preventing you from doing
# <code>
# def my_cost_function(mu1, mu2, sigma):
#     return ulh1(mu1,sigma)+ulh2(mu2.sigma)
# 
# m=Minuit(my_cost_function, **initial_values)
# m.migrad()
# <code>
# 
# If your cost function is more complex than adding them together this is the to do it.

# <markdowncell>

# ###Toy generation.
# This is invert CDF implementation (not accept reject). Large overhead but fast element-wise. Anyone want to signup for accept/reject?

# <codecell>

from probfit import gen_toy

# <codecell>

toy = gen_toy(total_pdf, 1000, (1.83,1.91), mass=1.87, gamma=0.01, c=1.045, m=-0.43, f_0=0.5, quiet=False)

# <codecell>

hist(toy, bins=100, histtype='step');

# <codecell>

ulh = UnbinnedLH(total_pdf, toy)
m = Minuit(ulh, mass=1.87, gamma=0.01, c=1.045, m=-0.43, f_0=0.5)
m.migrad();
ulh.show(m)

# <markdowncell>

# ####Tips
# 
# A lot of time you want to generate toy from fitted parameters. Retyping/Repeating yourself is not the best use of time. Use python dictionary expansion.

# <codecell>

m.fitarg

# <codecell>

toy = gen_toy(total_pdf, 1000, (1.83,1.91), quiet=False, **m.fitarg)#note the double star

# <markdowncell>

# ####Saving/Loading your toy
# using np.save

# <codecell>

np.save('mytoy.npy', toy)

# <codecell>

loaded_toy = np.load('mytoy.npy')
hist(loaded_toy, bins=100, histtype='step');

# <markdowncell>

# ###Recipe
# Something you may find useful
# 
# - Using Cython to write pdf for speed
# - Checking convergence programatically
# - Saving and reusing fit argument

# <markdowncell>

# ####Using Cython
# 
# Skip this part if you don't have cython
# 
# A much more comprehensive example of how to use cython is provided in iminuit [hard core tutorial](http://nbviewer.ipython.org/urls/raw.github.com/iminuit/iminuit/master/tutorial/hard-core-tutorial.ipynb). We will show a simple example here.

# <codecell>

%load_ext cythonmagic

# <codecell>

%%cython
from libc.math cimport sqrt
cimport cython

cdef double pi = 3.14159265358979323846264338327

@cython.embedsignature #you need this or experimental @cython.binding.
cpdef double cython_bw(double x, double m, double gamma):
    cdef double mm = m*m
    cdef double xm = x*x-mm
    cdef double gg = gamma*gamma
    cdef double s = sqrt(mm*(mm+gg))
    cdef double N = (2*sqrt(2)/pi)*m*gamma*s/sqrt(mm+s)
    return N/(xm*xm+mm*gg)

# <codecell>

cython_bw(1,2,3)

# <codecell>

from probfit import describe
describe(cython_bw)

# <codecell>

ulh = UnbinnedLH(cython_bw, bb_dmass)

# <codecell>

m = Minuit(ulh, m=1.875, gamma = 0.01)
ulh.show(m)

# <codecell>

%%timeit -r1 -n1 m.migrad()

# <markdowncell>

# ####Building Cost Functions Manually
# 
# See iminuit hardcore tutorial.

# <markdowncell>

# ####Checking convergence programatically

# <codecell>

status, param = m.migrad()

# <codecell>

print status.has_covariance
print status.is_valid

# <codecell>

#or an umbrella call
m.migrad_ok()

# <codecell>

#minos
results = m.minos('m')
print results['m']
print results['m'].upper_valid
print results['m'].lower_valid

# <markdowncell>

# ####Saving/Reuse fit argument
# Some time we want to resue fitting argument.

# <codecell>

m.fitarg

# <codecell>

old_fitarg = m.fitarg
ulh2 = UnbinnedLH(cython_bw, bb_dmass)
m2 = Minuit(ulh2, **old_fitarg)

# <codecell>

m2.print_param()

# <codecell>

#since fitarg is just a dictionary you can dump it via pickle
import pickle
out = open('my_fitarg.pck','w')
pickle.dump(old_fitarg,out)
out.close()

# <codecell>

fin = open('my_fitarg.pck','r')
loaded_fitarg = pickle.load(fin)
fin.close()

# <codecell>

print loaded_fitarg

# <codecell>

m3 = Minuit(ulh2, **loaded_fitarg)

# <codecell>

m3.migrad();

