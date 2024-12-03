# Load the input into an array
doc = open('input.txt', 'rt')
text = doc.read()
doc.close()

# Read into a 2D array
# iterate thru the text, line by line, then use list() to break the line into individual cells
grid = [list(line) for line in text.strip().split('\n')]

my_numbers_dict = {}
found_number = []
found_number_idx = []
found_symbol_idx = []
found_gear_idx = []
my_gear_parts_dict = {}


# Parse through the grid row by row and identify the numbers
for r, row in enumerate(grid):
    for c, col in enumerate(row):

        cell = grid[r][c]
        # determine if cell is a symbol
        # if not grid[r][c].isnumeric() and grid[r][c] != '.':

        # find a complete number
        if cell.isnumeric():
            if len(found_number) == 0:
                # this is the index of start of the number
                found_number_idx.append(str(r))
                found_number_idx.append(str(c))
            found_number.append(cell)
        else:
            # The cell is either a period or a symbol
            if cell != '.':
                # cell is not a number and not a period, so must be a symbol
                found_symbol_idx.append(str(r) + "," + str(c))

                if cell == '*':
                    # This is a gear so store it's index as well
                    found_gear_idx.append(str(r) + "," + str(c))

            # if we found a symbol and there is a found number, we need to end and record that number
            if len(found_number) > 0:
                # create the key for the dict using row and col values and add it to the dict
                key = ",".join(found_number_idx)
                my_numbers_dict[key] = "".join(found_number)

                # since we added the number, clear it and the index
                found_number.clear()
                found_number_idx.clear()

# if the last number ends on a line without a period, it would get missed
if len(found_number) > 0:
    my_numbers_dict[",".join(found_number_idx)] = "".join(found_number)

print(f"Found Numbers Dict: {my_numbers_dict}")
print(f"Found Symbol Index: {found_symbol_idx}")
print(f"Found Gear Index{found_gear_idx}")

# Now we know where the numbers and symbols are, so loop through the numbers and see if
# there is a symbol above, beside, or below

master_sum = 0
master_gear_ratio_sum = 0

part_numbers = []

for num_idx in my_numbers_dict:
    n = my_numbers_dict[num_idx]
    n_length = len(n)
    c = num_idx.split(',')
    idx_r = c[0]
    idx_c = c[1]

    # number starts at idx_r, idx_c so we need to check for a symbol at
    # above idx_r-1 from idx_c-1 to idx_c+n_Length+1
    # beside r,c-1 and r,c+length+1
    # below r+1,c-1 to r+1,c+length+1

    # start with above

    for tst_r in range(int(idx_r)-1, int(idx_r)+2):
        found_one = False
        for tst_c in range(int(idx_c)-1, int(idx_c)+n_length+1):
            # I don't think I need to test for being out of range since we're just looking at strings
            test_coord = str(tst_r) + "," + str(tst_c)
            if test_coord in found_gear_idx:
                # this number is potentially part of a gear, so check if this coord is already in the dict
                if test_coord in my_gear_parts_dict:
                    first_part = int(my_gear_parts_dict[test_coord])
                    second_part = int(n)
                    gear_ratio = first_part * second_part
                    master_gear_ratio_sum = master_gear_ratio_sum + gear_ratio
                    my_gear_parts_dict.update({test_coord: str(first_part) + "," + str(second_part)})
                else:
                    my_gear_parts_dict[test_coord] = n

            if test_coord in found_symbol_idx:
                # this is a part number so add it to our sum
                found_one = True
                part_numbers.append(n)
                master_sum = master_sum + int(n)
                break
        if found_one:
            # Need to stop looking so we don't double count
            break

print(f"The part numbers are: {part_numbers}")
print(f"The sum of all the part numbers that are next to a symbol is {master_sum}")

print(my_gear_parts_dict)
print(f"The sum of all the gear ratios is {master_gear_ratio_sum}")
