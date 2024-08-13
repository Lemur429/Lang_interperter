import lang
while (True):
    text = input('Meow > ')
    com=lang.Command(text)
    print(com.ToToken())