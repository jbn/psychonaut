# repo/src/block-map.ts
# from typing import Dict, List, Tuple, Union
# from multiformats import CID
# from pydantic import BaseModel
# #from placeholder_lexicon import lex_to_ipld, LexValue
# from placeholder_common import data_to_cbor_block


# class Entry(BaseModel):
#     cid: CID
#     bytes: bytes


# class BlockMap:
#     def __init__(self):
#         self.map: Dict[str, bytes] = {}

#     async def add(self, value: LexValue) -> CID:
#         block = await data_to_cbor_block(lex_to_ipld(value))
#         self.set(block.cid, block.bytes)
#         return block.cid

#     def set(self, cid: CID, bytes: bytes) -> None:
#         self.map[cid.to_string()] = bytes

#     def get(self, cid: CID) -> Union[bytes, None]:
#         return self.map.get(cid.to_string())

#     def delete(self, cid: CID) -> None:
#         del self.map[cid.to_string()]

#     def get_many(self, cids: List[CID]) -> Tuple["BlockMap", List[CID]]:
#         missing: List[CID] = []
#         blocks = BlockMap()
#         for cid in cids:
#             got = self.map.get(cid.to_string())
#             if got:
#                 blocks.set(cid, got)
#             else:
#                 missing.append(cid)
#         return blocks, missing

#     def has(self, cid: CID) -> bool:
#         return cid.to_string() in self.map

#     def clear(self) -> None:
#         self.map.clear()

#     def for_each(self, cb) -> None:
#         for key, val in self.map.items():
#             cb(val, CID.parse(key))

#     def entries(self) -> List[Entry]:
#         entries: List[Entry] = []
#         self.for_each(lambda bytes, cid: entries.append(Entry(cid=cid, bytes=bytes)))
#         return entries

#     def cids(self) -> List[CID]:
#         return [entry.cid for entry in self.entries()]

#     def add_map(self, to_add: "BlockMap") -> None:
#         to_add.for_each(lambda bytes, cid: self.set(cid, bytes))

#     def size(self) -> int:
#         return len(self.map)

#     def byte_size(self) -> int:
#         size = 0
#         self.for_each(lambda bytes: size.__add__(len(bytes)))
#         return size

#     def equals(self, other: "BlockMap") -> bool:
#         if self.size() != other.size():
#             return False
#         for entry in self.entries():
#             other_bytes = other.get(entry.cid)
#             if not other_bytes:
#                 return False
#             if entry.bytes != other_bytes:
#                 return False
#         return True
