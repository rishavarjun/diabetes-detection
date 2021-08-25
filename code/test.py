import re

str = "***'diabetes-detection-monitor-via-aml_1629920362_04ed9ee5': ***'testing_value': 15, 'pradeep_fresh_data_accuracy': 0.456***"

#result = re.sub('/[^0-9.]/g', '', str)

list_of_char = ["*", " ", "'"]
pattern = '[' + ''.join(list_of_char) + ']'
# Remove characters matched by pattern
result = re.sub(pattern, '', str)

#--

arr = result.split(':')
input_string = ':'.join(arr[1:])

cleaned_string = input_string

#print("cleaned string =",cleaned_string)
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
    
print(dictionary["pradeep_fresh_data_accuracy"])
