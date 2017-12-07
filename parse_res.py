from construct import *


class ArrayAdapter(Adapter):
    def __init__(self, subcon):
        super(ArrayAdapter, self).__init__(subcon)
    def _encode(self, obj, context):
        return obj

    def _decode(self, obj, context):
        for i, con in enumerate(obj):
            con.index = i
        return obj


dir_entry = Struct(
    "chunk_id" / Int16ul,
    "chunk_size_unpacked" / Int24ul,
    "chunk_type" / Enum(Int8ul,
                        flat_uncomp=0x00,
                        flat_comp=0x01,
                        subdir_uncomp=0x02,
                        subdir_comp=0x03),

    "chunk_size_packed" / Int24ul,
    "content_type" / Enum(Int8ul,
                          palette=0x00,
                          text=0x01,
                          bitmap=0x02,
                          font=0x03,
                          video=0x04,
                          sound_effect=0x07,
                          d3d_model=0x0f,
                          audiolog=0x11,
                          map=0x30),
)

chunk_dir_header = Struct(
    "chunks_num" / Int16ul,
    "first_chunk_offset" / Int32ul,
    "dir_entries" / Array(this.chunks_num, dir_entry)
)

chunk_entry = Struct(
    "subchunks_num" / Int16ul,
    "subckunks_offset" / Array(this.subchunks_num, Int32ul),
    "chunk_size" / Int32ul,
    "data" / Bytes(this.chunk_size - this.subchunks_num * 4 - 4 - 2),
)


res_file = Struct(
    "header" / Const(b"LG Res File v2\r\n\x1A" + b"\x00" * 107),
    "dir_offset" / Int32ul,
    "dir_header" / Pointer(this.dir_offset, chunk_dir_header),
    "chunks" / Array(this.dir_header.chunks_num, Aligned(4, chunk_entry))


)


#res_parser1 = res_file.parse_stream(open("res/data/cybstrng.res", "rb"))
res_parser2 = res_file.parse_stream(open("res/data/cybstrng.res-", "rb"))

print(res_parser2)


#for i in res_parser1.dir_header.dir_entries:
#    print(i.chunk_size_unpacked)

#for i in res_parser2.dir_header.dir_entries:
#    print(i.chunk_size_unpacked)