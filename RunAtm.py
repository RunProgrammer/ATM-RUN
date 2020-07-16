
# By: Tarun
# Atm name = Run
#importing Modules
import sys
import os
import time
import re
from datetime import datetime
from decimal import Decimal

#Initial code with some decoration...

print("_________________")
print("                  ")
print("*****RUN ATM*****")
print("_________________")
print("                  ")

#Main code starts

def replaceFile(account, file):
   os.remove(account + '.txt')
   userFile = open(account + '.txt', 'w')
   #rewrite
   for line in range(len(file)):
       userFile.write(str(file[line]) + '\n')
   userFile.close()
   return file



def equal(p):
   # If there is only one number left, we know all were equal
   if len(p) == 1:
       return True
   else:
       if p[0] == p[1]:
           # If they are equal, we have to check the next ones
           return equal(p[1:])
       else:
           return False

# Handles special cases such as 20 & 8 transactions
def is_special(account, file):
   myFile = open(account + 'history.txt')
   allTransactions = myFile.readlines()
   if len(allTransactions) % 8 == 0:
       now = datetime.now()
       current_time = "%s:%s %s / %s / %s" % (
       now.hour, now.minute, now.month, now.day, now.year)
       history_file = open(account + 'history.txt', 'a')
       history_file.write(current_time + '\n')
       history_file.write(str(-4.00) + '\n')
       if Decimal(file[4]) >= 4:
           balance = file[4]
           file.pop(4)
           file.insert(4, str(Decimal(balance) - Decimal(4)))  # at place 4 I insert the money - 4
       elif 0 < Decimal(file[4]) < 4:
           difference = 4 - Decimal(file[4])
           file.pop(4)
           file.pop(4)
           file.insert(4, str(0))
           file.insert(5, str(Decimal(file[5]) -difference))
           #file = overdraftfunction(difference, file[2], current_time, file)
       else:
           to_be_used = file[5]
           file.pop(5)
           file.insert(5, Decimal(to_be_used) - 4)
   elif len(allTransactions) % 40 == 0:
       history_file = open(account + 'history.txt', 'r')
       myhistory = history_file.readlines()
       total = 0
       print("You have reached 20 transactions. Here they are:")
       for a in range(len(myhistory)):
           if not a % 2 == 0:
               total += Decimal(myhistory[a].split('\n')[0])
           sys.stdout.write(myhistory[a])
       if total > 0:
           print("\nYour net income is: %s" % total)
       else:
           print("\nYour net lose is: %s" % total)

   pass

# Account details.
def view(file):
   print("****************")
   print("ACCOUNT DETAILS")
   print("****************")
   print("YOUR CARD NUMBER: %s" % file[0])
   print("YOUR ACCOUNT BALANCE: %s" % file[4])
   time.sleep(2)


# Printing transaction history
def print_transaction(account):
   transactions = open(account + 'history.txt', 'r')
   allTransactions = transactions.readlines()
   transactions.close()
   if len(allTransactions) == 0:
       print("No transactions yet")
   else:
       print("-------------")
       print("YOUR TRANSACTION:")
       print("-------------")
       for tran in range(len(allTransactions)):
           sys.stdout.write(allTransactions[tran])


# Replacing the pin
def pin(current, account, file):
   while True:
       pin = input("Enter the new pin(must be 4 digits): ")
       if not re.search(r'^\d{4}$', pin):
           continue
       if equal(pin):
           continue
       if pin == current:
           continue
       if pins_check(pin):
           break
       else:
           print("This pin already exists")
   file.pop(1)
   file.insert(1, str(pin))
   sys.stdout.write("Changing pin")
   name = "....\n"
   for char in name:
       sys.stdout.write(char)
       sys.stdout.flush()
       time.sleep(.5)
   return replaceFile(account, file)


def withdraw(money, overdraft, file, account, gone_overdraft):
   if overdraft == 'True':
       gone_overdraft = Decimal(gone_overdraft)
   allOptions = {'1': 500, '2': 700, '3': 1000, '4': 1200, '5': 1500, '6': 1700, '7': 'other'}
   while True:
       option = input('''Pick a withdraw option:
        1)Rs:500 
        2)Rs:700 
        3)Rs:1000 
        4)Rs:1200
        5)Rs:1500
        6)Rs:1700
        7)Other 
        Enter The Method Of Withdraw: ''')
       if option not in allOptions.keys():
           continue
       break
   withdrawen = allOptions[option]
   if withdrawen == 'other':
       while True:
           withdrawen = input("Enter an amount: ")
           try:
               if Decimal(withdrawen) > 0:
                   break
           except Exception:
               continue
   withdrawen = Decimal(withdrawen)
   if money > withdrawen or overdraft == 'True' and money + gone_overdraft > withdrawen:
       print("----------------")
       sys.stdout.write("Withdrawing money")
       name = ".....\n"
       for char in name:
           sys.stdout.write(char)
           sys.stdout.flush()
           time.sleep(.5)
       if money > withdrawen:
           file.pop(4)
           file.insert(4, str(money - withdrawen))
       else:
           difference = withdrawen - money
           gone_overdraft -= difference
           now = datetime.now()
           current_time = "%s:%s %s / %s / %s" % (
           now.hour, now.minute, now.month, now.day, now.year)
           #file =  overdraftfunction(gone_overdraft, file[2], current_time, file)
           money = 0
           file.pop(4)
           file.pop(4)
           file.insert(4, money)
           file.insert(5, gone_overdraft)

       # Rewrite file point
       now = datetime.now()
       current_time = "%s:%s %s / %s / %s" % (now.hour, now.minute, now.month, now.day, now.year)
       history_file = open(account + 'history.txt', 'a')
       history_file.write(current_time + '\n')
       history_file.write(str(-withdrawen) + '\n')
       history_file.close()
       is_special(account, file)
       return replaceFile(account, file)
   else:
       print("---------------")
       print("No enough money")
       print("---------------")
       return file


