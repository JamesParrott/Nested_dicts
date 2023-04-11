
import abc



class DefaultsDictABC(dict, abc.ABC,):
    """ Overrides to support multiple 'default' factories, with 
        the factory function both being passed the key and 
        being selectable depending on the value 
        of the key (and args and kwargs). 
    
        It would be nice to subclass collections.defaultdict, but 
        achieving multiple defaults with it requires something like 
        the code below to swap out .default_factory on the fly, and
        super().__missing__ still prevents passing the key to 
        the chosen factory.  
        
        factories = {'a': list
                    ,'b': int
                    }
        

        def __missing__(self, key):
            tmp = self.default_factory
            self.default_factory = self.factories.get(key, tmp)
            retval = super().__missing__(key)
            self.default_factory = tmp
            return retval

        A concrete DefaultsDictABC is simpler and less brittle.        

    
    """

    @abc.abstractmethod
    def choose_factory(self, key, *args, **kwargs):
        """ Called to provide the factory for a given key
            that constructs the default value for that key 
            (collections.defaultdict.__missing__ does 
            not pass the key). 
        """

    def __getitem__(self, key, *args, **kwargs):
        """ Using a subclass of collections.defaultdict
            requires a lot more code and can easily go wrong (see class docstring).  
            This method override easily implements a multiple-'defaults'dict.
        """
        if key not in self:
            factory = self.choose_factory(key, *args, **kwargs)
            default_val = factory(key)
            self[key] = default_val
            return default_val

        return super().__getitem__(key)



class FromNestedDict(dict):
    """ Simple dict class that can recreate the nested 
        structure passed to the initialiser, replacing the nested 
        dicts with instances of itself (or any subclass).

        The __str__ method returns what this call looks like
        (omitting the class of each nested instance from repr).
    """

    @classmethod
    def from_nested_dict(cls, dict_: dict = None):
        
        if dict_ is None:
            dict_ = {}

        inst = cls()

        for key, val in dict_.items():
            inst[key] = cls.from_nested_dict(val) if isinstance(val, dict) else val
        return inst

    def __str__(self):
        """ e.g. NameOfClass({k1 : v1, k2: {other nested dict})"""
        return f'{self.__class__.__name__}.from_nested_dict({dict.__repr__(self)})'


class NestedDefaultsDict(DefaultsDictABC, FromNestedDict):

    @classmethod
    def choose_factory(cls, key, *args, **kwargs):
        """ This can be done with collections.defaultdict.   
            The subclass NestedTOMLTableOrArrayOfTables
            actually uses key.
        """
        return lambda key: cls()



class ListKeyedDict(FromNestedDict):
    """Treats keys that are lists, as lists of arguments to pass to __getitem__,
       These can be lists of keys naturally, but the final item of the 'key' 
       list may also be an index if a value is a list.    
       
       Nested instances (non-inheriting tree-only-children), must also support 
       __getitem__(list), e.g. if they are also ListKeyedDicts
    """
      
    def __getitem__(self, keys, *args, **kwargs):       
        
        if isinstance(keys, list):
            if not keys:
                raise KeyError(f'Empty list: {keys=}. [] is not a valid key, unlike () ')

            # Handle nesting from list of keys
            if len(keys) >= 2:
                # only pass on array_of_tables to super call of
                # the final element in keys
                nested = super().__getitem__(keys[0])
                return nested.__getitem__(keys[1:], *args, **kwargs)
            else:
                keys = keys[0]
                
                
        return super().__getitem__(keys, *args, **kwargs)


    def __setitem__(self, keys, val):
        if not isinstance(keys, list):
            super().__setitem__(keys, val)
            return
        elif not keys:
            raise KeyError(f'Empty list of {keys=}. [] is not a valid key, unlike () ')

        inst = self[keys[:-1]]
        inst[keys[-1]] = val
        
            
        
