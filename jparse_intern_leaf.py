from __future__ import division
import json
import re
import csv
import os
import glob

internal_count = 0
external_count = 0

internal_placement_count = 0
leaf_placement_count = 0
total_placement_count = 0

def jparser(jplace):
        with open(jpfile) as json_data:

            data = json.load(json_data)

            ##json parse--extract tree string
            tree = data['tree']

            branches = re.split('[, ( )]' , tree)##splitting at ')' '(' and ',' eliminates all delimiters that are not curly braces--
                # leaves either empty elements ex: u'' or elements withedge numbers/labels/lengths in each element of the list

            #initialize totalEdgeCount at -1 because the root is indicated by a {x} but we dont want to count that in the edgeCount variable
            totalEdgeCount = -1
            leafCount = 0
            internalCount = 0
            #initialize lists to place leaf and internal edge numbers
            leafEdges = []
            internalEdges = []

            # i is integer index of each element in list
            # v is value (string) at each index
            for i,v in enumerate(branches):
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


            placements = data['placements'] #placement key in json


            #initialize lists
            leafList = []
            internalList = []
            total_placements = 0
            leafsWithPlacement = []
            internalWithPlacement = []
            # there are i pquery elements in the 'placements list--for loop iterates through each pquery--basically placements[i]
                #each pquery consists of a unicode list of placements (u'p') and short-read names (u'nm')
            for i in placements: #it works, but I am guessing there is a more efficient way to dig deep into a dictionary


                #verify total number of placements in the file
                total_placements += 1
                #i.values() retrieves the values (p and nm) of the unicode list (u'p', u'nm')
                #indeces: [0][0][2]
                    #first [0]: retrieves pquery placements (p) from the [p , nm] list at index i
                    #second [0]: retrieves the first element in the list of potential placements (p) at index i
                        #the first placement listed has the highest posterior probability (this element contains the placement edge)
                    #[2]: the highest probability placement edge is the 3rd element in the placement information
                placement_edge = i.values()[0][0][2]


                #multiplicity is number of reads placed at that edge
                multiplicity = i.values()[1]
                numReads = len(multiplicity)

                #check placement edge number against internal edge list
                if placement_edge in internalEdges:
                    internal_count += 1
                    if placement_edge not in internalWithPlacement:
                        internalWithPlacement.append(placement_edge)
                    smallList = [placement_edge , numReads]
                    internalList.append(smallList)
                #check placement edge number against leaf edge list
                elif placement_edge in leafEdges:
                    external_count += 1
                    if placement_edge not in leafsWithPlacement:
                        leafsWithPlacement.append(placement_edge)
                    smallList = [placement_edge , numReads]
                    leafList.append(smallList)


            newLeafList = [] #this will essentially be an array of [[edge_a, numSequences],[edge_b, numSequences]...etc] without repeating edge numbers
            leafSeqSum = 0
            for i in range(len(leafsWithPlacement)):
                counter = 0 #keeps running tally of sequences placed at edge (leafsWithPlacements[i])
                tempEdgeNum = 0
                for j in range(len(leafList)):
                    if (leafList[j][0] == leafsWithPlacement[i]):# when the first element in leafList[j] equals the element in the list of edges with placements
                        tempEdgeNum = leafsWithPlacement[i]
                        counter += leafList[j][1]
                        leafSeqSum += leafList[j][1]
                pair_edgeSeq = [tempEdgeNum, "leaf", counter]
                newLeafList.append(pair_edgeSeq)


            newInternalList = [] #this will essentially be an array of [[edge_a, numSequences],[edge_b, numSequences]...etc] without repeating edge numbers
            internalSeqSum = 0
            for i in range(len(internalWithPlacement)):
                counter = 0 #keeps running tally of sequences placed at edge (leafsWithPlacements[i])
                tempEdgeNum = 0
                for j in range(len(internalList)):
                    if (internalList[j][0] == internalWithPlacement[i]):# when the first element in leafList[j] equals the element in the list of edges with placements
                        tempEdgeNum = internalWithPlacement[i]
                        counter += internalList[j][1]
                        internalSeqSum += internalList[j][1]
                pair_edgeSeq = [tempEdgeNum, "internal", counter]
                newInternalList.append(pair_edgeSeq)

            allEdges = newLeafList + newInternalList
            allEdges.sort(key=lambda x: x[0])

     #       with open("output.csv", "wb") as f:
     #           writer = csv.writer(f)
     #           writer.writerows(allEdges)
