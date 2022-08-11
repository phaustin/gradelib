from collections import defaultdict
import copy
def create_keydict(id_list: list,keylen=3):
    """
    create a dictionary of the form 
    short_id:[ubc_id]
    where the short_id is the last digits of the
    ubc id, sliced [-keylen:]

    if there is more than 1 id with the same last
    digits then the entry will be a length of ubc_ids
    that have those digits in common
    """
    shortid_dict =  defaultdict(list)
    for the_id in id_list:
        the_key = the_id[-keylen:]
        shortid_dict[the_key].append(the_id)
    #
    #find all keys with multiple ubc_ids
    #
    multi_id_dict = {}
    short_ids = list(shortid_dict.keys())
    #
    # move collided ids to multi_id dict
    #
    for new_id in short_ids:
        if len(shortid_dict[new_id]) > 1:
            multi_id_dict[new_id]=shortid_dict.pop(new_id)
    return shortid_dict, multi_id_dict

def make_short_ids(short_ids: dict,multi_ids: dict,keylen=3):
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
    #
    # bump keylen for multi_ids
    #
    print(multi_ids)
    newkeylen=keylen+1
    print(f"{newkeylen=}")
    #
    # rerun the dictionary with the new longer key
    # for those ids in multi_id.  Note that
    # the old key needs to be removed from new_key_dict
    # in third loop below
    #
    new_key_dict=defaultdict(list)
    for conflicted_id, id_list in multi_ids.items():
        if len(id_list) > 1:
            print(f"{conflicted_id=}")
            print(f"{multi_ids=}")
            for the_id in id_list: 
                new_key=the_id[-newkeylen:] 
                print(f"collision: generate {new_key=}")
                new_key_dict[new_key].append(the_id)
        elif len(id_list) == 1:
            #
            # no collision if only 1 item left
            #
            newkeylen -= 1
            the_id = id_list[0]
            new_key=the_id[-newkeylen:] 
            new_key_dict[new_key].append(the_id)
        else:
            raise ValueError("should not be here")
    #
    # now sweep the new keys to see if they have
    # multiple ids
    #
    del_list=[]
    for new_id in new_key_dict.keys():
        # del_list = []
        if len(new_key_dict[new_id]) == 1:
            short_ids[new_id] = new_key_dict[new_id]
            del_list.append(new_id)
    #
    # remove up old keys
    #
    for old_key in del_list:
        del(new_key_dict[old_key])
    #
    # final dictionary write if multi_ids is empty
    # need to turn [ubc_id] into ubc_id
    #
    if len(new_key_dict) == 0:
        new_dict = {value[0]:key for key,value in short_ids.items()}
        return new_dict,new_key_dict
    else:
        multi_ids = copy.deepcopy(new_key_dict)
        new_short_ids = copy.deepcopy(short_ids)
        return make_short_ids(new_short_ids,multi_ids,keylen=newkeylen)

if __name__ =="__main__":
    id_list=['599443','605072','965120','731093','842093']
    keylen=2
    shortid_dict, multiid_dict = create_keydict(id_list,keylen=keylen)
    new_dict, new_key_dict =make_short_ids(shortid_dict,multiid_dict,keylen=keylen)
    print(f"{new_dict=},{new_key_dict=}")
