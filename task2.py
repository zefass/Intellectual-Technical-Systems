import scipy

def triangle(a):
    max = a
    stars = 1
    for i in range(a+1):
        print(' '*max, '*'*stars)
        stars+=2
        max-=1
triangle(3)

def histdist(hist1, hist2):
    dist=scipy.spatial.distance.euclidean(hist2, hist1)
    return dist
print(histdist((1, 0, 0), (0, 0, 1)))

def write(file, hist):
    text = ', '.join(str(i) for i in hist)
    with open(file, 'w') as f:
        f.write(text)

def read(file):
    with open(file, 'r') as r:
        reading=r.read()
    return reading

write('file.txt', (1, 0, 0))
print(read('file.txt'))



