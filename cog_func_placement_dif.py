import argparse
import os

import pandas as pd

'''
def get_files(root_directory, extension='.tab'):
    filtered_files = []
    extension_length = len(extension)
    for root, subdirList, files in os.walk(os.path.abspath(root_directory)):
        for name in files:
            if name[-extension_length:] == extension:
                filtered_files.append(os.path.join(root, name))
return filtered_files
'''

"""
def cog_function_groups(file_name):
    open file_name
    create cog_function_group_dict(key = functional group, value = cogs_in_functional_group, col3 = number_of_internal_placements, col4 = number_of_leaf_placements)
    return dict
"""

"""
def list_of_cogs(file_name):
       parse list_of_cog
           for cog in list_of_cogs:
               append cog to cog_function_group_dict(key=functional group, value = cog_name)
"""

"""
def placements_by_functional_group(jplace file):
    cog_placements <- jparser(jplace)
    if cog_name is in cog_function_group_dict:
        cog_function_group <- cog_function_group_dict[value = cog_name]
    for placements in cog_placements:
        if placement is internal:
            cog_function_group_dict[cog_function_group] key:number_of_internal_placements += placement
        if placement is leaf:
            cog_function_group_dict[cog_function_group] key:number_of_leaf_placements += placement
        else:
            error
return cog_function_group dictionary
"""

"""
def function_group_quant(cog_function_group_dictionary):
    func_group <- cog_function_group_dictionary
    for group in func_group:
        total <- func_group[group]:internal +func_group[group]:leaf
        percent_internal <- func_group[group]:interanl/total
        percent_internal <- func_group[group]:leaf/total
        func_group.append(percent_internal)
        func_group.append(percent_leaf)
"""

'''
def func_group_output_file(cog_function_group_dictionary):
    func_group <-cog_function_group_dictionary
    write func_group[functional_group, number_of_internal, number_of_leaf, percent_internal, percent_leaf] as tsv
'''

'''
extraneous python stuff that i don't know yet
'''
