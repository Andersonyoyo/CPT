from PredictionTree import *
import pandas as pd
from tqdm import tqdm

class CPT():
    alphabet = None
    root = None
    II = None
    LT = None

    def __init__(self):
        self.alphabet = set()
        self.root = PredictionTree()
        self.II = {}
        self.LT = {}

    def load_files(self,train_file,test_file = None):
        data = []
        target = []
        if train_file is None:
            return train_file
        train = pd.read_csv(train_file)
        for index, row in train.iterrows():    # 按行读取，第一行为索引
            data.append(list(row.values))
        if test_file is not None:
            test = pd.read_csv(test_file)
            for index, row in test.iterrows():
                # data.append(row.values)
                target.append(list(row.values))
            return data, target
        return data

    def train(self, data):
        cursornode = self.root
        # 每个树结构体上的Children都可以append多个子节点，这些子节点是平行的，且不重复的
        # 每次遍历都从根节点开始，往下自动寻找路径
        for seqid,row in enumerate(data):
            for element in row:
                if cursornode.hasChild(element)== False:        # 要添加的点不存在则执行添加
                    cursornode.addChild(element)                # 添加子节点
                    cursornode = cursornode.getChild(element)   # 将锚点定位到子节点上
                else:
                    cursornode = cursornode.getChild(element)   # 将锚点定位到子节点上
                if self.II.get(element) is None:# 键对应没有值
                    self.II[element] = set()    # 无序不重复元素集，一个键有多个不重复集
                self.II[element].add(seqid)     # 添加倒排索引，元素已存在的话不做操作
                self.alphabet.add(element)
            self.LT[seqid] = cursornode         # 保存序列最后一个元素
            cursornode = self.root              # 回到根节点进行下一行的插入
        return True

    def score(self, counttable,key, length, target_size, number_of_similar_sequences, number_items_counttable):
        weight_level = 1/number_of_similar_sequences
        weight_distance = 1/number_items_counttable
        score = 1 + weight_level + weight_distance* 0.001
        if counttable.get(key) is None:
            counttable[key] = score         # 键对应的值为得分
        else:
            counttable[key] = score * counttable.get(key)# 得分再乘上上一次同一字母得分
        return counttable

    def predict(self,data,target,k, n=1):
        predictions = []
        for each_target in tqdm(target): # 显示进度条
            each_target = each_target[-k:]                  # 测试集选择倒数K个数做预测
            intersection = set(range(0,len(data)))
            for element in each_target:                     # 每组序列中的元素
                if self.II.get(element) is None:
                    continue
                intersection = intersection & self.II.get(element)# 迭代，选出包含被测集中所有元素的的序列
            similar_sequences = []
            # print(intersection)
            for element in intersection:
                currentnode = self.LT.get(element)
                tmp = []
                while currentnode.Item is not None:# 向上遍历序列
                    tmp.append(currentnode.Item)
                    currentnode = currentnode.Parent
                similar_sequences.append(tmp)       # 取出intersection中的树中的序列
            for sequence in similar_sequences:  # 反转, similar_sequences中包含的是匹配好的多个序列
                sequence.reverse()
            counttable = {}
            print(similar_sequences)
            for sequence in similar_sequences:
                try:    # 取出匹配到测试集的截断点的索引值
                    index = next(i for i,v in zip(range(len(sequence)-1), sequence) if v == each_target[-1])
                except: # 当v满足判决条件时取出index = i，i 和 v是分别在range(len(sequence)-1), sequence中的迭代器
                    index = None
                if index is not None:
                    count = 1   # 出现次数
                    for element in sequence[index+1:]:# 匹配序列的后面部分
                        if element in each_target:
                            continue
                        counttable = self.score(counttable,element,len(each_target),len(each_target),len(similar_sequences),count)
                        count+=1 # 根据公式每多一个值就加一
            pred = self.get_n_largest(counttable,n) # 取n个预测值
            predictions.append(pred)
        return predictions

    def get_n_largest(self,dictionary,n):
        largest = sorted(dictionary.items(), key = lambda t: t[1], reverse=True)[:n]
        return [key for key,_ in largest]