def deposit(file, userMoney, account):
   allDeposits = []
   while True:
       while True:
           money = input("Enter money to Deposit(done to quit): ".upper())
           try:
               if Decimal(money) < 0:
                   continue
               break
           except Exception:
               if money == "done":
                   break
               else:
                   continue

       if money != 'done':
           allDeposits.append(money)
           time.sleep(2)
           print("----------------")
           print("Deposit accepted")
           print("----------------")
       else:
           break
   total = 0
   for i in range(len(allDeposits)):
       total += Decimal(allDeposits[i])
   if file[3] == 'True' and Decimal(file[5]) < 500:
       if total + Decimal(file[5]) <= 500:
           newOverDraft = Decimal(file[5]) + total
       else:
           subtract = total - Decimal(file[5])
           newOverDraft = 500
           another_varaible_to_store_total = total - subtract
           userMoney += another_varaible_to_store_total
   else:
       userMoney += total
       if file[3] == 'True':
           newOverDraft = 500
       else:
           newOverDraft = "Not in action"
   file.pop(4)
   file.insert(4, str(userMoney))
   file.pop(5)
   file.insert(5, str(newOverDraft))
   now = datetime.now()
   current_time = "%s:%s %s / %s / %s\n" % (now.hour, now.minute, now.month, now.day, now.year)
   history_file = open(account + 'history.txt', 'a')
   history_file.write(current_time)
   history_file.write(str(total) + '\n')
   history_file.close()
   is_special(account, file)
   return replaceFile(account, file)

def menu(file):
   while True:
       print("--------------------------------------------------------")
       print("Welcome To Run Atm.Pick Any Option to Further Proceed: ")
       print("--------------------------------------------------------"      
             "\n1. View your account details"
             "\n2. Change PIN"
             "\n3. Withdraw money"
             "\n4. Deposit money"
             "\n5. View History"
             "\n6. Quit")
       navigation = input("Pick any option: ")
       
       if navigation == '1':
           view(file)
       
       elif navigation == '2':
           file = pin(file[1], file[0], file)
       
       elif navigation == '3':
           file = withdraw(Decimal(file[4]), file[3], file, file[0], file[5])
       
       elif navigation == '4':
           file = deposit(file, Decimal(file[4]), file[0])
       
       elif navigation == '5':
           print_transaction(file[0])
       
       elif navigation == '6':
           print_transaction(file[0])
           return


def pins_check(pin_input):
   if os.path.exists('pins.txt'):
       pins = open('pins.txt', 'r')
       myFile = pins.readlines()
       pins.close()
       for pin in range(len(myFile)):
           new = myFile[pin].replace('\n', '')
           myFile.pop(pin)
           myFile.insert(pin, new)
       if pin_input in myFile:
           return False
       else:
           myPin = open('pins.txt', 'a')
           myPin.write(pin_input + '\n')
           myPin.close()
           return True

   else:
       pins = open('pins.txt', 'w')
       pins.write(pin_input + '\n')
       pins.close()
       return True

def signup():
   # input of card
   while True:
       card = input("Enter the card number[Must Be 4 Digits]: ")
       if not re.search(r'^\d{4}$', card):
           continue
       if equal(card):
           continue
       break
   # Pin input
   while True:
       pin = input("Enter the pin number[Must Be 4 Digits]: ")
       if not re.search(r'^\d{4}$', pin):
           continue
       if equal(pin):
           continue
       if pins_check(pin):
           break
       else:
           print("The pin already exists")
   
   while True:
       print("*****************")
       print("Would You Like To Sign Up For Protection?")
       prompt_overdraft = input("IF YES (y), IF NO (n): ")
       if prompt_overdraft == 'y' or prompt_overdraft == 'yes':
           overdraft = 'True'
           break
       elif prompt_overdraft == 'n' or prompt_overdraft == 'no':
           overdraft = 'False'
           break
       
   userFile = open(card + '.txt', 'w')
   userFile.write(card + '\n' + pin + '\n' +  '\n' + overdraft + '\n' + '0' + '\n')
   if overdraft == 'True':
       userFile.write('500')
   else:
       userFile.write('Not in action')
   userFile.close()
   user_history_file = open(card + 'history.txt', 'w')
   user_history_file.close()
   print("_________________")
   print("                 ")
   print("***LOGIN PAGE***")
   print("_________________")
   print("                 ")
   login()


def login():
   while True:
       card_login = input("Enter your card number: ")
       if not os.path.exists(card_login + '.txt'):
           continue
       break
   user_file = open(card_login + '.txt')
   userLines = user_file.readlines()
   
   for line in range(len(userLines)):
       new = userLines[line].replace('\n', '')
       userLines.pop(line)
       userLines.insert(line, new)
   user_file.close()

   actual_pin = userLines[1]
   while True:
       pin_login = input("Enter your pin: ")
       if not pin_login == actual_pin:
        print("-------------")
        print("Access Denied")
        print("-------------")
        continue
        
       break

   menu(userLines)
   return


while True:
   enter = input("Would you like to [ login (I) or signup (U) ]: ".upper())
   if enter == 'i':
       login()
       break
   elif enter == 'u':
       signup()
       break

print("___________________")
print("                   ")
print("*****THANK YOU*****") 
print("___________________")
print("                   ")   


