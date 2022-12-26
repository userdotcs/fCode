# What is FCode?
FCode is a scripting language designed for developing console applications. It can be used for education with its simple use.

# What's in FCode?
FCode add list:
- [x] Math
- [x] Variables
- [x] if-else
- [x] while
- [ ] Import from other files (It has not been added yet.)

In a file named "main.fcode" write:
```
print("Hello World!")
wait_input()
```
Write the file path of this file in the FCode SDK. Output(After FCode 1.1):
```
Hello World!
```
or;</br>
Code:
```
name = input("What's your name? ")
print("Hello " + name + "!")
wait_input()
```
Output(After FCode 1.1):
```
What's your name? John
Hello John!
```
or;</br>
Code:
```
is_logged = false

while is_logged is false
   username = input("Username: ")
   password = input("Password: ")
   if username is "john" and password is "1234"
      print("Logged in!")
      is_logged = true
   else
      print("Wrong password or username.")
   endif
endwhile

wait_input()
```
Output(After FCode 1.2):
```
Username: adkgjhdg
Password: 452452
Wrong password or username.
Username: john
Password: 123
Wrong password or username.
Username: john
Password: 1234
Logged in!
```
