import numpy as np
import pandas as pd
import torch
from .column_transformer import Column_transformer

class Categorical_transformer(Column_transformer):
    def __init__(self, column):
        super().__init__()
        mapper = column.value_counts().index.tolist()
        self.size = len(mapper)
        self.i2s = mapper

        self.fit(column.to_numpy())

    def fit(self, data_col):
        self.model = None
        self.components = None
        self.output_info = [(self.size, 'softmax', None)]
        self.output_dim = self.size
        

    def transform(self, data_col):
        data_col = np.asarray(data_col,int)
        self.ordering = None
        col_t = np.zeros([len(data_col), self.size])
        col_t[np.arange(len(data_col)), data_col] = 1
        return col_t

    def inverse_transform(self, data_col,st):
        # data_col = np.asarray(data_col,int)
        u = data_col[:, st:st + self.size]
        idx = np.argmax(u, axis=1)
        new_st = st + self.size
        return idx, new_st, []



    
    def inverse_transform_static(self, data, transformer, st, device,n_clusters=10): #TODO: remove n cluster when finding out how to handle this
        
        idx = torch.argmax(data[:, st:st + transformer.size], dim=1)
        new_st = st + transformer.size
        return idx, new_st, []