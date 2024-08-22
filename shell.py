import lang
#def factorial(n):
#    return n and n * factorial(n - 1) or 1

while (True):
 #   print(factorial(5))
    text = input('Meow > ')
    if text=='~': print('Stopping ... '); break
    if text=='.':
        text=input('FileName >')
        with open(text) as f:
            lang.run(f.read(),'text')
    else:
        lang.run(text,'Shell')
