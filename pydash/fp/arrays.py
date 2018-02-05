import pydash as pyd
from .convert import convert

__all__ = (
    'chunk',
    'compact',
    'concat',
    'difference',
    'difference_by',
    'difference_with',
    'drop',
    'drop_while',
    'drop_right',
    'drop_right_while',
    'duplicates',
    'fill',
    'find_index',
    'find_last_index',
    'flatten',
    'flatten_deep',
    'flatten_depth',
    'from_pairs',
    'head',
    'index_of',
    'initial',
    'intercalate',
    'interleave',
    'intersection',
    'intersection_by',
    'intersection_with',
    'intersperse',
    'last',
    'last_index_of',
    'mapcat',
    'nth',
    'pull',
    'pull_all',
    'pull_all_by',
    'pull_all_with',
    'pull_at',
    'remove',
    'repack',
    'reverse',
    'slice_',
    'sorted_index',
    'sorted_index_by',
    'sorted_index_of',
    'sorted_last_index',
    'sorted_last_index_by',
    'sorted_last_index_of',
    'sorted_uniq',
    'sorted_uniq_by',
    'split_at',
    'tail',
    'take',
    'take_right',
    'take_right_while',
    'take_while',
    'union',
    'union_by',
    'union_with',
    'uniq',
    'uniq_by',
    'uniq_with',
    'unzip',
    'unzip_with',
    'without',
    'xor',
    'xor_by',
    'xor_with',
    'zip_',
    'zip_object',
    'zip_object_deep',
    'zip_with'
)

chunk = convert([1, 0], pyd.chunk)
compact = pyd.compact
concat = convert([0, 1], pyd.concat)
difference = convert([0, 1], pyd.difference)
difference_by = convert([1, 2, 0], pyd.difference_by)
difference_with = convert([1, 2, 0], pyd.difference_with)
drop = convert([1, 0], pyd.drop)
drop_while = convert([1, 0], pyd.drop_while)
drop_right = convert([1, 0], pyd.drop_right)
drop_right_while = convert([1, 0], pyd.drop_right_while)
duplicates = convert([1, 0], pyd.duplicates)
fill = convert([3, 2, 0, 1], pyd.fill)
find_index = convert([1, 0], pyd.find_index)
find_last_index = convert([1, 0], pyd.find_last_index)
flatten = pyd.flatten
flatten_deep = pyd.flatten_deep
flatten_depth = convert([1, 0], pyd.flatten_depth)
from_pairs = pyd.from_pairs
head = pyd.head
index_of = convert([1, 0], pyd.index_of, interpose=False)
initial = pyd.initial
intercalate = convert([1, 0], pyd.intercalate)
interleave = convert([0, 1], pyd.interleave)
intersection = convert([0, 1], pyd.intersection)
intersection_by = convert([1, 2, 0], pyd.intersection_by)
intersection_with = convert([1, 2, 0], pyd.intersection_with)
intersperse = convert([1, 0], pyd.intersperse)
last = pyd.last
last_index_of = convert([1, 0], pyd.last_index_of, interpose=False)
mapcat = convert([1, 0], pyd.mapcat)
nth = convert([1, 0], pyd.nth)
pull = convert([1, 0], pyd.pull, cap=True)
pull_all = convert([1, 0], pyd.pull_all)
pull_all_by = convert([2, 1, 0], pyd.pull_all_by)
pull_all_with = convert([2, 1, 0], pyd.pull_all_with)
pull_at = convert([1, 0], pyd.pull_at, cap=True)
remove = convert([1, 0], pyd.remove)
repack = convert([0, 1], pyd.repack)
reverse = pyd.reverse
slice_ = convert([2, 0, 1], pyd.slice_)
sorted_index = convert([1, 0], pyd.sorted_index)
sorted_index_by = convert([2, 0, 1], pyd.sorted_index_by)
sorted_index_of = convert([1, 0], pyd.sorted_index_of)
sorted_last_index = convert([1, 0], pyd.sorted_last_index)
sorted_last_index_by = convert([2, 0, 1], pyd.sorted_last_index_by)
sorted_last_index_of = convert([1, 0], pyd.sorted_last_index_of)
sorted_uniq = pyd.sorted_uniq
sorted_uniq_by = convert([1, 0], pyd.sorted_uniq_by)
split_at = convert([1, 0], pyd.split_at)
tail = pyd.tail
take = convert([1, 0], pyd.take)
take_right = convert([1, 0], pyd.take_right)
take_right_while = convert([1, 0], pyd.take_right_while)
take_while = convert([1, 0], pyd.take_while)
union = convert([0, 1], pyd.union)
union_by = convert([1, 2, 0], pyd.union_by)
union_with = convert([1, 2, 0], pyd.union_with)
uniq = pyd.uniq
uniq_by = convert([1, 0], pyd.uniq_by)
uniq_with = convert([1, 0], pyd.uniq_with)
unzip = pyd.unzip
unzip_with = convert([1, 0], pyd.unzip_with)
without = convert([1, 0], pyd.without, cap=True)
xor = convert([0, 1], pyd.xor)
xor_by = convert([1, 2, 0], pyd.xor_by)
xor_with = convert([1, 2, 0], pyd.xor_with)
zip_ = convert([0, 1], pyd.zip_)
zip_object = convert([0, 1], pyd.zip_object)
zip_object_deep = convert([0, 1], pyd.zip_object_deep)
zip_with = convert([1, 2, 0], pyd.zip_with)
