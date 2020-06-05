from Misc.Sanitizers import *


# Decoration to ensure every argument is given in the form of a list of strings.
def ensure_list(func):
    def inner(*args, **kwargs):
        new_kwargs = {}
        for key, value in kwargs.items():
            if not isinstance(value, list):
                if not isinstance(value, str):
                    value = str(value)
                value = [value]
            else:
                for i in range(0,len(value)):
                    value[i] = str(value[i]) if not isinstance(value[i], str) else value[i]
                    value[i] = "NULL" if value[i] == "None" else value[i]
            new_kwargs[key] = value
        return func(*args, **new_kwargs)
    return inner


# Decoration to ensure all list arguments are the correct length
def ensure_list_lengths(func):
    def inner(*args, **kwargs):
        # Ensure 'sql_type is a singular entry
        assert_single_list(dictionary=kwargs, key='sql_type')
        # Ensure that 'table is a singular entry
        assert_single_list(dictionary=kwargs, key='table')
        # Ensure that, if match_columns and matches exist: they are equal
        assert_equivalent_lists(dictionary=kwargs, key_1='match_columns', key_2='matches')
        # Ensure that, if value_columns and values exist: they are equal
        assert_equivalent_lists(dictionary=kwargs, key_1='value_columns', key_2='values')
        # Ensure that string values are quoted
        ensure_quoted(dictionary=kwargs)
        # Ensure that database attributes have backticks
        ensure_backticked(dictionary=kwargs)
        # Run the function
        return func(*args, **kwargs)
    return inner
