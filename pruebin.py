regex = '(1|0)*001(1|0)*'
boperands='|.'
uoperands='+*'

def toPostfix(regex):
    stack = []
    for char in regex:
        if char in boperands:
            stack.append(char)
        elif char in uoperands:
            op1 = stack.pop()
            op2 = stack.pop()
        






print(regex)
print(concat(regex))
print(toPostFix(regex))