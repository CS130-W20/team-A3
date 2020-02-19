'''
Creator: Zijie Huang
Data: Feb/18/2020
Description: Parse the original course_taxonomy into sturctured data.
'''

def get_name_prioirty(line):
    category_name = line.split(".")[1].lstrip()
    priority = int((len(line.split(".")[0]) -1)/3.0)
    return category_name, priority

def dict_for_single_record(fields,values):
    dict_tmp = dict()
    for i in range(len(fields)):
        dict_tmp[fields[i]] = values[i]
    return dict_tmp



def generate_course_list(input_file):
    # input
    fields = ['id', 'category_name', 'sub_categories']

    # initialization
    data = dict()
    data_2_priority = dict()
    data_2_idlist = dict()
    f = open(input_file, 'r')
    lines = f.readlines()
    priority_max = 0


    for line_num, line in enumerate(lines):
        line = line.rstrip("\r\n")
        category_name, priority = get_name_prioirty(line)
        data_2_priority[line_num] = priority
        values = [line_num, category_name, []]
        dict_tmp = dict_for_single_record(fields, values)
        data[line_num] = dict_tmp
        if priority == priority_max: ## renew the hierarchy dictionary
            priority_current = dict()
            priority_current[priority] = line_num
            continue
        else: ### append leafs to the root
            priority_current[priority] = line_num
            if priority_current[priority-1] in data_2_idlist.keys():
                tmp = data_2_idlist[priority_current[priority-1]]
                tmp.append(line_num)
            else:
                data_2_idlist[priority_current[priority - 1]] = [line_num]

    f.close()

    for k, v in sorted(data_2_priority.items(), key=lambda item: item[1], reverse = True):
        if v == max(data_2_priority.values()):
            continue
        if k not in data_2_idlist.keys():
            continue
        leaf_list = data_2_idlist[k]
        new_list = []
        for id in leaf_list:
            new_list.append(data[id])
        data[k]["sub_categories"] = new_list


    data_new = list()
    for k,v in data.items():
        if data_2_priority[k] == priority_max:
            data_new.append(data[k])

    return data_new













