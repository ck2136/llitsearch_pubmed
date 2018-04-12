#!/usr/bin/python3.6

"""
This code will visualize the LDA distributions (i.e. topic and terms).
Author: C.K.
Created: 4/11/2018
Modified: 4/11/2018
"""


def gensim_output(modelfile, corpusfile, dictionaryfile):
    """ Displaying gensim toppic models """
    # load packages
    import gensim
    from gensim import corpora

    # Load files from gensim_modeling
    corpus = corpora.MmCorpus(corpusfile)
    dictionary = corpora.Dictionary.load(dictionaryfile)
    myldamodel = gensim.models.ldamodel.LdaModel.load(modelfile)

    # interactive visualization
    import pyLDAvis
    import pyLDAvis.gensim
    vis = pyLDAvis.gensim.prepare(myldamodel, corpus, dictionary)
    pyLDAvis.show(vis)


if __name__ == "__main__":
    gensim_output(modelfile='../data/asthma_lit_abs.mod',
                  corpusfile='../data/asthma_lit_abs.mm',
                  dictionaryfile='../data/asthma_lit_abs.dict')
