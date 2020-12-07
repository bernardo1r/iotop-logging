import sys

class stats_iotop:
    ''' ONLY FOR COMMAND iotop -abPqqqok '''


    def __init__(self, dic = {}):
        self.dic = dic
        self.__pad_updated = False

    @staticmethod
    def __sweep(dic, pattern):
        '''iter the dictionary and saves in a list the maximum size of characters of each pattern in pattern list. Pattern list indices must be functions that return an integer '''
         
        max_len = [0]*len(pattern)
        cur_len = [0]*len(pattern)
        
        for _, el in dic.items():
            
            for i in range(len(pattern)):
                cur_len[i] = pattern[i](el)
                
                if cur_len[i] > max_len[i]:
                    max_len[i] = cur_len[i]
                
        return max_len

    def __update_number_info(self):
        self.__max_disk_write = 10
        self.__max_disk_read = 10
        
        pattern = [lambda x: int(len(f"{x['disk_read']:,}")),
                   lambda x: int(len(f"{x['disk_write']:,}"))]
        
        len_disk_read, len_disk_write = stats_iotop.__sweep(self.dic, pattern)
        
        if len_disk_read > self.__max_disk_read:
            self.__max_disk_read = len_disk_read
        
        if len_disk_write > self.__max_disk_write:
            self.__max_disk_write = len_disk_write

    def __str__(self, op = "disk_write"):
        if len(self.dic) == 0:
            return "{}"
            
        if op == "disk_read":
            order = lambda x: x[1]["disk_read"]
        else:
            order = lambda x: x[1]["disk_write"]
 
        dic = sorted(self.dic.items(), key=order, reverse=True)
        
        if not self.__pad_updated:
            self.__update_number_info()
            self.__pad_updated = True
        
        fmt = f"{'disk read':>{self.__max_disk_read+2}}  {'disk write':>{self.__max_disk_write+2}}  name\n"   
        for key, value in dic:
            fmt += f"{value['disk_read']:>{self.__max_disk_read},} K  {value['disk_write']:>{self.__max_disk_write},} K  {key}\n"
            
        return fmt

    @staticmethod
    def buffer():
        ''' reads from stdin, sum stats from same processes and output to stdout\n
            MUST HAVE INPUT FORMAT LIKE iotop -abPqqqok '''
        
        dic = {}
        for line in sys.stdin:
             line = line.strip()
             
             elements = line.split()
             
             if len(elements) == 0:
                continue
             
             name = "".join(elements[11:])
             
             disk_read = int(elements[3].split(".")[0])
             disk_write = int(elements[5].split(".")[0])
             
             if not name in dic:
                dic[name] = {}
                
             dic[name]["disk_read"] = disk_read
             dic[name]["disk_write"] = disk_write   
                
             dic[name]["pid"] = elements[0]
             dic[name]["prio"] = elements[1]
             dic[name]["user"] = elements[2]
             dic[name]["swap"] = elements[7]
             dic[name]["io"] = elements[9]
             
        fmt = stats_iotop.__format_buffer(dic)
             
        print(fmt, end="")
                
    @staticmethod
    def __format_buffer(dic):
        pattern = [lambda x: len(x["pid"]), lambda x: len(x["prio"]), lambda x: len(x["user"]),
                   lambda x: len(f"{x['disk_read']:}"), lambda x: len(f"{x['disk_write']:}"),
                   lambda x: len(x["swap"]), lambda x: len(x["io"])]
        
        max_len = stats_iotop.__sweep(dic, pattern)
        
        fmt = ""
        
        for key, el in dic.items():
            fmt += f"{el['pid']:>{max_len[0]}} {el['prio']:>{max_len[1]}} " + \
                   f"{el['user']:<{max_len[2]}}    {el['disk_read']:>{max_len[3]}} K " + \
                   f"{el['disk_write']:>{max_len[4]}} K {el['swap']:>{max_len[5]}} % " + \
                   f"{el['io']:>{max_len[6]}} % {key}\n"
                   
        return fmt
        
                

    def update(self, file_name):
        ''' accept only standard iotop -abPqqqok output files '''
        self.__pad_updated = False
        
        
        with open(file_name) as file:    
            line_count = 0
            
            for line in file:
                line_count += 1
                        
                line = line.strip()

                elements = line.split()
                try:
                    name = "".join(elements[11:])
                    disk_write = int(elements[5].split(".")[0])
                    disk_read = int(elements[3].split(".")[0])
                    
                except Exception as exc:
                    print(f"Error in line {line_count}:\n{line}")
                    raise exc
                    
                if name in self.dic:
                    self.dic[name]["disk_write"] += disk_write
                    self.dic[name]["disk_read"] += disk_read
                    
                else:
                    self.dic[name] = {}                    
                    self.dic[name]["disk_read"] = disk_read
                    self.dic[name]["disk_write"] = disk_write
                            
