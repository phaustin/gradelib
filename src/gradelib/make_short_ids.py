from collections import defaultdict
def create_keydict(id_list,keylen=3):
    """
    create a dictionary of the form 
    short_id:[ubc_id]
    where the short_id is the last digits of the
    ubc id, sliced [-keylen:]

    if there is more than 1 id with the same last
    digits then the entry will be a length of ubc_ids
    that have those digits in common
    """
    key_dict =  defaultdict(list)
    for the_id in id_list:
        the_key = the_id[-keylen:]
        key_dict[the_key].append(the_id)
    return key_dict

def make_short_ids(key_dict,keylen=3):
    """
    given a dictionary created by create_keydict, recursively
    break all ties by adding extra digits to the key

    Parameters
    ----------

    key_dict:  dictionary mapping short_id:[ubc_id]
               where the list [ubc_id] may contain multiple ids
    keylen:  length of short_id, defaulting to last 3 digits
   
    Returns
    -------

    new_dict: dictinary mapping ubc_id: short_id
     where every short_id is unique
    """
    multi_ids = []
    short_ids = list(key_dict.keys())
    #
    #find all keys with multiple ubc_ids
    #
    for new_id in short_ids:
        if len(key_dict[new_id]) > 1:
            multi_ids.append(new_id)
    #
    # make the short ids longer
    #
    newkeylen=keylen+1
    #
    # rerun the dictionary with the new longer key
    # for those ids in multi_id.  Note that
    # the old key needs to be removed
    #
    for conflicted_id in multi_ids:
        id_list = key_dict[conflicted_id]
        del(key_dict[conflicted_id]) 
        for the_id in id_list: 
            new_key=the_id[-newkeylen:] 
            print(f"collision: generate {new_key=}")
            key_dict[new_key].append(the_id)
    #
    # repeat the iteration  (tbd: use update instead
    # of simply running the whole dictionary)
    # so we don't check any good ideas
    # note the recursive function call if there are still
    # multi_ids that need to be fixed
    #
    multi_ids = []
    short_ids = list(key_dict.keys())
    for new_id in short_ids:
        if len(key_dict[new_id]) > 1:
            multi_ids.append(new_id)
    #
    # final dictionary write if multi_ids is empty
    # need to turn [ubc_id] into ubc_id
    #
    if len(multi_ids) == 0:
        new_dict = {value[0]:key for key,value in key_dict.items()}
        return new_dict
    else:
        keylen=newkeylen
        return make_short_ids(key_dict,keylen=keylen)
