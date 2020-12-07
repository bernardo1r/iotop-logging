#!/usr/bin/env python3
import sys
import os
import stats_iotop

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        if sys.argv[1] not in ("-r", "-w"):
            print("BAD USAGE")
            sys.exit()
                    
        if not os.path.isfile(sys.argv[2]):
            print("invalid file")   
            sys.exit() 
    
        s = stats_iotop.stats_iotop()
        s.update(sys.argv[2])
        
        if sys.argv[1] == "-r":
            print(s.__str__(op="disk_read"))
        else: #sys.argv[1] == "-w":
            print(s)
            
    else:
        print(f"Usage: {__file__} [OPTION] [FILE]\nOptions:\n  -r\tSorts by reads\n  -w\tSorts by writes\n\nOnly works for command iotop -abPqqqok")    

