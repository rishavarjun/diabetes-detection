import sys
import re

args = sys.argv


#print("Args =",args)
#print(args)

arr = args[1].split(':')
input_string = ':'.join(arr[1:])
chars_to_remove = "* '"

for character in chars_to_remove:
    input_string = input_string.replace(character, "")

cleaned_string = input_string

#print("cleaned string =",cleaned_string)
arr_keyval = cleaned_string.split(",")

dictionary = {}
for keyval in arr_keyval:
    temp_Arr = keyval.split(":")
    result = re.sub('/[^0-9.]/g', '', temp_Arr[1])
    dictionary[temp_Arr[0]] = float(result) if result.isnumeric else result
    #dictionary[temp_Arr[0]] = temp_Arr[1]

#print("dictionary =",dictionary)

#print("Output =", dictionary[args[2]])
print(dictionary)

#print(dictionary[args[2]])