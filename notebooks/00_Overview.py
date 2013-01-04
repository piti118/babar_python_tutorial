# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# ##Overview
# 
# This notebook serves two purposes: testing out your installation and giving you a rough idea of what will be covered in this tutorial.

# <markdowncell>

# ###Basic python

# <markdowncell>

# ####hello world

# <codecell>

print 'hello world'

# <markdowncell>

# ####And others

# <codecell>

1+1

# <codecell>

for i in range(10):
    print 'loop', i

# <markdowncell>

# ####Reading ROOT FILE

# <codecell>

from root_numpy import root2rec

# <codecell>

bb = root2rec('data/B*.root') #yep that simple
cc = root2rec('data/cc-BtoDpi-all.root')

# <markdowncell>

# ####And plotting

# <codecell>

hist([bb.R2All, cc.R2All], bins=100, histtype='stepfilled', 
     color=['red','green'], alpha=0.5, label=[r'$B\bar{B}$',r'$c\bar{c}$']);
legend().get_frame().set_alpha(0.5)
title(r'My Amazing plot of R2All $\alpha$ $\beta$', fontsize='xx-large' )
xlabel('R2All')

# <markdowncell>

# ####Multivariate analysis

# <codecell>

from sklearn import tree

# <codecell>

X_sig= np.random.multivariate_normal(mean=[0.0, 0.0], cov=[ [1,0.5], [0.5,1] ], size= 1000)
X_bkg= np.random.rand(1000,2)
X_bkg= (X_bkg-0.5)*10
scatter(X_bkg[:,0], X_bkg[:,1], color='b', alpha=0.4)
scatter(X_sig[:,0], X_sig[:,1], color='g', alpha=0.4)

# <codecell>

features = np.concatenate([X_sig, X_bkg])
classes = np.array( [0]*len(X_bkg) + [1]*len(X_sig) )

# <codecell>

clf = tree.DecisionTreeClassifier(min_samples_leaf=10)

# <codecell>

clf.fit(features, classes)

# <codecell>

prediction = clf.predict(features)
print prediction.shape
print features[:,0].shape

# <codecell>

sig = features[prediction==1]
bg = features[prediction==0]
scatter(sig[:,0],sig[:,1],color='b', alpha=0.4)
scatter(bg[:,0],bg[:,1],color='g', alpha=0.4)
title('Prediction');

# <codecell>

scatter(X_bkg[:,0], X_bkg[:,1], color='b', alpha=0.4)
scatter(X_sig[:,0], X_sig[:,1], color='g', alpha=0.4)
title('Original');

# <markdowncell>

# ####Fitting

# <codecell>

from iminuit import Minuit
from probfit import UnbinnedLH, gaussian

# <codecell>

data = randn(10000)
hist(data, bins=100, histtype='step');

# <codecell>

ulh = UnbinnedLH(gaussian, data)
ulh.draw(args=dict(mean=1.2, sigma=0.7))

# <codecell>

m = Minuit(ulh, mean=1.2, sigma=0.7)

# <codecell>

m.migrad()

# <codecell>

print m.values
print m.errors
ulh.draw(m)

