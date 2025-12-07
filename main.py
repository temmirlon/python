# yield

def test():
    for i in range(5):
        yield i

a = test()

next(a)
next(a)
next(a) 

for i in test():
    print(i)