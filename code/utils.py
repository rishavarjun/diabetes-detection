#python code/utils.py 

import sys
args = sys.argv

#args = ["aasa","***diabetes-detection-monitor-via-aml_1629891337_5975a671: ***testing_value: 15, pradeep_fresh_data_accuracy: 0.456***", "pradeep_fresh_data_accuracy"]

print(args[1])

arr = args[1].split(':')
input_string = ':'.join(arr[1:])
chars_to_remove = "* "

print(input_string)

for character in chars_to_remove:
    input_string = input_string.replace(character, "")

cleaned_string = input_string
arr_keyval = cleaned_string.split(",")

dictionary = {}
for keyval in arr_keyval:
    temp_Arr = keyval.split(":")
    print(temp_Arr)
    dictionary[temp_Arr[0]] = float(temp_Arr[1]) if temp_Arr[1].isnumeric else temp_Arr[1]
    
print(dictionary[args[2]])

