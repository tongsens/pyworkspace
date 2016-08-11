__author__ = 'Administrator'

import sklearn.feature_extraction
import pandas as pd
import numpy as np
import tldextract
import math
from collections import Counter
import matplotlib.pyplot as plt
import pylab
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

def domain_extract(uri):
    ext = tldextract.extract(uri)
    if (not ext.suffix):
        return np.nan
    else:
        return ext.domain

def read_alexa():
    alexa_dataframe = pd.read_csv('alexa_100k.csv', names=['rank', 'uri'], header=None, encoding='utf-8')
    alexa_dataframe['domain'] = [domain_extract(uri) for uri in alexa_dataframe['uri']]
    del alexa_dataframe['rank']
    del alexa_dataframe['uri']
    alexa_dataframe = alexa_dataframe.dropna()
    alexa_dataframe = alexa_dataframe.drop_duplicates()
    alexa_dataframe['class'] = 'legit'
    alexa_dataframe = alexa_dataframe.reindex(np.random.permutation(alexa_dataframe.index))
    return alexa_dataframe

def read_dga():
    dga_dataframe = pd.read_csv('dga_domains.txt', names=['raw_domain'], header=None, encoding='utf-8')
    dga_dataframe['domain'] = dga_dataframe.applymap(lambda x:x.split('.')[0].strip().lower())
    del dga_dataframe['raw_domain']
    dga_dataframe = dga_dataframe.dropna()
    dga_dataframe = dga_dataframe.drop_duplicates()
    dga_dataframe['class'] = 'dga'
    return dga_dataframe

def entroy(s):
    p, lns = Counter(s), float(len(s))
    return -sum(count/lns*math.log(count/lns,2) for count in p.values())

def plot_cm(cm, labels):

    # Compute percentanges
    percent = (cm*100.0)/np.array(np.matrix(cm.sum(axis=1)).T)  # Derp, I'm sure there's a better way

    print 'Confusion Matrix Stats'
    for i, label_i in enumerate(labels):
        for j, label_j in enumerate(labels):
            print "%s/%s: %.2f%% (%d/%d)" % (label_i, label_j, (percent[i][j]), cm[i][j], cm[i].sum())

    # Show confusion matrix
    # Thanks kermit666 from stackoverflow :)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(b=False)
    cax = ax.matshow(percent, cmap='coolwarm')
    pylab.title('Confusion matrix of the classifier')
    fig.colorbar(cax)
    ax.set_xticklabels([''] + labels)
    ax.set_yticklabels([''] + labels)
    pylab.xlabel('Predicted')
    pylab.ylabel('True')
    pylab.show()

def tray_test(all_domains):
    global clf
    not_weird = all_domains[all_domains['class']!='weird']
    X = not_weird.as_matrix(['length', 'entropy', 'aleax_grams', 'word_grams'])
    y = np.array(not_weird['class'].tolist())
    import sklearn.ensemble
    import sklearn.cross_validation
    from sklearn.cross_validation import train_test_split
    from sklearn.metrics import confusion_matrix
    clf = sklearn.ensemble.RandomForestClassifier(n_estimators=20)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    labels = ['legit', 'dga']
    cm = confusion_matrix(y_test, y_pred, labels)
    #plot_cm(cm, labels)



def ngrams(alexa_dataframe, all_domains):
    global alexa_vc
    global alexa_counts
    global dict_vc
    global dict_counts
    alexa_vc = sklearn.feature_extraction.text.CountVectorizer(analyzer='char', ngram_range=(3,5), min_df=1e-4, max_df=1.0)
    counts_matrix = alexa_vc.fit_transform(alexa_dataframe['domain'])
    alexa_counts = np.log10(counts_matrix.sum(axis=0).getA1())

    word_dataframe = pd.read_csv('words.txt', names=['word'], header=None, dtype={'word':np.str}, encoding='utf-8')
    word_dataframe = word_dataframe[word_dataframe['word'].map(lambda x:str(x).isalpha())]
    word_dataframe = word_dataframe.applymap(lambda x:str(x).strip().lower())
    word_dataframe = word_dataframe.dropna()
    word_dataframe = word_dataframe.drop_duplicates()
    dict_vc = sklearn.feature_extraction.text.CountVectorizer(analyzer='char', ngram_range=(3,5), min_df=1e-5, max_df=1.0)
    counts_matrix = dict_vc.fit_transform(word_dataframe['word'])
    dict_counts = np.log10(counts_matrix.sum(axis=0).getA1())

    all_domains['aleax_grams'] = alexa_counts*alexa_vc.transform(all_domains['domain']).T
    all_domains['word_grams'] = dict_counts*dict_vc.transform(all_domains['domain']).T
    all_domains['diff'] = all_domains['aleax_grams'] - all_domains['word_grams']
    return all_domains

def parse_data():
    alexa_dataframe = read_alexa()
    dga_dataframe = read_dga()
    all_domains = pd.concat([alexa_dataframe, dga_dataframe], ignore_index=True)
    all_domains['entropy'] = [entroy(x) for x in all_domains['domain']]
    all_domains['length'] = [len(x) for x in all_domains['domain']]
    all_domains = all_domains[all_domains['length']>6]
    all_domains = ngrams(alexa_dataframe, all_domains)
    weird_cond = (all_domains['class']=='legit') & (all_domains['word_grams']<3) & (all_domains['aleax_grams']<2)
    all_domains.loc[weird_cond, 'class'] = 'weird'
    return all_domains

def test_url(domain,clf):
    if len(domain)<7:
        return 'legit'
    _alexa_match = alexa_counts * alexa_vc.transform([domain]).T  # Woot matrix multiply and transpose Woo Hoo!
    _dict_match = dict_counts * dict_vc.transform([domain]).T
    _X = [len(domain), entroy(domain), _alexa_match, _dict_match]
    #print '%s : %s' % (domain, clf.predict(_X)[0])
    return clf.predict(_X)[0]

def mydomain_extract(uri):
    ext = tldextract.extract(uri)
    if len(ext.domain)<3:
        if ext.subdomain:
            return ext.subdomain
        else:
            return ext.domain
    else:
        return ext.domain

def process_url():
    data_frame = pd.read_csv('url.csv', names=['idx','url'], header=None, encoding='utf-8')
    del data_frame['idx']
    data_frame['domain'] = [mydomain_extract(data) for data in data_frame['url']]
    data_frame =data_frame.dropna()
    data_frame = data_frame.drop_duplicates()
    data_frame['class'] = [test_url(domain, clf) for domain in data_frame['domain']]
    print data_frame.head(50)

if __name__ == '__main__':
    all_domains = parse_data()
    tray_test(all_domains)
    process_url()

