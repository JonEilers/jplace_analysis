#!/usr/bin/python3.5

'''
Abreviations
ff = functional family
ivl = internal vs leaf

'''

import json
import argparse
import re
import os
import pandas as pd


def get_files(root_directory, extension='.jplace'):
    filtered_files = []
    extension_length = len(extension)
    for root, subdirList, files in os.walk(os.path.abspath(root_directory)):
        for name in files:
            if name[-extension_length:] == extension:
                filtered_files.append(os.path.join(root, name))
    return filtered_files


def tree_splitter(jplace):
    tree = jplace["tree"]
    branches = re.split('[, ( )]',tree)  ##splitting at ')' '(' and ',' eliminates all delimiters that are not curly braces--
    # leaves either empty elements ex: u'' or elements withedge numbers/labels/lengths in each element of the list
    return branches


def edge_counter(split_tree):
    internalCount = -1
    totalEdgeCount = -1
    leafCount = 0
    leafEdges = []
    internalEdges = []
    branches = tree_splitter(split_tree)
    # i is integer index of each element in list
    # v is value (string) at each index
    for i, v in enumerate(branches):
        if '{' in v:
            totalEdgeCount += 1
        if "|" in v:
            leafCount += 1
            leaf_edgeNum = int(v.split('{')[1].split('}')[0])
            leafEdges.append(leaf_edgeNum)
        elif v != '':
            internal_edgeNum = int(v.split('{')[1].split('}')[0])
            internalCount += 1
            internalEdges.append(internal_edgeNum)
    return {"internalEdges": internalEdges, "internalCount": internalCount, "leafCount": leafCount,
            "leafEdges": leafEdges}


def number_of_placements(file):
    total_placement_count = 0
    placements = file['placements']
    total_placement_count += len(placements)
    return total_placement_count

def edge_indice(file):
    fields = file["fields"]
    for index, items in enumerate(fields):
        if items == "edge_num":
            return index

def get_cog_metadata(file):
    cog_meta_df = pd.read_table(file, index_col = False)
    return cog_meta_df

def get_cog_func_abv(file):
    func_pd = pd.read_table(file)
    func_fam_abv = func_pd['# Code']
    return func_fam_abv

def create_empty_pd(cog_func_abv_file):
    list = get_cog_func_abv(cog_func_abv_file)
    slength = len(list)
    empty_list = []
    for i in range(0,slength):
        empty_list.append(0)
    empty_dict = {"Internal":empty_list, "Leaf":empty_list, "Total":empty_list}
    func_abv = pd.DataFrame(list )
    empty_pd = pd.DataFrame(empty_dict)
    empty_df = pd.concat([func_abv,empty_pd], axis = 1)
    return empty_df

def get_cog_name(file):
    file_name = os.path.basename(file)
    cog_name = file_name.split('.')[0]  # name of gene is first part of file name
    return(cog_name)

def get_cog_ff(cog_name, cog_metadata):
    cog_data = cog_metadata[cog_metadata['# COG'].isin([cog_name])]
    cog_ff = cog_data['func']
    return cog_ff

def placement_location(file):
    external_count = 0
    internal_count = 0
    internal_edge_list = edge_counter(file)["internalEdges"]
    leaf_edge_list = edge_counter(file)["leafEdges"]
    placements = file['placements']
    edge_index = edge_indice(file)
    for i in placements:
        placement_edge = i["p"][0][edge_index]
        if placement_edge in internal_edge_list:
            internal_count += 1
        elif placement_edge in leaf_edge_list:
            external_count += 1
    return internal_count, external_count


def internal_vs_leaf(dir):
    cog_metadata = get_cog_metadata('cognames2003-2014.tab')
    create_empty_pd('fun2003-2014.tab')
    jplace_files = get_files(dir)
    for file in jplace_files:
        with open(file) as json_data:
            jplace = json.load(json_data)
        placement_count_total = number_of_placements(jplace)
        placement_int_vs_ext = placement_location(jplace)
        cog_name = get_cog_name(file)
        cog_ff = str(get_cog_ff(cog_name, cog_metadata))
        return placement_count_total, placement_int_vs_ext, cog_ff

def output(dir, out_file):
    with open(out_file, "w") as output:
        placement_handle = internal_vs_leaf(dir)
        output.write(placement_handle[2])
        output.write("Total number of read placements " + '\t' + str(placement_handle[0]))
        output.write("\n" + "Number of reads placed internally " + '\t'+ str(placement_handle[1][0]))
        output.write("\n" + "Number of reads placed on leafs " + "\t"+ str(placement_handle[1][1]))
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Count the number of internal placements vs leaf placements on a phylogenetic tree. Takes .jplace files")
    parser.add_argument('-directory', help = 'directory with .jplace files', required = True)
    parser.add_argument('-out_file', help = 'output file (txt formart)', required = True)
    args = parser.parse_args()

    output(dir = args.directory, out_file=args.out_file)

