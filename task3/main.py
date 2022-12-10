import json
import scipy
import operator

class NNClassifier:
    def __init__(self, file):
        try:
            f = open(file)
        except(OSError):
            print("Failed to open file:", file)
        with f:
            self.data = json.load(f)
    def deftype(self, hist, k):
        dists = {}
        for i, value in enumerate(self.data['objects']):
            dists[NNClassifier.histdist(value['hist'], hist)] = value['type']
        sortdists = {i: dists[i] for i in sorted(dists)[:k]}
        types = dict.fromkeys(set(dists.values()), 0)
        for type in sortdists.values():
            types[type]+=1
        sortedval = sorted(types.items(), key=operator.itemgetter(1))
        reqtype = {type for type, value in sortedval[2:]}
        return reqtype
    @staticmethod
    def histdist(hist1, hist2):
        dist = scipy.spatial.distance.euclidean(hist2, hist1)
        return dist
hist = [3, 4, 5]
NNC = NNClassifier('objects.json')
print(NNC.deftype(hist, 3))
