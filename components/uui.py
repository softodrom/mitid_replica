# Python3 code to generate the 
# random id using uuid1() 
  
import uuid 
import datetime
# import time_uuid
# from cassandra.util import datetime_from_uuid1
  
# Printing random id using uuid1() 
u1 = uuid.UUID("26c27fe4-eaa0-11ec-9ea0-046c59f70eee")
u2 = uuid.UUID("7f03cd50-eaa0-11ec-b3d5-046c59f70eee")
u3 = uuid.UUID("e08a81c6-eaa2-11ec-a056-046c59f70eee")
u = uuid.uuid1()
print ("The random id using uuid1() is : ") 
# print (u.int) 

# datetime.fromtimestamp((request_uuid.time - 0x01b21dd213814000L)*100/1e9)
# ts = time_uuid.TimeUUID(bytes=u.bytes).get_timestamp()
# print(ts)
tes = 0x01b21dd213814000
date = datetime.datetime.fromtimestamp((u1.time - 0x01b21dd213814000)*100/1e9)
date2 = datetime.datetime.fromtimestamp((u2.time - 0x01b21dd213814000)*100/1e9)
date3 = datetime.datetime.fromtimestamp((u3.time - 0x01b21dd213814000)*100/1e9)
# date = datetime.datetime.fromtimestamp(u.time)
print(date)
print(date2)
print(date3)
# dt_foo = datetime_from_uuid1(u)
# print (dt_foo)