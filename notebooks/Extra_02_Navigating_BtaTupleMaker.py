# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from root_numpy import root2rec

# <markdowncell>

# Suppose we want to plot B mass vs D Mass for all candidates. They are associated via Bd1Idx

# <codecell>

bb = root2rec('data/B0B0bar-BtoDpi-all.root')

# <codecell>

bb.dtype

# <codecell>

#most obvious way but not very pleasant
#you can clean it up but you get the idea

def process_event(data):
    idx_Bd1Idx = data.dtype.names.index('Bd1Idx')
    idx_Dmass = data.dtype.names.index('DMass')
    idx_Bmass = data.dtype.names.index('BSphrROE') #hmmm i don't have BMass?
    
    result = np.zeros(len(data), dtype=[('x','O'),('y','O')])
    for idata in xrange(len(data)):
        tmp_B = []
        tmp_D = []
        for i_B in xrange(len(data[idata][idx_Bd1Idx])):
            Bd1Idx = data[idata][idx_Bd1Idx][i_B]
            if Bd1Idx >= 0 and Bd1Idx < len(data[idata][idx_Dmass]):
                BMass = data[idata][idx_Bmass][i_B]
                DMass = data[idata][idx_Dmass][Bd1Idx]
                tmp_D.append(DMass)
                tmp_B.append(BMass)
        result[idata]= tmp_B, tmp_D
        
    return result

# <codecell>

%timeit process_event(bb)

# <codecell>

tmp = process_event(bb).view(np.recarray)
print tmp.x
hist2d(hstack(tmp.x), hstack(tmp.y));

# <markdowncell>

# A tad smarter way

# <codecell>

#a bit smarter way
def do_something(sphr, idx, Dmass, nD):
    ret = np.empty(len(sphr),dtype=[('x','O'),('y','O')])
    for i_data in xrange(len(sphr)):
        good_idx = (idx[i_data] >=0) & (idx[i_data] < nD[i_data])
        x = sphr[i_data][good_idx]
        y = Dmass[i_data][idx[i_data][good_idx]]
        ret[i_data]= x,y
    return ret

# <codecell>

%timeit do_something(bb.BSphrROE, bb.Bd1Idx, bb.DMass, bb.nD)

# <codecell>

tmp = do_something(bb.BSphrROE, bb.Bd1Idx, bb.DMass, bb.nD).view(np.recarray)
print tmp.x
hist2d(hstack(tmp.x), hstack(tmp.y));

# <markdowncell>

# Generic way with blockwise_inner_join

# <codecell>

from root_numpy import blockwise_inner_join

# <codecell>

#data to two block
#left block is scalar sl and array al
#right block is ar
#two types of foreign key fk and s_fk 
#notice some foreign keys are invalid(-1) those are discarded
test_data = np.array([
                    (1.0,np.array([11,12,13]),np.array([1,0,1]),0,np.array([1,2,3])),
                    (2.0,np.array([21,22,23]),np.array([-1,2,-1]),1,np.array([31,32,33]))
                    ],
                    dtype=[('sl',np.float),('al','O'),('fk','O'),('s_fk',np.int),('ar','O')])

# <codecell>

blockwise_inner_join(test_data, ['sl','al'], test_data['fk'], ['ar'] )

# <codecell>

blockwise_inner_join(test_data, ['sl','al'], test_data['fk'], ['ar'], force_repeat=['al'])

# <codecell>

blockwise_inner_join(test_data, ['sl','al'], test_data['s_fk'], ['ar'] )

# <codecell>

Bblock = [n for n in bb.dtype.names if n.startswith('B')]
Dblock = [n for n in bb.dtype.names if n.startswith('D')]
Kblock = [n for n in bb.dtype.names if n.startswith('K')]

# <codecell>

%timeit a = blockwise_inner_join(bb,Bblock,bb.Bd1Idx,Dblock).view(np.recarray)

# <codecell>

a = blockwise_inner_join(bb,Bblock,bb.Bd1Idx,Dblock).view(np.recarray)
print a[0]
print a.dtype
hist2d(a.BSphrROE,a.DMass);

# <markdowncell>

# If you want to emulate multiple join, say we want to B -> D -> K, do this:

# <codecell>

first_join = blockwise_inner_join(bb,Bblock+Kblock,bb.Bd1Idx,Dblock, force_repeat=Kblock).view(np.recarray)
second_join = blockwise_inner_join(first_join,Bblock+Dblock, first_join.Dd1Idx, Kblock).view(np.recarray)

# <codecell>

print len(second_join)
print second_join.dtype

# <codecell>

second_join[0]

# <codecell>


