import sys
args = sys.argv

arr = args[1].split(':')
input_string = ':'.join(arr[1:])
chars_to_remove = "* '"

for character in chars_to_remove:
    input_string = input_string.replace(character, "")

cleaned_string = input_string
arr_keyval = cleaned_string.split(",")

dictionary = {}
for keyval in arr_keyval:
    temp_Arr = keyval.split(":")
    #dictionary[temp_Arr[0]] = float(temp_Arr[1]) if temp_Arr[1].isnumeric else temp_Arr[1]
    dictionary[temp_Arr[0]] = temp_Arr[1]

#print(dictionary[args[2]])
print(dictionary)