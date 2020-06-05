from Misc.Error import error


# Function to check dictionaries for items with singular lists.
def assert_single_list(dictionary, key):
    if key in dictionary and len(dictionary[key]) != 1:
        error(key + " is not a single-item list!")


# Function to ensure two specified lists are the same length inside a dictionary
def assert_equivalent_lists(dictionary, key_1, key_2):
    # If both keys are not in the dictionaries, quit
    if key_1 not in dictionary or key_2 not in dictionary:
        return
    if len(dictionary[key_1]) != len(dictionary[key_2]):
        error(key_1 + " is not equal to " + key_2)


# TODO: THIS FUNCTION DOES NOT WORK WHEN THERE ARE MULTIPLE VALUE/MATCH_COLUMNS OF THE SAME NAME
# Function to ensure specific entries are properly quoted in the dictionary
def ensure_quoted(dictionary):
    quotable_values = ['public_key', 'hash', 'private_key', 'type', 'private_key_wif', 'private_key_wif_comp', 'address']
    eligible_columns = ['match_columns', 'value_columns']
    eligible_items = ['matches', 'values']
    for i in range(0, len(eligible_columns)):
        if eligible_columns[i] in dictionary:
            for item in quotable_values:
                # if address in match_columns and its value is not NULL
                if item in dictionary[eligible_columns[i]] and dictionary[eligible_items[i]][dictionary[eligible_columns[i]].index(item)] != "NULL":
                    dictionary[eligible_items[i]][dictionary[eligible_columns[i]].index(item)] = "'" + dictionary[eligible_items[i]][dictionary[eligible_columns[i]].index(item)] + "'"
    return dictionary


# Ensure backticks are added to all column, tables, and other entries
def ensure_backticked(dictionary):
    quoted_values = ['selects', 'table', 'match_columns', 'value_columns']
    for item in quoted_values:
        if item in dictionary:
            # cycle through each subsequent entry and backtick each one.
            for i in range(0, len(dictionary[item])):
                dictionary[item][i] = "`" + dictionary[item][i] + "`"
    return dictionary
