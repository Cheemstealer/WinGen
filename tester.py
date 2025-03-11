import struct
import xca  # Ensure pyxca is installed

def decompress_prefetch(prefetch_file):
    with open(prefetch_file, "rb") as f:
        data = f.read()

    # Prefetch header starts with 'MAM\x04'
    if not data.startswith(b'MAM\x04'):
        print("❌ Not a valid Prefetch file!")
        return

    # Extract the size of the compressed data from the header (next 4 bytes)
    compressed_data_size = struct.unpack('<I', data[4:8])[0]  # Size of compressed data
    print(compressed_data_size)

    # Extract the compressed data (skip the first 8 bytes of the header)
    compressed_data = data[8:8+compressed_data_size]
    print(len(compressed_data))

    # Decompress the data
    decompressor = xca.XpressHuffman()

    # The decompressed data size is unknown, but we can try to estimate it by looking at the actual file content
    # Let's just try using the size of the decompressed portion from the real prefetch file (for example)
    decompressed_data = decompressor.decompress(compressed_data, compressed_data_size)  # Provide length of the original data

    # Print decompressed size
    print(f"✅ Decompressed Size: {len(decompressed_data)} bytes")

    # Extract last run time and run count
    last_run_time_offset = 120  # Confirm in hex editor
    run_count_offset = 172  # Confirm in hex editor

    last_run_time_raw = struct.unpack("<Q", decompressed_data[last_run_time_offset:last_run_time_offset+8])[0]
    run_count = struct.unpack("<I", decompressed_data[run_count_offset:run_count_offset+4])[0]

    print(f"📅 Last Run Time (Raw FILETIME): {last_run_time_raw}")
    print(f"▶ Run Count: {run_count}")

decompress_prefetch("C:/Windows/Prefetch/COMPATTELRUNNER.EXE-DB97728F.pf")


