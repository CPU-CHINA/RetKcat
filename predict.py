from bin.Process import process
from codes.run import predict
import pickle
import os
pr=process(init=False,path='bin/lib/')# creat tem file input.pkl
with open('input.pkl','rb') as inp:
    inp=pickle.load(inp)
    predict(inp,'modelstate/tr50.modelstate')
os.remove('input.pkl')
import analysis.pearson
#import analysis.box