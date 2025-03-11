import xca #xca library created by GitHub user jborean93 accessible at https://github.com/jborean93/pyxca
import struct 
import os 
import time 
import platform
import hashlib
import datetime
import winfiletime  #winfiletime created by GitHub user jleclanche accessible at https://github.com/jleclanche/winfiletime

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

    #splitting the given last run time into it's component parts
    full_split=[]
    part_split= last_run_time.split(',')
    for i in part_split:
       full_split.append(i.split(':'))
    #convert last run time into a python datetime format
    last_run_time = datetime.datetime(int(full_split[0][2]), int(full_split[0][1]), int(full_split[0][0]), int(full_split[1][0]), int(full_split[1][1]),int(full_split[1][2]))
    #comvert the last run time into a windows filetime format
    last_run_time = winfiletime.from_datetime(last_run_time)
    
    #constructing file header
    #header = struct.pack('4sI4s4sI60s4sI',b'MAM\x00',version,b'SCCA',b'0x11',file_size, bytes(file_name, 'utf-16le'), bytes(file_path_hash,'utf-16le'),0)
    #header = struct.pack('4sI',b'MAM\x00',file_size)
    #print(header)
    #print(len(header))
     
    #file information portion differs by version
    #creating file information section for a windows 10 machine
    if version == 30:
        #print('windows 10')
        #file information section 220 bytes in size
        file_metrics_array_offset = 304
        file_metrics_array_entries = 1

        trace_chains_array_offset = file_metrics_array_offset + (file_metrics_array_entries*32)
        trace_chains_array_entries = 1

        file_name_strings_offset = trace_chains_array_offset + (trace_chains_array_entries*8)
        file_name_strings_size = 4

        volume_information_offset = file_name_strings_offset + file_name_strings_size
        number_of_volumes = 1
        volume_information_size = 96

        hash_string_offset = volume_information_offset + (number_of_volumes*volume_information_size)
        hash_string_size = 8

        print(struct.pack('I',file_metrics_array_offset))
        #packing all of the relevant file information together in the correct order
        file_information = struct.pack('<I',file_metrics_array_offset)+struct.pack('<I',file_metrics_array_entries)+struct.pack('<I',trace_chains_array_offset)
        file_information += struct.pack('<I',trace_chains_array_entries) +struct.pack('<I',file_name_strings_offset) +struct.pack('<I', file_name_strings_size)
        file_information +=  struct.pack('<I', volume_information_offset) +struct.pack('<I',number_of_volumes) +struct.pack('<I',volume_information_size)
        file_information += struct.pack('8s',b'') +struct.pack('<Q', last_run_time)
        #prefetch files store up to 8 last run times, here we only want 1 so the rest are zeroed
        for i in range(7):
            file_information+=struct.pack('<Q',0)
        file_information+= struct.pack('16s',b'') + struct.pack('<I',run_count)+struct.pack('8s',b'')
        file_information += struct.pack('<I',hash_string_offset) + struct.pack('<I',hash_string_size) + struct.pack('76s',b'')
        #print(file_information)                                                                    
        #calculate size of uncompressed file                                                                     
        #print(file_size)

        #compress the file information using the Xpress Huffman algorithm
        compressor = xca.XpressHuffman()
        compressed_file_information = compressor.compress(file_information)
        #print(len(compressed_file_information))
        file_size = len(compressed_file_information)
        #setting header
        header = struct.pack('4sI',b'MAM\x04',file_size)

        #combining together into one file
        prefetch_data = header + compressed_file_information
        print(prefetch_data)
        
        
    f = open(prefetch_path + file_name.upper() + '.pf', 'wb')
    f.write(prefetch_data)
    f.close()

generate_prefetch('test.exe', 5, '22:12:2024,10:15:45', 'files accessed', OS, 2000, 'C:/Users/Forensics-User/Documents')
