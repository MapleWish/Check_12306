import requests
import re
import json
import webbrowser 
from prettytable import PrettyTable

#获取地名与URL简称的对应关系
req = requests.get("https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9063")

#正则表达式处理后，保存到字典list_1中
respond = re.findall(r'([\u4e00-\u9fa5]+)\|([A-Z]+)',req.text)
list_1 = dict(respond)

startstation = input("请输入起点: ")
startstation = list_1[startstation]
endstation = input("请输入终点: ")
endstation = list_1[endstation]
times = input("请输入时间 格式(2000-01-01): ")
kind = input("请输入需要查询的车次类型(如G,D,Z,T,K)（默认全查）:")

#通过API进行来获取Json数据
url = "https://kyfw.12306.cn/otn/leftTicketPrice/query?leftTicketDTO.train_date=%s&leftTicketDTO.from_station=%s&leftTicketDTO.to_station=%s&purpose_codes=ADULT"%(times,startstation,endstation)
respond = requests.get(url)
respond = respond.content.decode()
respond = json.loads(respond)["data"]

#Title
pt = PrettyTable(["车站号","出发站","到达站","出发时间","到达时间","历时","商务座价格","一等座价格","二等座价格","高级软卧价格","软卧一等卧价格","动卧价格","硬卧价格","软座价格","硬座价格","无座价格"])
for i in range(len(respond)):
    source = respond[i]["queryLeftNewDTO"]

    #将Json中价格去0 并转为小数 如: 0575 => 57.5
    if(source["swz_price"]!="--"):
        source["swz_price"]=int(source["swz_price"])/10.0
    if(source["zy_price"]!="--"):
        source["zy_price"]=int(source["zy_price"])/10.0
    if(source["ze_price"]!="--"):
        source["ze_price"]=int(source["ze_price"])/10.0
    if(source["gr_price"]!="--"):
        source["gr_price"]=int(source["gr_price"])/10.0
    if(source["rw_price"]!="--"):
        source["rw_price"]=int(source["rw_price"])/10.0
    if(source["srrb_price"]!="--"):
        source["srrb_price"]=int(source["srrb_price"])/10.0
    if(source["yw_price"]!="--"):
        source["yw_price"]=int(source["yw_price"])/10.0
    if(source["rz_price"]!="--"):
        source["rz_price"]=int(source["rz_price"])/10.0
    if(source["yz_price"]!="--"):
        source["yz_price"]=int(source["yz_price"])/10.0
    if(source["wz_price"]!="--"):
        source["wz_price"]=int(source["wz_price"])/10.0    
    
    #通过kind来确定需要添加内容
    if(kind==''or source["station_train_code"][0]==kind):
    #Content
        pt.add_row([source["station_train_code"],
                    source["from_station_name"],
                    source["to_station_name"],
                    source["start_time"],
                    source["arrive_time"],
                    source["lishi"],
                    source["swz_price"],
                    source["zy_price"],
                    source["ze_price"],
                    source["gr_price"],
                    source["rw_price"],
                    source["srrb_price"],
                    source["yw_price"],
                    source["rz_price"],
                    source["yz_price"],
                    source["wz_price"]
                    ])
print(pt)

#调用Chrome浏览器进行访问
flag = input("若需要跳转至购票页面,请输入Y: ")  
if(flag == "Y"):
    ChromePath = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'              
    webbrowser.register('Chrome', None, webbrowser.BackgroundBrowser(ChromePath)) 
    webbrowser.get('Chrome').open('https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs=%s&ts=%s&date=%s&flag=N,N,Y'%(startstation,endstation,times),new=1,autoraise=True) 
""" 
    车站号 station_train_code
    出发站 from_station_name
    到达站 to_station_name
    出发时间 start_time
    到达时间 arrive_time
    历时 lishi

    商务座数量(是否有) swz_num
    一等座 zy_num
    二等座 ze_num
    高级软卧 gr_num
    软卧一等卧 rw_num
    动卧 srrb_num
    硬卧 yw_num
    软座 rz_num
    硬座 yz_num
    无座 wz_num

 """