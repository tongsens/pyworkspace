__author__ = 'Administrator'

#pands plot use
def plottest():
    from pandas import Series,DataFrame
    import numpy as np
    import matplotlib.pyplot as plt
    liss = [[1,2,3,4],[4,3,2,2]]
    narr = np.array(liss).T
    s = DataFrame(narr, columns=['type0', 'type1'])
    print s
    s.plot()
    plt.show() #this is must, other pic will not show()


def selecttest():
    import matplotlib.pyplot as plt
    import numpy as np

    from sklearn.datasets import load_boston
    from sklearn.feature_selection import SelectFromModel
    from sklearn.linear_model import LassoCV

    boston = load_boston()
    X,y = boston['data'], boston['target']

    clf = LassoCV()
    sfm = SelectFromModel(clf, threshold=0.25)
    sfm.fit(X,y)
    n_features = sfm.transform(X).shape[1]

    while n_features > 2:
        sfm.threshold += 0.1
        X_transform = sfm.transform(X)
        n_features = X_transform.shape[1]

    plt.title(
    "Features selected from Boston using SelectFromModel with "
    "threshold %0.3f." % sfm.threshold)
    feature1 = X_transform[:, 0]
    feature2 = X_transform[:, 1]
    plt.plot(feature1, feature2, 'r.')
    plt.xlabel("Feature number 1")
    plt.ylabel("Feature number 2")
    plt.ylim([np.min(feature2), np.max(feature2)])
    plt.show()

if __name__ == '__main__':
    selecttest()