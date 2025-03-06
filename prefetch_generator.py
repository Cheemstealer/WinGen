import xca #xca library created by GitHub user jborean93 accessible at https://github.com/jborean93/pyxca
import struct 
import os 
import time 
import platform

#obtaining the OS of the machine to produce accurately structured files
OS = platform.system()+platform.release()


def generate_prefetch(executable_name, run_count, last_run_time, accessed_files, OS):

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
    # 60 - executable name
    # 4 - prefetch hash
    # 4 - unknown
    header = struct.pack('I4s',version,b'SCCA')
    print(header)
    print(len(header))
    

    #file information portion differs by version
    #creating file information section for a windows 10 machine
    if version == 30:
        print('windows 10')

generate_prefetch('test.exe', 5, 0, 'xyz', OS)
