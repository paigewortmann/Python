# -*- coding: utf-8 -*-
'''
 Paige Wortmann
 Python 2 - DAT-129
 Icon Manipulation
 a program that takes in 1s and 0s and displays a simple character icon
'''


import sys

lst = []

def number_validation(row):
    '''collects 10 numbers from user which goes into its own list'''
    
   # for i in range(10):
       
    counter = 1
       
    while counter < row + 1:
        raw_input = input("Please enter 10 digits, each followed by a space: ")
       
      #  raw_input = input("Please enter 10 digits: ")

        if len(raw_input) != 20:
            if len(raw_input) < 20:
                    raw_input = (input("I dont have enough values, lets try again: "))
            if len(raw_input) > 20:
                    raw_input = (input("I have too many values, lets try again: "))
        else:
            # adds each row into total icon list, each number has its own index
            lst.append(raw_input.split())
            counter += 1
                    
    
    
def encoding(number):
    ''' turns number into either a blank or "*" '''
    if number == '0':
        return " "
    if number == '1':
        return "*"
    
    # if number is not a 1 or 0, will fill in as a space instead
    else:
        return " "
    
def double_encoding(number):
    ''' doubles how many characters are assigned to one number'''
    if number == '0':
        return '  '
    if number == '1':
        return '**'
    else:
        return ' '
            
        
    
def printing(icon):
    '''takes number-validated row and encodes into simple characters'''
    for row in icon:
        for number in row:
            print(encoding(number), end='') # encodes one row at a time
        print('\r') # carriage return
    
def double_printing(icon):
    for row in icon:
        for number in row:
            print(double_encoding(number), end='') 
        print('\r')
    
  #  one_row(10)
    
def main():
    print('Hello and welcome to Icon Translation!')
    print('This program will take 10 "1"s and "0"s and display a pretty')
    print('picture using simple character-based output.')
    print()
    print('disclaimer: any character that is not a 1 or 0 will be interpreted')
    print('as a blank space, and ill write yor name')
   
    number_validation(10) # asks user and validates input 10 times
    printing(lst)
    
    double = input('We can double the size if you would like (yes/no): ')
    if double == 'yes':
        double_printing(lst)
        print('Hope you like it! Thank you.')
        sys.exit(0)
        
    if double == 'no':
        print('Thanks, come again soon.')
        sys.exit(0)
    
    
  
    
if __name__ == '__main__':
    main()
