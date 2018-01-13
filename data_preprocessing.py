import pandas as pd
import numpy as np
import sys

class pre_processor:
    def __init__(self):
        self.file = None
    def load_file(self, file_str : str) -> pd.DataFrame:
        """Performs sanity checks on the file specified, before loading it into the pre_processor.
        """
        try:
            file_df = pd.read_csv(file_str,sep=',',quotechar='"',skipinitialspace=True)
            # This is an incomplete list, to be examined further
            expected_columns = ['rent','title_listing','deposit','key_money']
            if ~all(i in expected_columns for i in file_df.columns):
                raise Exception('Expected columns are missing: %s' % ','.join(np.setdiff1d(expected_columns,file_df.columns)))
        except Exception as err:
            print(err)
            return -1
        self.file = file_df