from sfsf import sfsf_config
from sfsf import training_data_factory
import pickle

# main
training_factory = training_data_factory.TrainingDataFactory()
#training_data = training_factory.create_by_indices( 'wpg_data.csv', (1,5,-600,-596), sample_size=5000, source=sfsf_config.TXT  )
training_data = training_factory.create_by_indices( 'wpg_data.csv', (1,51,-599,-549), sample_size=5000, source=sfsf_config.TXT  )
pickle.dump( training_data, open( 'sfsf_training_data.pickle', 'wb' ) )
