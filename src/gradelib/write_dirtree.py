"""
https://stackoverflow.com/questions/9618862/how-to-parse-a-directory-structure-into-dictionary
"""

import os
from pprint import pprint
import json
import click
from setuptools_scm import get_version
import flatdict

def set_leaf(tree, branches, leaf):
    """ Set a terminal element to *leaf* within nested dictionaries.
   *branches* defines the path through dictionnaries.

    Example:
    >>> t = {}
    >>> set_leaf(t, ['b1','b2','b3'], 'new_leaf')
    >>> print t
    {'b1': {'b2': {'b3': 'new_leaf'}}}
    """

    if len(branches) == 1:
        tree[branches[0]] = leaf
        return
    if branches[0] not in tree:
        tree[branches[0]] = {}
    set_leaf(tree[branches[0]], branches[1:], leaf)

#version = get_version()
    
@click.command()
@click.argument('startpath',type=click.Path())
@click.argument('json_tree_out',type=click.File(mode='w'))
@click.argument('json_flat_out',type=click.File(mode='w'))
#@click.version_option(version)
def main(startpath,json_tree_out,json_flat_out):
    tree = {}
    for root, dirs, files in os.walk(startpath):
        branches = [startpath]
        if root != startpath:
            branches.extend(os.path.relpath(root, startpath).split('/'))

        set_leaf(tree, branches, dict([(d,{}) for d in dirs]+ \
                                      [(f,None) for f in files]))
    json.dump(tree,json_tree_out,indent=4)
    # https://www.freecodecamp.org/news/how-to-flatten-a-dictionary-in-python-in-4-different-ways/
    d = flatdict.FlatDict(tree,delimiter = '/')
    with open(json_flat_out,'w') as flat:
        json.dump(list(d.keys()),flat, indent=4)

#https://github.com/dpath-maintainers/dpath-python

# Python3 code to demonstrate working of
# Convert String to Nested Dictionaries
# Using loop

def helper_fnc(test_str, sep):
    if sep not in test_str:
	return test_str
    key, val = test_str.split(sep, 1)
    return {key: helper_fnc(val, sep)}

# initializing string
test_str = 'gfg_is_best_for_geeks'

# printing original string
print("The original string is : " + str(test_str))

# initializing separator
sep = '_'

# Convert String to Nested Dictionaries
# Using loop
res = helper_fnc(test_str, sep)

# printing result
print("The nested dictionary is : " + str(res))
