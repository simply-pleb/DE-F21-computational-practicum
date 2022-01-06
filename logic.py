from abc import abstractclassmethod
import math
import threading
# import time

APR_ZERO = 1e-8

class Initial_value:
    _x0=0
    _y0=0 
    _X=0
    def __init__(self, x0, X, y0) -> None:
        self._x0 = x0
        self._X = X
        self._y0 = y0
        pass

    def get_x0(self):
        return self._x0
    def get_X(self):
        return self._X
    def get_y0(self):
        return self._y0

class DE:
    _iv: Initial_value
    _c = 0
    
    # Constructors
    def __init__(self, x0, X, y0) -> None:
        self.set_initial_value(Initial_value(x0, X, y0))
        pass
    def __init__(self, iv:Initial_value) -> None:
        self.set_initial_value(iv)
        pass
    
    def get_initial_value(self):
        return self._iv

    # Sets initial values of DE and calculates the constant term
    def set_initial_value(self, iv):
        self._iv = iv
        self._calc_constant()
    
    def get_constant(self):
        return self._c

    # Calculates the constant term of DE
    def _calc_constant(self):
        x = self._iv.get_x0()
        y = self._iv.get_y0()
        if x==0:
            # print("!%f!"%(x))
            x = APR_ZERO
        elif x==1:
            # print("!%f!"%(x))
            x = 1+APR_ZERO
        self._c = (y+math.log(x))/(math.log(x)**2)
    
    def solve_de(self, x, y):
        if x==0:
            print("!%f!"%(x))
            x = APR_ZERO
        elif abs(x)==1:
            print("!%f!"%(x))
            x = 1+APR_ZERO
        return 1/x + 2*y/(x*math.log(x))

    def solve_exact(self, x):
        if x==0:
            x = APR_ZERO
        return self._c*math.log(x)**2 - math.log(x)

class Memory_unit:
    x: float
    val: float
    lte: float
    gte: float
    def __init__(self, x, val, lte, gte) -> None:
        self.x = x
        self.val = val
        self.lte = lte
        self.gte = gte
        pass


class Method:
    @abstractclassmethod
    def solve(self, de:DE, n):
        pass

class Method_exact(Method):
    def solve(self, de: DE, n):
        mem = []

        iv = de.get_initial_value()
        x = iv.get_x0()
        y0 = iv.get_y0()
        xf = iv.get_X()

        prev_val = y0
        step_len = (xf-x)/n
        mem.append(Memory_unit(x, y0, 0, 0))
        for i in range (1, n+1):
            x = x+step_len
            val = de.solve_exact(x)
            lte = 0
            gte = 0
            
            mem.append(Memory_unit(x, val, lte, gte))
            prev_val = val   
        
        return mem

class Method_euler(Method):
    def solve(self, de: DE, n):
        mem = []

        iv = de.get_initial_value()
        x = iv.get_x0()
        y0 = iv.get_y0()
        xf = iv.get_X()

        prev_val = y0
        step_len = (xf-x)/n
        mem.append(Memory_unit(x, y0, 0, 0))
        for i in range (1, n+1):
            cur_step = step_len*de.solve_de(x, prev_val)
            val = prev_val + cur_step
            
            # lte = self.exact[i] - self.exact[i-1] - cur_step 
            lte = de.solve_exact(x+step_len) - de.solve_exact(x) - cur_step
            lte = abs(lte)

            gte = de.solve_exact(x+step_len) - val
            gte = abs(gte)
            
            x = x+step_len
            mem.append(Memory_unit(x, val, lte, gte))
            # f.write("%f,%f,%f,%f\n"%(x, val, lte, gte))
            prev_val = val   
        
        return mem

class Method_improved_euler(Method):
    def solve(self, de: DE, n):
        mem = []

        iv = de.get_initial_value()
        x = iv.get_x0()
        y0 = iv.get_y0()
        xf = iv.get_X()

        prev_val = y0
        step_len = (xf-x)/n
        mem.append(Memory_unit(x, y0, 0, 0))
        for i in range (1, n+1):
            temp = prev_val + step_len*de.solve_de(x, prev_val)
            cur_step = (de.solve_de(x, prev_val) + de.solve_de(x+step_len, temp))*step_len/2
            val = prev_val + cur_step
            
            # lte = self.exact[i] - self.exact[i-1] - cur_step 
            lte = de.solve_exact(x+step_len) - de.solve_exact(x) - cur_step
            lte = abs(lte)

            gte = de.solve_exact(x+step_len) - val
            gte = abs(gte)
            
            x = x+step_len
            mem.append(Memory_unit(x, val, lte, gte))
            # f.write("%f,%f,%f,%f\n"%(x, val, lte, gte))
            prev_val = val   
        
        return mem

