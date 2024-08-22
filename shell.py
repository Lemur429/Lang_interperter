import lang
#def factorial(n):
#    return n and n * factorial(n - 1) or 1

while (True):
 #   print(factorial(5))
    text = input('Meow > ')
    if text=='~': print('Stopping ... '); break
    tokens,error=lang.run(text,'Shell')
    if error==None:
        print(tokens)
    else:
        print(error)