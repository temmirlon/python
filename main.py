import re

a = "apple orange apple banana"

pattern = "apple"
repl = "grape"

# a way to modify strings by replacing specific patterns
# Replace all occurrences of 'apple' with 'grape'
result = re.sub(pattern, repl, a)

print(result)