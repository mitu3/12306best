import requests
import re
import json
from dictfile import address



startd1 ='北京'    #  开始站
endd1 ='天津'        #  到达站
date ='2018-01-11'   #  时间
checi = 'k7727'           #  所有    0
seattype = 0         # 一等座  1   二等座  2   软卧  3    硬卧   4      硬座  5     无座  6    所有  0

from_station =address(startd1)
to_station =address(endd1)



def returnxpath(date, from_station, to_station, checi , seattype):


    url =  'https://kyfw.12306.cn/otn/leftTicket/queryZ?' \
           'leftTicketDTO.train_date={}&'\
          'leftTicketDTO.from_station={}&' \
           'leftTicketDTO.to_station={}&' \
           'purpose_codes=ADULT'.format(date, from_station, to_station)
    print(url)

    req = requests.get(url)
    json_response = req.content.decode('utf-8')  # 获取r的文本 就是一个json字符串
    # 将json字符串转换成dic字典对象
    # raw_trains = req.json()['data']['result']
    dict_json = json.loads(json_response)
    raw_trains = (dict_json['data'])['result']

    alldict = {}
    for raw_train in raw_trains:
        # split切割之后得到的是一个列表
        data_list = raw_train.split("|")
        train_no = data_list[3].lower()
        xpath = data_list[2]
        from_station_code = data_list[6]
        to_station_code = data_list[7]
        from_station_name = ''
        to_station_name = ''
        start_time = data_list[8]
        arrive_time = data_list[9]
        time_duration = data_list[10]
        first_class_seat = data_list[31] or "--"     #    type = 1
        second_class_seat = data_list[30] or "--"    #    type = 2
        soft_sleep = data_list[23] or "--"           #    type = 3
        hard_sleep = data_list[28] or "--"           #    type = 4
        hard_seat = data_list[29] or "--"            #    type = 5
        no_seat = data_list[33] or "--"              #    type = 6
        ddd = data_list[12]
        zhong = [train_no,first_class_seat,second_class_seat,soft_sleep,hard_sleep,hard_seat,
                 no_seat,xpath,from_station_code,to_station_code,start_time,arrive_time,time_duration,ddd]
        alldict[train_no] = zhong


    print(alldict)
    # 判断是否是查询特定车次的信息
    isall = checi
    seattype = seattype
    print(isall,seattype)
    if isall == 0 :
        if seattype == 0 :
            for i in alldict.values():
                for j in range(6):
                    if i[j + 1] != '--' or '无':
                        return i[7]
                    else:
                        return 0
        else:
            for i in alldict.values():
                if i[seattype] != '--' or '无':
                    return i[7]
                else:
                    return 0
    else:
        try:
            if seattype == 0:
                i = alldict[isall]
                if i[seattype] != '--' or '无':
                    return i[7]
                else:
                    return 0

            else:
                i = alldict[isall]
                if i[seattype] != '--' or '无':
                    return i[7]
                else:
                    return 0
        except:
            return 0
# #
#
def run():
    r = returnxpath(date, from_station, to_station ,checi , seattype)

    return r

run()