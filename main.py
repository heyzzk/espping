import numpy as np
import matplotlib.pyplot as plt

import datetime as dt

import os
import serial
import json

from threading import Thread
from mac_vendor_lookup import MacLookup
import urllib.request as urllib2
import json
import codecs

#从串口获取到mac（RSSI不管），遍历每个mac，每个查字典，如果已有->update；如果没有->新增。

dev_dict={}
mnf_list=[]

def get_manufacture(mac_address):
    global plt
    try:
      url = "http://macvendors.co/api/"
      request = urllib2.Request(url+mac_address, headers={'User-Agent' : "API Browser"}) 
      response = urllib2.urlopen( request )
      #Fix: json object must be str, not 'bytes'
      reader = codecs.getreader("utf-8")
      obj = json.load(reader(response))
      #return obj['result']['company']
      #plt.text(5,dev_dict[mac_address]-1,obj)
      mnf_list.append([mac_address,obj['result']['company']])
      #print(mnf_list)
    except:
      #TODO:ignore macs without manufacture
      mnf_list.append([mac_address,"FAILED"])
      pass

def wifiinfo_handler(imac):
  cHour = dt.datetime.now().strftime('%H')
  cMin = dt.datetime.now().strftime('%M')
  #print(currentHour,currentMinute)

  #print(imac)
  if(imac in dev_dict):#找出其index，画新点
    #print("update:"+imac+","+dev_dict[imac])
    plt.scatter(int(cHour)+int(cMin)/60, dev_dict[imac])
    plt.pause(0.01)
  else:#新增，画新点
    index=len(dev_dict)*5
    dev_dict[imac]=index
    #print("addnew")
    plt.scatter(int(cHour)+int(cMin)/60, dev_dict[imac])
    plt.text(0.5,dev_dict[imac]-1,imac)
    plt.pause(0.01)
    t = Thread(target=get_manufacture,args=(imac,))
    t.start()
    

  #print(dev_dict)
#--------------------------main-----------------------------
plt.axis([0, 24, 0, 100])
plt.ion()

try:
  portx="COM5"
  bps=115200
  timex=5
  ser=serial.Serial(portx,bps,timeout=timex)

  result=ser.write("I am jack".encode("gbk"))

  while True:
         if ser.in_waiting:
             str=ser.read(ser.in_waiting ).decode("gbk")
             if(str=="exit"):
                 break
             else:
                 if(str[2:8]=="probes" and str[-4:-2]=="]}"):
                   print("blank")
                   continue

                 if(str[2:8]=="probes"):
                   str0=""
                   str0=str
                 elif(str[-4:-2]=="]}"):
                   str0=str0+str
                   #这里得到完整json
                   #os.system("cls")
                   #print(str0)
                   json_str = json.loads(str0)
                   #print(len(json_str['probes']))
                   #print(json_str['probes'][0]['address'])
                   #每个mac传给处理函数
                   print('--------------------------')
                   old=''
                   for i in range(len(json_str['probes'])):
                     if(json_str['probes'][i]['address'] != old and json_str['probes'][i]['rssi']>-50):#排除重复
                       wifiinfo_handler(json_str['probes'][i]['address'])
                       old=json_str['probes'][i]['address']
                       print(old)
                 else:
                   str0=str0+str

         if(len(mnf_list)>0):
           #print(mnf_list[0])
           plt.text(7,dev_dict[mnf_list[0][0]]-1,mnf_list[0][1])
           mnf_list.pop()


  print("---------------")
  ser.close()


except Exception as e:
    print("---异常---：",e)
