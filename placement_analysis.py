import json
# import argparse
import re
import glob
# import pandas

internal_count = 0
external_count = 0
total_placement_count = 0
totalEdgeCount = 0
leafCount = 0
internalCount = 0


def jplace_file_grabber():
    jplace = glob.glob("*.jplace")
    return jplace


def tree_splitter(jplace):
    ##json parse--extract tree string
    tree = jplace["tree"]
    branches = re.split('[, ( )]',tree)  ##splitting at ')' '(' and ',' eliminates all delimiters that are not curly braces--
    # leaves either empty elements ex: u'' or elements withedge numbers/labels/lengths in each element of the list
    return branches


def edge_counter(split_tree):
    # initialize totalEdgeCount at -1 because the root is indicated by a {x} but we dont want to count that in the edgeCount variable
    global totalEdgeCount, leafCount, internalCount
    totalEdgeCount -= 1
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
    return {"internalEdges": internalEdges, "internalCount": internalCount, "leafCount": leafCount,
            "leafEdges": leafEdges}


def number_of_placements(file):
    global total_placement_count
    placements = file['placements']
    total_placement_count += len(placements)
    return (total_placement_count)


def placement_location(file):
    internal_edge_list = edge_counter(file)["internalEdges"]
    leaf_edge_list = edge_counter(file)["leafEdges"]
    placements = file['placements']
    for i in placements:
        placement_edge = i["p"][0][2]  # 2 is a magic number, changes between pplacer runs. Need to add a function to determine index.
        if placement_edge in internal_edge_list:
            global internal_count
            internal_count += 1
        elif placement_edge in leaf_edge_list:
            global external_count
            external_count += 1
    return internal_count, external_count


def internal_vs_leaf():
    jplace_files = jplace_file_grabber()
    for file in jplace_files:
        with open(file) as json_data:
            jplace = json.load(json_data)
        placement_count_total = number_of_placements(jplace)
        placement_int_vs_ext = placement_location(jplace)
    return placement_count_total, placement_int_vs_ext


if __name__ == "__main__":
    with open("jplace_data", "w") as output:
        placement_handle = internal_vs_leaf()
        output.write("Total number of read placements " + str(placement_handle[0]))
        output.write("\n" + "Number of reads placed internally " + str(placement_handle[1][0]))
        output.write("\n" + "Number of reads placed on leafs " + str(placement_handle[1][1]))
