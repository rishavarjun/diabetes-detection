import sys
import re

args = sys.argv

str = args[1]

list_of_char = ["*", " ", "'"]
pattern = '[' + ''.join(list_of_char) + ']'
# Remove characters matched by pattern
result = re.sub(pattern, '', str)
#--
arr = result.split(':')
input_string = ':'.join(arr[1:])

cleaned_string = input_string

arr_keyval = cleaned_string.split(",")

dictionary = {}
for keyval in arr_keyval:
    temp_Arr = keyval.split(":")
    result = ""
    try:
        result = float(temp_Arr[1])
    except ValueError:
        result = temp_Arr[1]

    dictionary[temp_Arr[0]] = result
    
print(dictionary[args[2]])
