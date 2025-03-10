import xca #xca library created by GitHub user jborean93 accessible at https://github.com/jborean93/pyxca
import struct 
import os 
import time 
import platform
import hashlib

#obtaining the OS of the machine to produce accurately structured files
OS = platform.system()+platform.release()


def generate_prefetch(executable_name, run_count, last_run_time, accessed_files, OS, file_size, path):
    prefetch_path = 'C:/Windows/Prefetch/'

    #dictionary containing windows versions and the corresponding identifiers
    format_versions = {'WindowsXP':17, 'Windows2003':17, 'WindowsVista':23, 'Windows7':23, 'Windows8':26, 'Windows10':30}

    #finds OS of machine and assigns the correct identifier
    for entry in format_versions: 
        if entry == OS: 
            version = format_versions[entry]
    #file header same across all versions
    #header consists of 84 bytes
    # 4 - format version
    # 4 - signature
    # 4 - unknown
    # 4 - file size
    # 60 - executable name - name of file.exe - hash of path of executable
    # 4 - prefetch hash
    # 4 - unknown

    #hashing file path using sdbm hash function
    hash_value=0
    for i in path.lower().encode('utf-16le'):
        hash_value = (hash_value * 65599 +i) & 0xFFFFFFFF
    file_path_hash=f"{hash_value:08X}"
    
    file_name = executable_name + '-' +file_path_hash
    file_name_as_bytes = bytes(file_name, 'utf-16le') 
    
    #constructing file header
    #header = struct.pack('4sI4s4sI60s4sI',b'MAM\x00',version,b'SCCA',b'0x11',file_size, bytes(file_name, 'utf-16le'), bytes(file_path_hash,'utf-16le'),0)
    header = struct.pack('4sI',b'MAM\x00',file_size)
    #print(header)
    print(len(header))
    exe_name = struct.pack('64s', executable_name.encode('utf-16le')) 

# Run count and last run time 
    run_info = struct.pack('I', run_count) + struct.pack('Q', int(last_run_time))

  # Accessed files (simplified) 

    files_info = b'' 

    for file in accessed_files: 

        files_info += struct.pack('64s', file.encode('utf-16le')) 

  # Combine all parts 

    prefetch_data = header + exe_name + run_info + files_info
    #print(prefetch_data)
    

    #file information portion differs by version
    #creating file information section for a windows 10 machine
    if version == 30:
        print('windows 10')
        file_metrics_array_offset = 304
        file_metrics_array_entries = 1
        trace_chains_array_offset = file_metrics_array_offset + (file_metrics_array_entries*32)
        trace_chains_array_entries = 1
        file_name_strings_offset = trace_chains_array_offset + (trace_chains_array_entries*8)
        file_name_strings_size = 4
        file_information = struct.pack('III',file_metrics_array_offset, file_metrics_array_entries, trace_chains_array_offset)
    #f = open(prefetch_path + file_name.upper() + '.pf', 'wb')
    #f.write(prefetch_data)
    #f.close()

generate_prefetch('test.exe', 5, 0, 'xyz', OS, 2000, 'C:/Users/Forensics-User/Documents')
