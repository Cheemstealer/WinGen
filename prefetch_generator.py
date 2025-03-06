import xca
data = b'cheese balls'
workspace = xca.XpressHuffman()

compressed_data = workspace.compress(data)
print(compressed_data)
decompressed_data = workspace.decompress(compressed_data, len(data))
print(decompressed_data)
