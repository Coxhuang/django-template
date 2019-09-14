p = {
    "a":"c",
    "b":"o"
}


class A(object):

    def __init__(self):
        pass


    def get(self):

        for foo, k in p.items():
            print(foo, k)
            if not hasattr(A, foo):
                setattr(A, foo, k)

    def tetsss(self):

        print(self.a)

z = A()
z.get()
print(dir(z))
z.tetsss()



