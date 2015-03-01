#!/usr/bin/env python

import numpy as np
import pandas as pd
import pandas.compat as compat

import sklearn.datasets as datasets
import sklearn.feature_extraction as fe

import expandas as expd
import expandas.util.testing as tm


class TestFeatureExtraction(tm.TestCase):

    def test_objectmapper(self):
        df = expd.ModelFrame([])
        self.assertIs(df.feature_extraction.DictVectorizer, fe.DictVectorizer)
        self.assertIs(df.feature_extraction.FeatureHasher, fe.FeatureHasher)

        self.assertIs(df.feature_extraction.image.img_to_graph, fe.image.img_to_graph)
        self.assertIs(df.feature_extraction.image.grid_to_graph, fe.image.grid_to_graph)
        self.assertIs(df.feature_extraction.image.extract_patches_2d, fe.image.extract_patches_2d)
        self.assertIs(df.feature_extraction.image.reconstruct_from_patches_2d,
                      fe.image.reconstruct_from_patches_2d)
        self.assertIs(df.feature_extraction.image.PatchExtractor, fe.image.PatchExtractor)

        self.assertIs(df.feature_extraction.text.CountVectorizer, fe.text.CountVectorizer)
        self.assertIs(df.feature_extraction.text.HashingVectorizer, fe.text.HashingVectorizer)
        self.assertIs(df.feature_extraction.text.TfidfTransformer, fe.text.TfidfTransformer)
        self.assertIs(df.feature_extraction.text.TfidfVectorizer, fe.text.TfidfVectorizer)


if __name__ == '__main__':
    import nose
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'],
                   exit=False)