# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=2>

# Basic Python

# <markdowncell>

# This is just to give you a glimpse of what Python can do.
# We select only subset of the feature we think will be useful for doing analysis.
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
print l #[1, 2, 3, 4, 5, 6, 7]
print l[2] #3
print len(l) # list length
print l[-1] #7 negative index works from the back (-1)
l2 = [] #want an empty list?
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
print d #{'a': 1, 'c': 100, 'b': 10}
d2 = dict(a=2, b=20, c=200) #using named argument
print d2 #{'a': 2, 'c': 200, 'b': 20}
d3 = dict([('a', 3),('b', 30),('c', 300)]) #list of tuples
print d3 #{'a': 3, 'c': 300, 'b': 30}
d4 = {x:2*x for x in range(10)}#comprehension (key doesn't have to be string)
print d4 #{0: 0, 1: 2, 2: 4, 3: 6, 4: 8, 5: 10, 6: 12, 7: 14, 8: 16, 9: 18}
d5 = {} #empty dict
print d5 #{}

# <codecell>

print d['a'] #access
print len(d) #count element
d['d'] = 1000#insert
print d #{'a': 1, 'c': 100, 'b': 10, 'd': 1000}
del d['c']#remove
print d #{'a': 1, 'b': 10, 'd': 10}
print 'c' in d #keyexists?

# <codecell>

#use dictionary in comprehension
#d.items() return generator which gives tuple 
#k,v in d.items() does tuple expansion in disguise
new_d = {k:2*v for k,v in d.items()}
print new_d #{'a': 2, 'b': 20, 'd': 20}

# <markdowncell>

# Set
# ---
# Binary tree-ish

# <codecell>

s = {1,2,3,4,5,6}
print s
s2 = set([4, 5, 6, 7, 8, 9, 9, 9, 9]) #from a list
#duplicated element is ignored
print s2

# <codecell>

#membership this is O(log(n))
print 3 in s
print 10 in s
print 11 not in s

# <codecell>

print s | s2 #union
print s & s2 #intersection
print s - s2 #differece
print s ^ s2 #symmetric differnce
print {2,3,4} <= s #subset
print s >= {2,3,4} #superset

# <codecell>

#insert
s.update([10,11,12])
print s
print 11 in s

# <markdowncell>

# ##Control Flow
# ###if else elif
# Indentation in python is meaningful. There is "NO" bracket scoping in python.
# 
# Recommended indentation is 4 spaces not Tab. Tab works but not recommended
# Set your text editor to soft tab. [PEP8](http://www.python.org/dev/peps/pep-0008/) which list all the
# recommended style: space, comma, indentation, new line, comment etc. Fun Read.

# <codecell>

x = 20
if x>10: #colon
    print 'greater than 10'#don't for get the indentation
elif x>5: #parenthesis is not really needed
    print 'greater than 5'
else:
    print 'not greater than 10'
x+=1#continue your execution with lower indentation
print x

# <codecell>

#shorthand if
y = 'oh yes' if x>100 else 'oh no' #no colon
print y

# <codecell>

#since indentation matters sometime we don't need any statement
if x>10:
    print 'yes'
else:
    pass #pass keywoard means do nothing
x+=1
print x

# <codecell>

#why is there no bracket??
from __future__ import braces #easter egg

# <markdowncell>

# ###For loop, While loop, Generator, Iterable
# 
# There is actually no `for(i=0;i<10;i++)` in python. `list` is an example of iterable.

# <codecell>

#iterate over list
for i in range(5): #not recommended use xrange instead
    print i#again indentation is meaningful

# <markdowncell>

# ####Generator
# In previous example, we use range. But ``range`` will be evaluated 
# eagerly and put ``[1,2,3,4,5]`` in the memory
# 
# This is bad if you try to loop over large number. `for i in range(100000)` will put 100000 numbers in to the memory first. This is very inefficient since you use each one of them once.
# 
# To fix this we use generator instead. As far as we are concern they are
# object that spit out number only when ask and doesn't keep it's previous
# states which means no access by index nor going backward. You can read more about it from [python wiki](http://wiki.python.org/moin/Generators). Or just google for python `yield` keyword.
# 
# Long story short just use `for i in xrange(5)` instead

# <codecell>

#Lazy programming 
for i in xrange(5):
    print i

# <codecell>

#looping the list
l = ['a','b','c']
for x in l:
    print x

# <codecell>

#you can build your own generator too
l = [1,2,3,4]
#(2*y for y in l) is a generator that split out 2*y
#for every element in l
#not really a good way to write it but just to show it
for x in (2*y for y in l):#notice the brackets
    print x

# <codecell>

#if you need index
for i,x in enumerate(l):
    print i,x

# <codecell>

#looping dictionary
d = {'a':1,'b':10,'c':100}
#items() returns a generator which return tuple
#k,v in d.items() is tuple expansion in disguise
for k,v in d.items():
    print k,v

# <codecell>

#looping over multiple list together
lx = [1,2,3]
ly = [x+1 for x in l]
print l,l2
for x,y in zip(lx,ly): #there is also itertools.izip that does generator
    print x,y

# <codecell>

#you can 

# <codecell>

x = 0
while x<5:
    print x
    x+=1

# <markdowncell>

# ####See Also
# For more complex looping you can look at [itertools](http://docs.python.org/2/library/itertools.html)

# <markdowncell>

# ###Function
# Functions in python is a first class object(except in a very few cases).

# <codecell>

def f(x, y):
    return x+y

# <codecell>

#Bonus argument expansion

# <codecell>


# <codecell>


# <markdowncell>

# ###Classes, Object etc
# Think about it as pointer to object in C.

# <codecell>

a = [1,2,3]

# <codecell>

id(a)

# <codecell>

b = a[:]

# <codecell>

id(b)

# <codecell>


