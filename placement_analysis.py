import json
#import argparse
import re
#import os
import glob
#import pandas

internal_count = 0
external_count = 0

internal_placement_count = 0
leaf_placement_count = 0
total_placement_count = 0  # initialize lists
leafList = []
internalList = []
leafsWithPlacement = []
internalWithPlacement = []

def jplace_file_grabber():
    jplace = glob.glob("*.jplace")
    return jplace

def tree_splitter(jplace):
    ##json parse--extract tree string
    tree = jplace["tree"]
    branches = re.split('[, ( )]',tree)  ##splitting at ')' '(' and ',' eliminates all delimiters that are not curly braces--
    # leaves either empty elements ex: u'' or elements withedge numbers/labels/lengths in each element of the list
    return branches
    print(branches)

def edge_counter(split_tree):
    # initialize totalEdgeCount at -1 because the root is indicated by a {x} but we dont want to count that in the edgeCount variable
    totalEdgeCount = -1
    leafCount = 0
    internalCount = 0
    # initialize lists to place leaf and internal edge numbers
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
    return internalEdges, internalCount, leafCount, leafEdges
    # there are i pquery elements in the 'placements list--for loop iterates through each pquery--basically placements[i]
    # each pquery consists of a unicode list of placements (u'p') and short-read names (u'nm')

def number_of_placements(file):
    total_placements = 0
    placements = file['placements']  # placement key in json
    for i in placements:
    #  verify total number of placements in the file
        total_placements += 1

            # multiplicity is number of reads placed at that edge
        multiplicity = i.values()[1]
        numReads = len(multiplicity)
    return (numReads, total_placements, leafCount, internalCount)

def num_internal_placements(file):
    internal_edge_list = edge_counter(file)[internalEdges]
    placements = file['placements']
    for i in placements:
        placement_edge = i.values()[0][0][2]

        # i.values() retrieves the values (p and nm) of the unicode list (u'p', u'nm')
        # indeces: [0][0][2]
        # first [0]: retrieves pquery placements (p) from the [p , nm] list at index i
        # second [0]: retrieves the first element in the list of potential placements (p) at index i
        # the first placement listed has the highest posterior probability (this element contains the placement edge)
        # [2]: the highest probability placement edge is the 3rd element in the placement information

    # check placement edge number against internal edge list
    if placement_edge in internal_edge_list:
        internal_count += 1
        if placement_edge not in internalWithPlacement:
            internalWithPlacement.append(placement_edge)
        smallList = [placement_edge, numReads]
        internalList.append(smallList)
    # check placement edge number against leaf edge list
    elif placement_edge in leafEdges:
        external_count += 1
        if placement_edge not in leafsWithPlacement:
            leafsWithPlacement.append(placement_edge)
        smallList = [placement_edge, numReads]
        leafList.append(smallList)

    internal_placement_count += internalSeqSum
    leaf_placement_count += leafSeqSum
    total_placement_count += total_placements

def internal_vs_leaf():
    jplace_files = jplace_file_grabber()
    for file in jplace_files:
        with open(file) as json_data:
            jplace = json.load(json_data)

        tree_counts = edge_counter(jplace)
        placement_count = number_of_placements(jplace)
    return placement_count, tree_counts




if __name__ == "__main__":
    internal_vs_leaf()
