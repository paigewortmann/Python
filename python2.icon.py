# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 17:42:03 2021

@author: 17244
"""

"""Declare global variable for access
by all functions in the script """


def number_validation():
    '''collects user numbers and prints them vertically'''
    lst = []
    
    n = 10
    # asks for a new row 10 times
    
    for i in range(0 , n):
        user_row = input("Please enter row of 10 digits: ")
        
        new_row = lst.append([user_row])
        
            
    
    print() #space
    return new_row

def encoding():
    
# work in progress??
    encoding_lst = number_validation()
    for i in encoding_lst:
        if i == '1':
            encoding_lst = '*'
        elif i == '0':
            encoding_lst = ' '
    
# gets rid of "[]" and "," from lst
    for i in encoding_lst:
        print(' '.join(map(str, i)))
        return encoding_lst
        
def printing():
    
        
      

            

def main():
    user_icon = number_validation()
    print(user_icon)
    
   # encoding(user_icon)
    

  
    
if __name__ == '__main__':
    main()