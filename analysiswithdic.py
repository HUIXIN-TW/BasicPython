import sys

def main(csvfile, indexlist, token):
    with open("token.txt", "r") as f:
        if f != token:
            print("Incorrect Password")
            sys.exit(1)
    try:
        # pass parameter to readfile(), then store useful data only as datalist
        datalist=readfile(csvfile, indexlist)
    except:
        print("The file:", csvfile, "is invalid file.")
        return None, None
    
    # sort the data by continent, country, month
    datalist.sort(key=lambda x:(x[0], x[1], x[2]))
    # 1-12 positive cases, calculate by months, 1-12 new deaths, calculate by months
    dict_country, dict_continent=Get_cases(datalist)
    # calculate month avg
    dict_continent=Get_continentAvg(dict_continent)
    dict_country=Get_countryAvg(dict_country)
    # calculate how many days > avg for positive cases
    # calculate how many days > avg for deaths
    dict_continent, dict_country=Get_Days(dict_continent, dict_country, datalist)
    return dict_country, dict_continent

def readfile(filename, indexlist):
    # open the file, read each line except the first line, then close the file.
    infile = open(filename, 'r')
    if indexlist==None: # if indexlist is none, then return None to readfile
        return None
    # read the rest of file
    data = infile.readlines()
    # close the file
    infile.close()
    # set an empty list to store the row of specific index
    clear_data=[]
    # read each line
    for datum in data:
        # split str into list
        itemline=datum.split(',')
        # split date(dd/mm/yyyy) into dd, mm, and yyyy
        # indexlist[2] indicates where the data column is
        date=itemline[indexlist[2]].split('/')
        
        # set an empty list to stroe these data by specific index
        item_data=[]

        for i in indexlist:
            # if data is date, store it as int
            if indexlist.index(i)==2:
                item_data.append(int(date[1]))       
            # check if num is valid
            elif indexlist.index(i)==3 or indexlist.index(i)==4:
                # convert str into num, then append the number.
                # if error, just append(0)
                try:
                    num=int(itemline[i])
                    if num < 0:
                        item_data.append(0)
                    else:
                        item_data.append(num)
                except:
                    item_data.append(0)                   
            # no special concideration, continent and countery, append it to item_data
            else:
                # convert all data into lowercase
                str_name=itemline[i].lower()
                item_data.append(str_name)                
        clear_data.append(item_data)
        # clear list for next item
        item_data=[]
    return clear_data

def Get_cases(datalist):
    # set two empty dictionaries to store the lists
    continent_dict={}
    country_dict={}
    # call each data continent, country, month, newcase, deathcase
    for data in datalist:
        # month as index
        index=data[2]-1
        # if continent_dict[data[0]] does not exist, create a new one.
        # data[0] is continent
        # data[1] is country
        # create new continent_dict[data[0]] include two lists to store new case and death case
        # country_dict[data[1]] includes three lists to store new case, death case and count days
        try:
            if continent_dict[data[0]]==None:
                continue
        except:
            continent_dict[data[0]]=[[0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0]]
        try:    
            if country_dict[data[1]]==None:
                continue
        except:
            country_dict[data[1]]=[[0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0]]
        
        # For continent
        # call values of the dictionary by data[0], continent name
        caselist=continent_dict.get(data[0])
        # divide caselist into newcase and deathcase
        newcaselist=caselist[0]
        deathcaselist=caselist[1]
        
        # newcase has 12 zeros as initial num.
        # call newcase list by month index, then add the data[3] which is new case number
        # insert updated number into corresponding month by index
        update_newcase=newcaselist.pop(index) + data[3]
        newcaselist.insert(index, update_newcase)
        # deathcase has 12 zeros as initial num.
        # call deathcase list by month index, then add the data[4] which is death case number
        # insert updated number into corresponding month by index
        update_deathcase=deathcaselist.pop(index) + data[4]
        deathcaselist.insert(index, update_deathcase)
        # update the list into continent dictionaries
        continent_dict[data[0]]=[newcaselist, deathcaselist]
        
        # For country
        # call values of the dictionary by data[1], conutry name
        caselist2=country_dict.get(data[1])
        # divide caselist into newcase, deathcase, days of the month
        newcaselist2=caselist2[0]
        deathcaselist2=caselist2[1]
        countdays2=caselist2[2]
        # newcase has 12 zeros as initial num.
        # call newcase list by month index, then add the data[3] which is new case number
        # insert updated number into corresponding month by index
        update_newcase2=newcaselist2.pop(index) + data[3]
        newcaselist2.insert(index, update_newcase2)
        # deathcase has 12 zeros as initial num.
        # call deathcase list by month index, then add the data[4] which is death case number
        # insert updated number into corresponding month by index
        update_deathcase2=deathcaselist2.pop(index) + data[4]
        deathcaselist2.insert(index, update_deathcase2)
        # monthday has 12 zeros as initial num.
        # call this list by month index, then add 1 which is valid day
        # insert updated number into corresponding month by index        
        update_countdays2=countdays2.pop(index) + 1
        countdays2.insert(index, update_countdays2)
        # update the list into continent dictionaries
        country_dict[data[1]]=[newcaselist2, deathcaselist2, countdays2]
    return country_dict, continent_dict
    
