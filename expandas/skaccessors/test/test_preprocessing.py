#!/usr/bin/env python

import numpy as np
import pandas as pd
import pandas.compat as compat

import sklearn.datasets as datasets
import sklearn.preprocessing as pp

import expandas as expd
import expandas.util.testing as tm


class TestPreprocessing(tm.TestCase):

    def test_objectmapper(self):
        df = expd.ModelFrame([])
        self.assertIs(df.preprocessing.Binarizer, pp.Binarizer)
        self.assertIs(df.preprocessing.Imputer, pp.Imputer)
        self.assertIs(df.preprocessing.KernelCenterer, pp.KernelCenterer)
        self.assertIs(df.preprocessing.LabelBinarizer, pp.LabelBinarizer)
        self.assertIs(df.preprocessing.LabelEncoder, pp.LabelEncoder)
        self.assertIs(df.preprocessing.MultiLabelBinarizer, pp.MultiLabelBinarizer)
        self.assertIs(df.preprocessing.MinMaxScaler, pp.MinMaxScaler)
        self.assertIs(df.preprocessing.Normalizer, pp.Normalizer)
        self.assertIs(df.preprocessing.OneHotEncoder, pp.OneHotEncoder)
        self.assertIs(df.preprocessing.StandardScaler, pp.StandardScaler)
        self.assertIs(df.preprocessing.PolynomialFeatures, pp.PolynomialFeatures)

    def test_add_dummy_feature(self):
        iris = datasets.load_iris()
        df = expd.ModelFrame(iris)

        result = df.preprocessing.add_dummy_feature()
        expected = pp.add_dummy_feature(iris.data)

        self.assertTrue(isinstance(result, expd.ModelFrame))
        self.assert_numpy_array_almost_equal(result.data.values, expected)

        result = df.preprocessing.add_dummy_feature(value=2)
        expected = pp.add_dummy_feature(iris.data, value=2)

        self.assertTrue(isinstance(result, expd.ModelFrame))
        self.assert_numpy_array_almost_equal(result.data.values, expected)
        self.assert_index_equal(result.columns[1:], df.data.columns)

        s = df['sepal length (cm)']
        self.assertTrue(isinstance(s, expd.ModelSeries))
        result = s.preprocessing.add_dummy_feature()
        expected = pp.add_dummy_feature(iris.data[:, [0]])

        self.assertTrue(isinstance(result, expd.ModelFrame))
        self.assert_numpy_array_almost_equal(result.values, expected)
        self.assertEqual(result.columns[1], 'sepal length (cm)')

    def test_binarize(self):
        iris = datasets.load_iris()
        df = expd.ModelFrame(iris)

        result = df.preprocessing.binarize()
        expected = pp.binarize(iris.data)

        self.assertTrue(isinstance(result, expd.ModelFrame))
        self.assert_numpy_array_almost_equal(result.data.values, expected)
        self.assert_index_equal(result.columns, df.data.columns)

        result = df.preprocessing.binarize(threshold=5)
        expected = pp.binarize(iris.data, threshold=5)

        self.assertTrue(isinstance(result, expd.ModelFrame))
        self.assert_numpy_array_almost_equal(result.data.values, expected)
        self.assert_index_equal(result.columns, df.data.columns)

        s = df['sepal length (cm)']
        self.assertTrue(isinstance(s, expd.ModelSeries))
        result = s.preprocessing.binarize()
        expected = pp.binarize(iris.data[:, 0])

        self.assertTrue(isinstance(result, expd.ModelSeries))
        self.assert_numpy_array_almost_equal(result.values, expected)
        self.assertEqual(result.name, 'sepal length (cm)')

        result = s.preprocessing.binarize(threshold=6)
        expected = pp.binarize(iris.data[:, 0], threshold=6)

        self.assertTrue(isinstance(result, expd.ModelSeries))
        self.assert_numpy_array_almost_equal(result.values, expected)
        self.assertEqual(result.name, 'sepal length (cm)')

    def test_normalize(self):
        iris = datasets.load_iris()
        df = expd.ModelFrame(iris)

        result = df.preprocessing.normalize()
        expected = pp.normalize(iris.data)

        self.assertTrue(isinstance(result, expd.ModelFrame))
        self.assert_numpy_array_almost_equal(result.data.values, expected)
        self.assert_index_equal(result.columns, df.data.columns)

        s = df['sepal length (cm)']
        self.assertTrue(isinstance(s, expd.ModelSeries))
        result = s.preprocessing.normalize()
        expected = pp.normalize(np.atleast_2d(iris.data[:, 0]))[0]

        self.assertTrue(isinstance(result, expd.ModelSeries))
        self.assert_numpy_array_almost_equal(result.values, expected)
        self.assertEqual(result.name, 'sepal length (cm)')

    def test_normalize_abbr(self):
        iris = datasets.load_iris()
        df = expd.ModelFrame(iris)

        result = df.pp.normalize()
        expected = pp.normalize(iris.data)

        self.assertTrue(isinstance(result, expd.ModelFrame))
        self.assert_numpy_array_almost_equal(result.data.values, expected)
        self.assert_index_equal(result.columns, df.data.columns)

        s = df['sepal length (cm)']
        self.assertTrue(isinstance(s, expd.ModelSeries))
        result = s.pp.normalize()
        expected = pp.normalize(np.atleast_2d(iris.data[:, 0]))[0]

        self.assertTrue(isinstance(result, expd.ModelSeries))
        self.assert_numpy_array_almost_equal(result.values, expected)
        self.assertEqual(result.name, 'sepal length (cm)')

    def test_scale(self):
        iris = datasets.load_iris()
        df = expd.ModelFrame(iris)

        result = df.preprocessing.scale()
        expected = pp.scale(iris.data)

        self.assertTrue(isinstance(result, expd.ModelFrame))
        self.assert_numpy_array_almost_equal(result.data.values, expected)
        self.assert_index_equal(result.columns, df.data.columns)

        s = df['sepal length (cm)']
        self.assertTrue(isinstance(s, expd.ModelSeries))
        result = s.preprocessing.scale()
        expected = pp.scale(np.atleast_2d(iris.data[:, 0]))[0]

        self.assertTrue(isinstance(result, expd.ModelSeries))
        self.assert_numpy_array_almost_equal(result.values, expected)
        self.assertEqual(result.name, 'sepal length (cm)')

    def test_preprocessing_assignment(self):
        iris = datasets.load_iris()
        df = expd.ModelFrame(iris)

        original_columns = df.data.columns
        df['sepal length (cm)'] = df['sepal length (cm)'].preprocessing.binarize(threshold=6)
        self.assertTrue(isinstance(df, expd.ModelFrame))
        binarized = pp.binarize(np.atleast_2d(iris.data[:, 0]), threshold=6)
        expected = np.hstack([binarized.T, iris.data[:, 1:]])
        self.assert_numpy_array_almost_equal(df.data.values, expected)
        self.assert_index_equal(df.data.columns, original_columns)

        # recreate data
        iris = datasets.load_iris()
        df = expd.ModelFrame(iris)

        target_columns = ['sepal length (cm)', 'sepal width (cm)']
        df[target_columns] = df[target_columns].preprocessing.binarize(threshold=6)
        self.assertTrue(isinstance(df, expd.ModelFrame))
        binarized = pp.binarize(iris.data[:, 0:2], threshold=6)
        expected = np.hstack([binarized, iris.data[:, 2:]])
        self.assert_numpy_array_almost_equal(df.data.values, expected)
        self.assert_index_equal(df.data.columns, original_columns)

    def test_transform(self):
        iris = datasets.load_iris()
        df = expd.ModelFrame(iris)

        models = ['Binarizer', 'Imputer', 'KernelCenterer',
                  'Normalizer', 'StandardScaler']
        for model in models:
            mod1 = getattr(df.preprocessing, model)()
            mod2 = getattr(pp, model)()

            df.fit(mod1)
            mod2.fit(iris.data, iris.target)

            result = df.transform(mod1)
            expected = mod2.transform(iris.data)

            self.assertTrue(isinstance(result, expd.ModelFrame))
            self.assert_series_equal(df.target, result.target)
            self.assert_numpy_array_almost_equal(result.data.values, expected)

            mod1 = getattr(df.preprocessing, model)()
            mod2 = getattr(pp, model)()

            result = df.fit_transform(mod1)
            expected = mod2.fit_transform(iris.data)

            self.assertTrue(isinstance(result, expd.ModelFrame))
            self.assert_series_equal(df.target, result.target)
            self.assert_numpy_array_almost_equal(result.data.values, expected)


if __name__ == '__main__':
    import nose
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'],
                   exit=False)
