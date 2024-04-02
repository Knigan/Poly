class Poly:
    def __init__(self, L: list):
        if isinstance(L, dict):
            self.P = dict(sorted(L.items()))
        elif isinstance(L, list):
            self.P = {n: L[n] for n in range(len(L))}
        else:
            raise TypeError("Переменная L должна быть списком или словарём")
    
    def __str__(self):
        if len(self.P) == 0:
            return '0'
        
        for i in self.P:
            if self.P[i] == int(self.P[i]):
                self.P[i] = int(self.P[i])

        arr = []
        for i in self.P:
            if self.P[i] != 0:
                if i == 0:
                    arr.append(str(self.P[i]))

                elif i == 1:
                    if self.P[i] == 1:
                        arr.append("x")
                    elif self.P[i] == -1:
                        arr.append("- x")
                    elif self.P[i] < 0:
                        arr.append(f"- {-self.P[i]} x")
                    else:
                        arr.append(f"{self.P[i]} x")
                
                else:
                    if self.P[i] == 1:
                        arr.append(f"x^{i}")
                    elif self.P[i] == -1:
                        arr.append(f"- x^{i}")
                    elif self.P[i] < 0:
                        arr.append(f"- {-self.P[i]} x^{i}")
                    else:
                        arr.append(f"{self.P[i]} x^{i}")
        
        if len(arr) == 0:
            return '0'
        
        res = arr[0]
        for i in range(1, len(arr)):
            if arr[i][0] == '-':
                res += " " + arr[i]
            else:
                res += " + " + arr[i]
        
        return res
                                      
    
    def __repr__(self):
        return self.__str__()
    
    def __add__(self, other):
        d = self.P
        if isinstance(other, int) or isinstance(other, float):
            if 0 in d:
                d[0] += other
            else:
                d[0] = other
        elif isinstance(other, Poly):
            for i in other.P:
                if i in d:
                    d[i] += other.P[i]
                else:
                    d[i] = other.P[i]
        else:
            raise TypeError("Вы можете складывать полиномы только с числами или другими полиномами")
        
        return Poly(d)
    
    def __radd__(self, other):
        d = self.P
        if isinstance(other, int) or isinstance(other, float):
            if 0 in d:
                d[0] += other
            else:
                d[0] = other
        else:
            raise TypeError("Вы можете складывать полиномы только с числами или другими полиномами")
        
        return Poly(d)        

    def __sub__(self, other):
        d = self.P
        if isinstance(other, int) or isinstance(other, float):
            if 0 in d:
                d[0] -= other
            else:
                d[0] = -other
        elif isinstance(other, Poly):
            for i in other.P:
                if i in d:
                    d[i] -= other.P[i]
                else:
                    d[i] = other.P[i]
        else:
            raise TypeError("Вы можете вычитать из полиномов только числа или другие полиномы")
        
        return Poly(d)
    
    def __rsub__(self, other):
        d = self.P
        if isinstance(other, int) or isinstance(other, float):
            for i in d:
                d[i] = -d[i]

            if 0 in d:
                d[0] += other
            else:
                d[0] = other
        else:
            raise TypeError("Вы можете вычитать из полиномов только числа или другие полиномы")
        
        return Poly(d)    
    
    def __mul__(self, other):
        d = {}
        if isinstance(other, int) or isinstance(other, float):
            d = self.P
            for i in d:
                d[i] *= other
        elif isinstance(other, Poly):
            if len(other.P) == 0:
                return Poly([])
            
            for i in self.P:
                for j in other.P:
                    if i + j in d:
                        d[i + j] += self.P[i] * other.P[j]
                    else:
                        d[i + j] = self.P[i] * other.P[j]
        else:
            raise TypeError("Вы можете умножать на полином только числа или другие полиномы")

        return Poly(d)
    
    def __rmul__(self, other):
        d = self.P
        if isinstance(other, int) or isinstance(other, float):
            for i in d:
                d[i] *= other
        else:
            raise TypeError("Вы можете умножать полином только на числа или другие полиномы")

        return Poly(d)        

    def __truediv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            if other == 0:
                raise ValueError("Деление на ноль невозможно!")
            d = self.P
            for i in d:
                d[i] /= other
            
            return Poly(d)
        elif isinstance(other, Poly):
            if len(other.P) == 0:
                raise ValueError("Деление на ноль невозможно!")
            flag = True
            for i in other.P:
                if other.P[i] != 0:
                    flag = False
                    break
            if flag:
                raise ValueError("Деление на ноль невозможно!")

            if list(other.P.keys())[-1] > list(self.P.keys())[-1]:
                return Poly([])
            elif list(other.P.keys())[-1] == list(self.P.keys())[-1]:
                return Poly([self.P[self.P.keys()[-1]] / other.P[other.P.keys()[-1]]])
            else:
                l = min(len(self.P.keys()), len(other.P.keys()))
                buffer = {}
                temp = Poly(self.P)
                k = 1
                for i in range(1, l + 1):
                    deg = list(self.P.keys())[-i] - list(other.P.keys())[-k]

                    while deg < 0:
                        k += 1
                        if k <= l:
                            deg = list(self.P.keys())[-i] - list(other.P.keys())[-k]
                        else:
                            break
                    
                    if k > l:
                        break

                    buffer[deg] = temp.P[list(temp.P.keys())[-i]] / other.P[list(other.P.keys())[-k]]
                    if deg != 0:
                        temp = temp - other * Poly({deg: buffer[deg]})
                    else:
                        break
                    
                
                return Poly(buffer)
        else:
            raise TypeError("Вы можете делить полином только на числа или другие полиномы")
    
    def __rtruediv__(self, other):
        return Poly([])
    
    def __mod__(self, other):
        return self - (self / other) * other
    
    def __pow__(self, n):
        def factorial(n):
            res = 1
            for k in range(2, n + 1):
                res *= k
            return res
        
        if n == 0:
            if len(self.P) == 0:
                raise ValueError("Невозможно возвести 0 в нулевую степень!")
            flag = True
            for i in self.P:
                if self.P[i] != 0:
                    flag = False
                    break
            if flag:
                raise ValueError("Невозможно возвести 0 в нулевую степень!")
            
            return Poly([1])
        if len(self.P) == 0:
            return Poly([])
        elif len(self.P) == 1:
            d = {}
            for i in self.P:
                d[i * n] = self.P[i] ** n
            
            return Poly(d) 
        else:
            p0 = Poly({list(self.P.keys())[0]: list(self.P.values())[0]})
            p1 = Poly({list(self.P.keys())[i]: list(self.P.values())[i] for i in range(1, len(self.P))})
            S = 0
            for k in range(n + 1):
                S += factorial(n) / (factorial(k) * factorial(n - k)) * p1 ** (n - k) * p0 ** k
            return S
    
    def __eq__(self, other):
        if len(self.P) != len(other.P):
            return False
        
        for i in range(len(self.P)):
            if list(self.P.items())[i][0] != list(other.P.items())[i][0] or float(list(self.P.items())[i][1]) != float(list(other.P.items())[i][1]):
                return False
        
        return True
    
    def __ne__(self, other):
        return not(self == other)
    

    def eval(self, value):
        res = 0
        for i in self.P:
            res += self.P[i] * value ** i
        
        return res
    
    def diff(self, num):
        if num == 0:
            return self
        
        temp = self.P
        for _ in range(num):
            temp2 = {}
            for i in temp:
                if i != 0:
                    temp2[i - 1] = i * temp[i]
            temp = temp2
        return Poly(temp)
    
    def integrate(self, a, b):
        temp = {}
        for i in self.P:
            temp[i + 1] = self.P[i] / (i + 1)
        
        res = Poly(temp)
        return res.eval(b) - res.eval(a)
    
    def shift(self, num):
        res = Poly([])
        for i in self.P:
            res = res + self.P[i] * Poly([num, 1]) ** i
        
        return res


if __name__ == "__main__":
    d1 = {0: 1, 1: 2, 2: 3}
    d2 = {0: 1, 1: 2, 2: 1}
    a = Poly(d1)
    b = Poly(d2)
    print((a ** 10) / (a ** 9))