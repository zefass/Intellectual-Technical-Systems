def chetnumgen(n):
    x = [i*2 for i in range(1, n)]
    yield x
for i in (range(12)):
    print(next(chetnumgen(i)))
