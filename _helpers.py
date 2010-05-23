def split_values(values):
    if '/' in values:
        values_list = [values_part.split() for values_part in values.split('/')]
    else:
        values_list = [values.split()]

    full_lists = []
    for values in values_list:
        if len(values) == 1:
            values = 4 * [values[0]]
        elif len(values) == 2:
            values = 2 * [values[0], values[1]]
        elif len(values) == 3:
            values = [values[0], values[1], values[2], values[1]]
        full_lists.append(values)

    return zip(*full_lists)
