# open the file containing the Elves' Calories
with open('01/calories.txt') as f:
  # read the contents of the file
  calories_string = f.read()

# split the string into a list of lines
lines = calories_string.split('\n')

# create a list to store the Calories for each Elf
elf_calories = []

# create a variable to store the current Elf's total Calories
current_total = 0

# iterate through the list of lines
for line in lines:
  # if the current line is an empty string, store the current Elf's total Calories and reset the total
  if line == "":
    elf_calories.append(current_total)
    current_total = 0
  else:
    # otherwise, add the Calories from the current line to the total
    current_total += int(line)

# store the final Elf's total Calories
elf_calories.append(current_total)

# find the Elf with the most Calories
max_calories = max(elf_calories)
  
# print the total number of Calories carried by the Elf with the most Calories
print(max_calories)

elf_calories.remove(max(elf_calories))
max_calories += max(elf_calories)
elf_calories.remove(max(elf_calories))
max_calories += max(elf_calories)
print(max_calories)
