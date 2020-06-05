import math
from Classes.FileHandling import FileHandler
from decimal import Decimal
from datetime import datetime
highest_private_key = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141


# function to calculate combinatorial combinations 'n choose k'
def combinatorial_choose(n, k):
    return math.factorial(n) // math.factorial(k) // math.factorial(n-k)


# Function to generate the probability sheet for the number of ones a random n1p-length number
def generate_n1p(n1p=256):
    values = []
    comb_sum = 0
    # Delete old file and create header
    f = FileHandler("/Information/Derived Information/n1p" + str(n1p))
    f.first_line("[NUM_ZEROS], [PROBABILITY_FOR_THIS_MANY_ZEROS], [NUMBER_OF_CONFIGURATIONS_WITH_THIS_MANY_ZEROS]\n")
    # Check each sum of possible configurations, and save the sum of all sums.
    for i in range(0, n1p + 1):
        current = combinatorial_choose(n1p, i)
        comb_sum += current
        values.append(current)
    for i in range(0, len(values)):
        probability = values[i]/comb_sum
        line = format(i, '03') + ", "                       # Number of 1's in this configuration.
        line += ('%.10E' % Decimal(probability)) + ", "     # Probability any random number would have this many 1's.
        line += '%.10E' % Decimal(values[i])                # Total number of possible numbers with this many 1's.
        line += "" if i == len(values) - 1 else "\n"
        f.add_line(line)


# Function to calculate the number of different groupings of 1's
def generate_ng1p(n1p_value=128, current=1, stop=129, multipliers=None, file=None, line="", sum=0, groups=0):
    # Base case
    if current > n1p_value or sum == 128:
        return 0
    # Process intensive base case
    if current == stop and sum == 0:
        return 0
    # configure multipliers if necessary [nlp,...,1]
    if multipliers is None:
        multipliers = []
        for i in range(n1p_value, 0, -1):
            multipliers.append(i)
    # configure file if necessary
    if file is None:
        file = FileHandler("/Information/Derived Information/ng1p" + str(n1p_value) + "." + str(multipliers[current-1]))
    # Loop for largest possible size if current is 1
    for i in range(1, n1p_value + 1):
        value = i*multipliers[current - 1]
        # If the value and sum are too big, stop looping.
        if (value + sum) > n1p_value:
            if multipliers[current-1] == 1:
                return 0
            if sum == 0:
                print("Level: " + format(multipliers[current - 1], '03') + datetime.now().strftime(" (%H:%M:%S.%f)"))
                return generate_ng1p(n1p_value=n1p_value, current=current + 1, multipliers=multipliers, file=file, line="", sum=0, groups=0, stop=stop)
            return generate_ng1p(n1p_value=n1p_value, current=current + 1, multipliers=multipliers, file=file, line=line, sum=sum, groups=groups, stop=stop)
        # If value is less than n1p, save it and recurse, then skip to next value.
        elif (value + sum) < n1p_value:
            generate_ng1p(n1p_value=n1p_value, current=current + 1, multipliers=multipliers, file=file, line=line + str(i) + "x" + str(multipliers[current - 1]) + ", ", sum=sum + value, groups=groups + i*1, stop=stop)
        # If value is equal to n1p, save it and loop again.
        elif (value + sum) == n1p_value:
            file.add_line(format(groups + i*1, '03') + ": " + line + str(i) + "x" + str(multipliers[current - 1]) + "\n")
            if multipliers[current - 1] == 1:
                return 0
    return 0

