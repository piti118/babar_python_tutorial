# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=2>

# Basic Python

# <markdowncell>

# This is just to give you a glimpse of what Python can do.
# We select only subset of the feature we think will be useful for us.
# 
# For more comprehensive book see http://www.greenteapress.com/thinkpython/html/index.html
# 
# To go through this tutorial press ``shift+enter`` to execute the current cell and go to
# the next cell.

# <headingcell level=3>

# Hello World

# <codecell>

#press shift+enter to execute this
print 'Hello world'

# <codecell>

#ipython automatically show representation of the return value of the last command
1+1

# <headingcell level=3>

# Data Type(Usual Stuff)

# <codecell>

x = 1 #integer
y = 2.0 #float
t = True #boolean (False)
s = 'hello' #string
s2 = "world" #double quotes works too
n=None #Null like variable None.

# <codecell>

print x+y #you can refer to previously assigned variable.

# <codecell>

s+' '+s2

# <codecell>

#boolean operations
x>1 and (y>=3 or not t) and not s=='hello' and n is None

# <codecell>

#Bonus: The only language I know that can do this
0<x<10

# <markdowncell>

# ##List, Set, Tuple, Dictionary, Generator

# <markdowncell>

# List
# ----
# Think of it as std::vector++

# <codecell>

l = [1, 2, 3, 4, 5, 6, 7]
print l
print l[2] #3
print l[-1] #7 negative index works from the back (-1)
#want an empty list?
l2 = []
print l2

# <codecell>

#doesn't really need hold the same type
#but don't recommend. You will just get confused
bad_list = ['dog','cat',1,1.234]

# <codecell>

l[1] = 10 #assignment
l

# <codecell>

l.append(999) #append list
l

# <codecell>

#can be created from list com
l.sort() #sort
l

# <codecell>

#searching O(N) use set for O(log(N))
10 in l

# <codecell>

11 not in l

# <codecell>

#useful list function
range(10) #build it all in memory

# <codecell>

#list comprehension
#we will get to for loop later but for simple one
#list comprehension is much more readable
my_list = [2*x for x in l]
print my_list
my_list = [ (2*x,x) for x in range(10)]
print my_list
my_list = [3*x for x in range(10) if x%2==0]
print my_list

# <markdowncell>

# Tuple
# -----
# Think of it as immutable list

# <codecell>

tu = (1,2,3) #tuple immutable list
print tu
tu2 = tuple(l) #convert list to tuple
print tu2
tu3 = 4,5,6 #parenthesis is actually optional but makes it more readable
print tu3

# <codecell>

#access
tu[1]

# <codecell>

#tuple expansion
x, y, z = tu
print x #1
print y #2
print z #3
print x, y, z #you can use tuple in print statement too

x, y, z = 10, 20, 30#parenthesis is actually optional
print z, y, x #any order

# <codecell>

#useful for returning multiple values
def f(x,y):
    return x+y, x-y #parenthesis is implied
a, b = f(10,5)
print a #15
print b #5
print a, b #works too

# <markdowncell>

# Dictionary
# ----------
# 
# Think of it as std::map - ish

# <codecell>

d = {'a':1, 'b':10, 'c':100}
print d
d2 = dict(a=2, b=20, c=200) #using named argument
print d2
d3 = dict([('a', 3),('b', 30),('c', 300)]) #list of tuples
print d3
d4 = {x:2*x for x in range(10)}#comprehension (key doesn't have to be string)
print d4
d5 = {} #empty dict
print d5

# <codecell>

print d['a'] #access
d['d'] = 10#insert
print d
del d['c']#remove
print d

# <codecell>

#use dictionary in comprehension
#d.items() return generator which gives tuple 
#k,v in d.items() does tuple expansion in disguise
new_d = {k:2*v for k,v in d.items()}
print new_d

# <markdowncell>

# Set
# ---
# Binary tree-ish

# <codecell>


# <codecell>


# <codecell>


# <headingcell level=3>

# Control Flow: Generator, For, if else elif, while

# <codecell>


# <codecell>


# <codecell>


# <headingcell level=3>

# List/Dict/etc Comprehension

# <codecell>


# <headingcell level=3>

# Function

# <markdowncell>

# Functions are first class object too.

# <codecell>


# <codecell>

#Bonus argument expansion

# <codecell>


# <codecell>


# <headingcell level=3>

# Classes

# <codecell>

a = [1,2,3]

# <codecell>

id(a)

# <codecell>

b = a[:]

# <codecell>

id(b)

# <codecell>


