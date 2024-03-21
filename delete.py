# Open the file and read the lines
with open('Test5_Real.txt', 'r') as file:
    lines = file.readlines()

# Filter out the blank lines
lines = [line for line in lines if line.strip() != '']

# Write the filtered lines back to the file
with open('Result5.txt', 'w') as file:
    file.writelines(lines)