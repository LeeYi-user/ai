import random

vars = [0, 0, 0]
value = 0
fails = 0

def f(vars):
    if vars[0] + vars[1] <= 10 and 2*vars[0] + vars[2] <= 9 and vars[1] + 2*vars[2] <= 11 and vars[0] >= 0 and vars[1] >= 0 and vars[2] >= 0:
        return 3*vars[0] + 2*vars[1] + 5*vars[2]
    else:
        return -1

if __name__ == "__main__":
    while fails < 10000:
        newVars = vars.copy()

        for i in range(len(newVars)):
            newVars[i] += random.choice([-1, 1]) * 0.01
        
        newValue = f(newVars)

        if newValue > value:
            vars = newVars
            value = newValue
            print(value)
        else:
            fails += 1
    
    print(vars)
