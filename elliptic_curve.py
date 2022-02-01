import itertools

class elliptic_curve:
    def __init__(self, p, a, b):
        if (4*a**3 + 27*b**2 ) % p != 0 and p > 3:
            self.a = a
            self.b = b
            self.p = p
            self.equation = lambda x, y: (y**2 - x**3 - self.a*x - self.b) % p
            self.dots = self.gen_dots()
        else:
            print("no cumple el criterio")

    def modular_sum(self,x,y):
        return (x + y) % self.p
    def modular_sus(self,x,y):
        inv_y = self.p - y
        return (x + inv_y) % self.p
    def modular_mult(self,x,y):
        return (x*y) % self.p
    def modular_div(self,x,y):
        for i in range(self.p):
            if self.modular_mult(i,y) == 1:
                return self.modular_mult(x,i)
    def lamb(self,P,Q):
        if P != Q:
            return self.modular_div(self.modular_sus(Q[1],P[1]),self.modular_sus(Q[0],P[0]))
        else:
            numerador = self.modular_sum(self.modular_mult(self.modular_mult(P[0],P[0]),3),self.a)
            denominador = self.modular_mult(P[1],2)
            print(numerador,denominador)
            return self.modular_div(numerador, denominador)

    def gen_dots(self):
        return [(x,y) for x, y in itertools.product(range(self.p),range(self.p)) if self.equation(x,y) == 0]


ec = elliptic_curve(11,1,6)
print(ec.dots)
print(ec.lamb((2,4),(3,6)))