class ListOfListKeyedDicts(list):
    def __getitem__(self, keys_or_indices, *args, **kwargs):
        if isinstance(keys_or_indices, list):
            return super().__getitem__(keys_or_indices[0]).__getitem__(keys_or_indices[1:], *args, **kwargs)
        return super().__getitem__(keys_or_indices) 
        

def list_keyed_from_nested_dict_and_lists(nested):
    if isinstance(nested, list):
        return ListOfListKeyedDicts([list_keyed_from_nested_dict_and_lists(item)
                                     for item in nested
                                    ]
                                   )
    if isinstance(nested, dict):
        return ListKeyedDict({k: list_keyed_from_nested_dict_and_lists(v)
                              for k, v in nested.items()
                             }
                            )
    return nested



class ListKeyedNestedDefaultsDict(ListKeyedDict, NestedDefaultsDict):
    pass


class DottedKeyedNestedDefaultsDict(ListKeyedNestedDefaultsDict):
    """ Accepts TOML style dotted keys - e.g. root[parent.child] """


    def __getitem__(self, key, *args, **kwargs):   


        if not isinstance(key, str) or '.' not in key:
            return super().__getitem__(key, *args, **kwargs)

        first, dot, rest = key.partition('.')       
        return super().__getitem__(first).__getitem__(rest, *args, **kwargs)

    def __setitem__(self, key, val):
        if not isinstance(key, str) or '.' not in key:
            super().__setitem__(key, val)
            return
        leading, dot, last = key.rpartition('.')       

        inst = self[leading]
        inst[last] = val

        

class NestedTOMLTableOrArrayOfTables(NestedDefaultsDict):
    """ TOML Table is a nested recursive structure of TOML Tables 
        and Arrays of TOML Tables (ArrayOfTables). 
    """

    @classmethod
    def choose_factory(cls, key, array_of_tables = False):
        if array_of_tables:
            return lambda x: TOMLArrayOfTables(Table = cls)
        return lambda x: cls()

    @staticmethod
    def is_array_of_tables_keys(keys) -> bool:
        if not isinstance(keys, list):
            return False

        if len(keys) != 1:
            return False
        
        return True

    def __getitem__(self, keys, array_of_tables = False):
        # print(f'{keys=}')
        
        if self.is_array_of_tables_keys(keys):
            #
            keys = keys[0]
            array_of_tables = True

        retval = super().__getitem__(keys, array_of_tables)       

        # This is not great.  But a TOML structure always refers to a Root Table, 
        # and this avoids more complicated dunder method magic (and tricky bugs).
        # 
        # Something like this is needed to append a new empty table when 
        # merely referring to the header, not actually calling a method on it.
        if array_of_tables and isinstance(retval, TOMLArrayOfTables):
            return retval.new_table()

        return retval


class TOMLTable(NestedTOMLTableOrArrayOfTables, DottedKeyedNestedDefaultsDict):
    pass



class TOMLListKeyedTable(NestedTOMLTableOrArrayOfTables, ListKeyedNestedDefaultsDict):
    def is_array_of_tables_keys(self, keys) -> bool:

        if not super().is_array_of_tables_keys(keys):
            return False

        # assert isinstance(keys, list) and len(keys) == 1

        return isinstance(keys[0], list)


class TOMLArrayOfTables(ListOfListKeyedDicts):
    """ Intended to be a List[Table]
    """
    def __init__(self, Table, *args, **kwargs):
        self.Table = Table
        super().__init__(*args, **kwargs)

    def new_table(self):
        table = self.Table()
        self.append(table)
        return table

    def __getitem__(self, keys_or_indices, *args, **kwargs):
        try:
            # This will not only pass a key to a dict,
            # but also pass a list of keys and indexes 
            # to a ListKeyedDict.
            return list.__getitem__(self, -1).__getitem__(keys_or_indices, *args, **kwargs)
        except (KeyError, IndexError):
            return super().__getitem__(keys_or_indices)

            
            

