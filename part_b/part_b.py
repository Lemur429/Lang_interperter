from functools import *

#QUESTION 1: Implement a Fibonacci sequence generator using a single lambda expression that
#returns a list of the first n Fibonacci numbers. The function should take n as an input.
fibonacci = lambda n: reduce(lambda x,_: x + [x[-1] + x[-2]], range(n-2), [0, 1])[:n]
print(f'QUESTION 1:{fibonacci(8)}\n')

#QUESTION 2:Write the shortest Python program, that accepts a list of strings and return a
#single string that is a concatenation of all strings with a space between them. Do not
#use the "join" function. Use lambda expressions
sec= lambda lis :reduce(lambda a,b:f'{a} {b}',lis)
print(f'QUESTION 2:{sec(['hello','world', '!'])}\n')

#QUESTION 3:Write a Python function that takes a list of lists of numbers and return a new list
#containing the cumulative sum of squares of even numbers in each sublist. Use at
#least 5 nested lambda expressions in your solution.
third=lambda lists:reduce(lambda a,b: a+b,map(lambda lis:reduce(lambda a,b: a+b,map(lambda a: a**2,filter(lambda a:a%2==0,lis))),lists))
print(f'QUESTION 3{third([ [4,2,4,5] , [1,1,1,1,8],[2,3,4,5]    ])}\n')

#QUESTION 4:Write a higher-order function that takes a binary operation (as a lambda function)
#and returns a new function that applies this operation cumulatively to a sequence.
#Use this to implement both factorial and exponentiation functions.
fourth=lambda op:lambda lis:reduce(op,lis)
fact=fourth(lambda a,b: a*b)
print(f'QUESTION 4 ,factorial:{fact(range(1,8))}')
print(f'QUESTION 4 , exponent:{fact([5]*5)}\n')
#QUESTION 5:Rewrite the following program in one line by using nested filter, map and reduce
#functions
print(f'QUESTION 5:{reduce(lambda a,b:a+b,map(lambda a:a**2,filter(lambda a: a%2==0,[1,2,3,4,5,6])))}\n')
#QUESTION 6:Write one-line function that accepts as an input a list of lists containing strings
#and returns a new list containing the number of palindrome strings in each sublist.
#Use nested filter / map / reduce functions.
sixth=lambda lists:list(map(lambda lis: len(list(filter(lambda string:string==string[::-1],lis))),lists))
print(f"QUESTION 6:{sixth([['aaa','meow','asesa','fsdf'],['ba','woemeow','sa','fsdf']])}\n")

#QUESTION 7:Explain the term "lazy evaluation" in the context of the following program
# חישוב עצל לפי התוכנית הוא בעצם חישוב שחוסך את הגדרת משתנה נוסף לגשר בין הקוד
# זה חוסך משתנה נוסף אבל יכול לגרום לקוד להראות יותר מסובך

#QUESTION 8:Write a one-line Python function that takes a list of integers and returns a new list
#containing only the prime numbers, sorted in descending order. Use lambda
#expressions and list comprehensions.
eigth=lambda lis:sorted(list(filter(lambda is_prime: is_prime and all(is_prime%i!=0 for i in range(2,is_prime)),lis)),reverse=True)
print(f'QUESTION 8:{eigth(range(3,75))}')