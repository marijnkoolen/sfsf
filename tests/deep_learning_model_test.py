import setup_dev
import unittest
import numpy
import os
from sfsf import deep_learning_model
from sfsf import sfsf_config
from sfsf import training_data_factory

class DeepLearningModelTest( unittest.TestCase ):

    def setUp( self ):
        sfsf_config.set_env( sfsf_config.DEVELOPMENT )

    def test_build_deep_learning_model( self ):
        factory = training_data_factory.TrainingDataFactory()
        training_data = factory.create( 'wpg_data.csv', 2 )
        model = deep_learning_model.DeepLearningModel()
        # training_data, batch_size, epochs
        accuracy = model.build( ( training_data['x'], training_data['y'] ), 10, 5 )
        self.assertEqual( 100.00, accuracy )

    def test_prediction_no_model( self ):
        model = deep_learning_model.DeepLearningModel()
        with self.assertRaises( deep_learning_model.NoDeepLearningModelError ):
            model.predict( None )

    def test_prediction_wrong_test_dimension( self ):
        factory = training_data_factory.TrainingDataFactory()
        training_data = factory.create( 'wpg_data.csv', 2 )
        model = deep_learning_model.DeepLearningModel()
        # training_data, batch_size, epochs
        accuracy = model.build( ( training_data['x'], training_data['y'] ), 10, 5 )
        with self.assertRaises( deep_learning_model.TestingDimensionError ):
            model.predict( numpy.array( [ [ 1, 2, 3 ], [1, 2, 3 ] ] ) )

    def test_predictions( self ):
        factory = training_data_factory.TrainingDataFactory()
        training_data = factory.create( 'wpg_data.csv', 2 )
        model = deep_learning_model.DeepLearningModel()
        # training_data, batch_size, epochs
        accuracy = model.build( ( training_data['x'], training_data['y'] ), 10, 5 )
        vect = training_data['vectorizer']
        isbn_info = [ [ '', 9789023449416, '' ] ]
        test_tuples = factory.sample_epubs( isbn_info, 1000 )[-4:]
        test_samples = [ test_sample for tupel in test_tuples for test_sample in tupel[1] ]
        test_tdm = vect.transform( test_samples )
        predictions = model.predict( numpy.array( test_tdm.toarray() ) )
        for idx, prediction in enumerate( predictions ):
            assert( prediction[0] > 0.9 )

    def test_save_load( self ):
        factory = training_data_factory.TrainingDataFactory()
        training_data = factory.create( 'wpg_data.csv', 2 )
        model = deep_learning_model.DeepLearningModel()
        # training_data, batch_size, epochs
        accuracy = model.build( ( training_data['x'], training_data['y'] ), 10, 5 )
        model.save( 'test_save_load_model' )
        del model
        vect = training_data['vectorizer']
        isbn_info = [ [ '', 9789023449416, '' ] ]
        test_tuples = factory.sample_epubs( isbn_info, 1000 )[-4:]
        test_samples = [ test_sample for tupel in test_tuples for test_sample in tupel[1] ]
        test_tdm = vect.transform( test_samples )
        model = deep_learning_model.DeepLearningModel()
        model.load( 'test_save_load_model' )
        predictions = model.predict( numpy.array( test_tdm.toarray() ) )
        for idx, prediction in enumerate( predictions ):
            assert( prediction[0] > 0.9 )
        os.remove( os.path.join( sfsf_config.get_data_dir(), 'test_save_load_model.h5' ) )

if __name__ == '__main__':
    unittest.main()
