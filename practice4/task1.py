def evengen():
    num = 0
    while True:
        num+=2
        yield num

x = evengen()
i = int(input("Введите число генераций:"))
for i in range(i):
    print(next(x))
