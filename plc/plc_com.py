import snap7
from snap7 import util
#0x81是输入区，0x82输出区，0x83是M,0x84是db块
#第二个参数是dbnumber，输入输出区域默认为0，db块就是块的序号
#start和size，对于I0.3起始地址为0，对应size为3
#plc.write_area(0x84,1,0,struct.pack('B',4))
#a=plc.read_area(0x84,1,2,2)

class plc_db_com():
    #key parameter for init-------------------------------
    def __init__(self,plc_address='192.168.0.1',db_number=1,db_read_start=0,
    db_read_size=100,db_write_start=100,db_write_size=1):
        self.plc_address=plc_address
        self.db_number=db_number
        self.db_read_start=db_read_start
        self.db_read_size=db_read_size
        self.db_write_start=db_write_start
        self.db_write_size=db_write_size

    #create connection------------------------------------
    def connect(self):
        self.plc=snap7.client.Client()
        try:
            self.plc.connect(self.plc_address,0,1)
        except:
            return False
        else:
            return True
        # return True if self.plc.get_connected else False

    #disconnect
    def disconnect(self):
        if hasattr(self,'plc'):
            self.plc.disconnect()
        
    #read db---------------------------------------------
    def read(self,datatype,*args):
        self.plc2pc_data=self.plc.db_read(self.db_number,self.db_read_start,self.db_read_size)

        if datatype=='bool':
            return util.get_bool(self.plc2pc_data,args[0],args[1])
        elif datatype=='int':
            return util.get_int(self.plc2pc_data,args[0])
        elif datatype==('dint' or 'dword'):
            return util.get_dword(self.plc2pc_data,args[0])
        elif datatype=='real':
            return util.get_real(self.plc2pc_data,args[0])
        elif datatype=='string':
            return util.get_string(self.plc2pc_data,args[0],args[1])

    #write db----------------------------------------------
    def write(self,datatype,*args):
        self.pc2plc_data=self.plc.db_read(self.db_number,self.db_write_start,self.db_write_size)
        if datatype=='bool':
            util.set_bool(self.pc2plc_data,args[0],args[1],args[2])
        elif datatype=='int':
            util.set_int(self.pc2plc_data,args[0],args[1])
        elif datatype==('dint' or 'dword'):
            util.set_dword(self.pc2plc_data,args[0],args[1])
        elif datatype=='real':
            util.set_real(self.pc2plc_data,args[0],args[1])
        elif datatype=='string':
            util.set_string(self.pc2plc_data,args[0],args[1],args[2])

        self.plc.db_write(self.db_number,self.db_write_start,self.pc2plc_data)
