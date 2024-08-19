import lang
while (True):
    text = input('Meow > ')
    if text=='~': print('Stopping ... '); break
    tokens,error=lang.run(text)
    if error==None:
        print(tokens)
    else :
        print(error)