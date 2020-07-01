from CPT import CPT
from PredictionTree import PredictionTree
from tqdm import tqdm
from time import sleep

model = CPT()
data,target = model.load_files("./data/train.csv","./data/test.csv")
# print(data)
# print(target)
model.train(data)
predictions = model.predict(data,target,5,3)
print(predictions)