class Method_runge_kutta(Method):
    def solve(self, de: DE, n):
        mem = []

        iv = de.get_initial_value()
        x = iv.get_x0()
        y0 = iv.get_y0()
        xf = iv.get_X()

        prev_val = y0
        step_len = (xf-x)/n
        mem.append(Memory_unit(x, y0, 0, 0))
        for i in range (1, n+1):
            temp1 = de.solve_de(x, prev_val)
            temp2 = de.solve_de(x+step_len/2, prev_val+step_len/2*temp1)
            temp3 = de.solve_de(x+step_len/2, prev_val+step_len/2*temp2)
            temp4 = de.solve_de(x+step_len, prev_val+step_len*temp3)
            cur_step = step_len/6*(temp1+2*temp2+2*temp3+temp4)

            val = prev_val + cur_step
            
            lte = de.solve_exact(x+step_len) - de.solve_exact(x) - cur_step
            lte = abs(lte)

            gte = de.solve_exact(x+step_len) - val
            gte = abs(gte)
            
            x = x+step_len
            mem.append(Memory_unit(x, val, lte, gte))
            prev_val = val   
        
        return mem


# de = DE(Initial_value(2, 12, 0))
# meth = Method_euler()
# mem = meth.solve(de, 10)

# meth = Method_runge_kutta()
# mem1 = meth.solve(de, 10)

# for x in mem1:
#     print(x.val)
#     pass

# meth = Solving_methods(de, 10)
# meth.solve()

class Solution_plotter:
    _de: DE
    _n: int

    def __init__(self, de, n) -> None:
        self._de = de
        self._n = n

    def set_de(self, de):
        self._de = de

    def set_n(self, n):
        # self._n0 = n0
        self._n = n
        # self.calc_and_save_all()

    def calc_and_save_exact(self):
        meth = Method_exact()
        mem = meth.solve(self._de, self._n)
        f = open("data/exact.csv", "w")
        f.write("x,y(x),LTE,GTE\n")
        for i in mem:
            f.write("%f,%f,%f,%f\n"%(i.x, i.val, i.lte, i.gte))

    def calc_and_save_euler(self):
        meth = Method_euler()
        mem = meth.solve(self._de, self._n)
        f = open("data/euler.csv", "w")
        f.write("x,y(x),LTE,GTE\n")
        for i in mem:
            f.write("%f,%f,%f,%f\n"%(i.x, i.val, i.lte, i.gte))
    
    def calc_and_save_im_euler(self):
        meth = Method_improved_euler()
        mem = meth.solve(self._de, self._n)
        f = open("data/im_euler.csv", "w")
        f.write("x,y(x),LTE,GTE\n")
        for i in mem:
            f.write("%f,%f,%f,%f\n"%(i.x, i.val, i.lte, i.gte))
    
    def calc_and_save_rg_kt(self):
        meth = Method_runge_kutta()
        mem = meth.solve(self._de, self._n)
        f = open("data/rg_kt.csv", "w")
        f.write("x,y(x),LTE,GTE\n")
        for i in mem:
            f.write("%f,%f,%f,%f\n"%(i.x, i.val, i.lte, i.gte))

    def calc_and_save_all(self):
        t_ex = threading.Thread(target=self.calc_and_save_exact)
        t_eu = threading.Thread(target=self.calc_and_save_euler)
        t_ieu = threading.Thread(target=self.calc_and_save_im_euler)
        t_rk = threading.Thread(target=self.calc_and_save_rg_kt)
        
        t_ex.start()
        t_eu.start()
        t_ieu.start()
        t_rk.start()

        t_ex.join()
        t_eu.join()
        t_ieu.join()
        t_rk.join()

class GTE_plotter:
    _de: DE
    _n0: int
    _n: int

    def __init__(self, de, n0, n) -> None:
        self._de = de
        self._n0 = n0
        self._n = n

    def set_de(self, de):
        self._de = de

    def set_bounds(self, n0, n):
        self._n0 = n0
        self._n = n
        # self.calc_and_save_all()

    def get_n(self):
        return self._n

    def get_n0(self):
        return self._n0

    def calc_max_gte_euler(self):
        meth = Method_euler()
        f = open("data/gte_euler.csv", "w")
        f.write("x,max GTE\n")
        for i in range(self._n0, self._n+1):
            mem = meth.solve(self._de, i)
            max_gte=0
            for j in mem:
                max_gte = max(max_gte, j.gte)
            f.write("%f,%f\n"%(i, max_gte))
    
    def calc_max_gte_im_euler(self):
        meth = Method_improved_euler()
        f = open("data/gte_im_euler.csv", "w")
        f.write("x,max GTE\n")
        for i in range(self._n0, self._n+1):
            mem = meth.solve(self._de, i)
            max_gte=0
            for j in mem:
                max_gte = max(max_gte, j.gte)
            f.write("%f,%f\n"%(i, max_gte))
    
    def calc_max_gte_rg_kt(self):
        meth = Method_runge_kutta()
        f = open("data/gte_rg_kt.csv", "w")
        f.write("x,max GTE\n")
        for i in range(self._n0, self._n+1):
            # print("%d\n"%(i))
            mem = meth.solve(self._de, i)
            max_gte=0
            for j in mem:
                max_gte = max(max_gte, j.gte)
            f.write("%f,%f\n"%(i, max_gte))
    
        # return max_gte

    def calc_and_save_all(self):
        t_eu = threading.Thread(target=self.calc_max_gte_euler)
        t_ieu = threading.Thread(target=self.calc_max_gte_im_euler)
        t_rk = threading.Thread(target=self.calc_max_gte_rg_kt)
        
        t_eu.start()
        t_ieu.start()
        t_rk.start()

        t_eu.join()
        t_ieu.join()
        t_rk.join()

