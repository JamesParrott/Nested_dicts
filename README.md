# Nested Dicts

Python multiple-default dicts, list-keyed dicts, dotted-key dicts and Arrays of Tables classes.

*pip install nested_dicts*


## Examples

### DefaultsDictABC
Implement the choose_factory method on a subclass 
to select a factory.  The returned factory is itself 
called with the key value (unlike collections.defaultdict.__missing__)

*The following 4 examples all define a dictionary subclass `d` for which
`d == {'k': {'sub_dict_key': 'v'}}` is True.*

### NestedDefaultsDict
```
>>> d = NestedDefaultsDict()
>>> d['k']['sub_dict_key'] = 'v'
```

### ListKeyedDict
```
>>> d = ListKeyedDict.from_nested_dict({'k': {'sub_dict_key': 'v'}})
>>> d[['k', 'sub_dict_key']]
'v'
```

### ListKeyedNestedDefaultsDict
```
>>> d = ListKeyedNestedDefaultsDict()
>>> d[['k', 'sub_dict_key']] = 'v'
```

### DottedKeyedNestedDefaultsDict
```
>>> d = DottedKeyedNestedDefaultsDict()
>>> d['k.sub_dict_key'] = 'v'
```

### [TOMLTable](https://toml.io/en/v1.0.0#table)
```
>>> from nested_dicts import TOMLTable
>>> t = TOMLTable()
>>> t['table-1'].update(
... key1 = "some string",
... key2 = 123)

>>> t['table-2'].update(
... key1 = "another string",
... key2 = 456)
>>> t
{'table-1': {'key1': 'some string', 'key2': 123}, 'table-2': {'key1': 'another string', 'key2': 456}}
```

Values in TOMLTable()s indexed with lists behave like [Arrays of Tables](https://toml.io/en/v1.0.0#array-of-tables),
even when only read
```
>>> from nested_dicts import TOMLTable
>>> t = TOMLTable()
>>> t[['products']].update(
name = "Hammer",
sku = 738594937
)

>>> t[['products']]  # empty table within the array
{}
>>> t[['products']].update(
name = "Nail",
sku = 284758393,

color = "gray"
)


>>> t
{'products': [{'name': 'Hammer', 'sku': 738594937}, {}, {'name': 'Nail', 'sku': 284758393, 'color': 'gray'}]}
```