def Get_continentAvg(dict_continent):
    # default day of each month in year
    monthlist=[31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    # loop continent name
    for continent in dict_continent:
        # use key to get the values, two list indiate the new case and deathcase
        for caselist in dict_continent.get(continent):
            if len(dict_continent.values()) == 4: # once it complete 4 lists, break the loop
                break
            i=0
            updatelist=[]
            # calculate the avg = caselist[i]/monthlist[i], and append it in a new list
            for i in range(12):
                update=round(caselist[i]/monthlist[i], 4)
                updatelist.append(update)
            # append new list after the original list (new case and death case)
            dict_continent[continent]=dict_continent.get(continent) + [updatelist]
    return dict_continent

def Get_countryAvg(dict_conutry):
    # loop conutry name
    for conutry in dict_conutry:
        # use key to get the values, two list indiate the new case and deathcase
        monthlist=dict_conutry.get(conutry)[2]
        # once it assign as monthlist, then del it
        del dict_conutry.get(conutry)[2]
        # use key to get the values, two list indiate the new case and deathcase
        for caselist in dict_conutry.get(conutry):
            if len(dict_conutry.values()) == 4: # once it complete 4 lists, break the loop
                break
            i=0
            updatelist=[]
            # calculate the avg = caselist[i]/monthlist[i], and append it in a new list
            for i in range(12):
                try:
                    update=round(caselist[i]/monthlist[i], 4)
                    updatelist.append(update)
                except:
                    updatelist.append(0)
            # append new list after the original list (new case and death case)
            dict_conutry[conutry]=dict_conutry.get(conutry) + [updatelist]
    return dict_conutry

def Get_Days(dict_continent, dict_country, datalist):
    # call each data continent, country, month, newcase, deathcase
    for data in datalist:
        # month as index
        index=data[2]-1
        # do twice, one for continent, another for country
        for i in range(2):
            # first, use continent dictionary
            if i==0:
                target_dict=dict_continent
            # second, use country dictionary
            else:
                target_dict=dict_country
            # data[0] is continent name
            # data[1] is country name
            keyname=str(data[i])
            # add [[0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0]]
            # for storing day number whose new cases/ death cases is higher than averge
            if len(target_dict[keyname]) < 6:
                target_dict[keyname]=target_dict.get(keyname) + [[0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0]]
            # data[3] is new case
            # target_dict.get(keyname)[2] is the averge of new case for 12 months
            # and use [index] to find the same month with data[3]
            if data[3]>target_dict.get(keyname)[2][index]:
                # target_dict.get(keyname)[4] is to store day number for new case
                countlist=target_dict.get(keyname)[4]
                # use pop and add 1 to count the day as update
                update=countlist.pop(index) + 1
                # insert update into countlist
                countlist.insert(index, update)
                # update target_dict[keyname], only [countlist] is new
                target_dict[keyname]=target_dict.get(keyname)[0:4]+[countlist]+target_dict.get(keyname)[5:]
            # data[4] is death case
            # target_dict.get(keyname)[3] is the averge of death case for 12 months
            # and use [index] to find the same month with data[4]
            if data[4]>target_dict.get(keyname)[3][index]:
                # target_dict.get(keyname)[5] is to store day number for death case
                countlist=target_dict.get(keyname)[5]
                # use pop and add 1 to count the day as update
                update=countlist.pop(index) + 1
                # insert update into countlist
                countlist.insert(index, update)
                # update target_dict[keyname], only [countlist] is new
                target_dict[keyname]=target_dict.get(keyname)[0:5]+[countlist]
            if i==0:
                dict_continent=target_dict
            else:
                dict_country=target_dict
    # discord the averge list, need no more
    for continent in dict_continent:
        dict_continent[continent]=dict_continent.get(continent)[0:2]+dict_continent.get(continent)[4:]
    for country in dict_country:
        dict_country[country]=dict_country.get(country)[0:2]+dict_country.get(country)[4:]
    return dict_continent, dict_country