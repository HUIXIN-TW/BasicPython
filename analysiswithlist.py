def main(csvfile, country, type):
    # open the file, read each line except the first line, then close the file.
    infile = open(csvfile, 'r')
    infile.readline()
    data = infile.readlines()
    infile.close()
    
    # depend on type seleacted
    if type.strip() == "basic":
        # clear data, only remain date and new case
        date_case = clear_data(data, country)
        get_Min = mn1(date_case)
        get_Max = mx1(date_case)
        get_Avg = avg1(date_case)
        get_Std = std1(date_case)
        return get_Min, get_Max, get_Avg, get_Std
    else:
        print("Incorrect Type")
        
def clear_data(data, country):
    # filter useful data by using country, only date and new case can shown
    date_case = []
    for line in data:
        check_location = line.split(",")
        if check_location[2].upper() == country.upper().strip():
            check_date = check_location[3].split("/")
            check_date.append(check_location[4])
            # transform string into int
            # date_case represent [dd, mm, yy, new case] of parameter country
            date_case.append(list(map(int, check_date)))
    return date_case
            
def mn1(date_case):
    min_list = []
    # calculate min by month
    for i in range(1 ,13):
        # set min = population on Earth
        month_min = 7000000000
        for data in date_case:
            if data[1] == i and data[3] != 0:
                month_min = min(data[3], month_min)
        if month_min == 7000000000:
            min_list.append(0)
        else:
            min_list.append(month_min)
    return min_list

def mx1(date_case):
    max_list = []
    # calculate max by month
    for i in range(1 ,13):
        month_max = 0
        for data in date_case:
            if data[1] == i:
                month_max = max(data[3], month_max)
        max_list.append(month_max)
    return max_list

def avg1(date_case):
    avg1_list = []
    # calculate avg by month
    for i in range(1 ,13):
        month_sum = 0
        count = 0
        # sum each new case in ith month
        for data in date_case:
            if data[1] == i:
                month_sum += data[3]
                count = count + 1
        if count == 0:
            avg1_list.append(0)
        else:
            avg1_list.append(round(month_sum/count, 4))
    return avg1_list

def std1(date_case):
    std1_list = []
    avg1_list = avg1(date_case)
    # calculate std by month
    for i in range(1 ,13):
        month_var = 0
        count = 0
        # each new case in ith month minus the average of ith month
        for data in date_case:
            if data[1] == i:
                var = data[3] - avg1_list[i - 1]
                month_var += var*var
                count = count + 1
        if count == 0:
            std1_list.append(0)
        else:
            std1_list.append(round((month_var**0.5)/(count**0.5), 4))
    return std1_list