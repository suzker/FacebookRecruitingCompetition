import utilities
'''
output a commutual + mutual following w/ simple node credit result
@author: Zhiliang SU (suzker) zsu2 [at] buffalo [dot] edu
'''

def get_node_credit(edgeSet, nodeSet):
    '''
    compute the node credit according to the edgeSet 
    (siplified version, number of followers)
    '''
    nodeCredit = get_empty_dict(nodeSet, 'zero')
    print ">>> computing node credits ...",
    for edge in edgeSet:
        nodeCredit[edge[1]]+=1
    print " done!"
    return nodeCredit

def get_edge_set(graph):
    '''
    utility to get the edge set out of a graph
    '''
    print ">>> building the edge set ...",
    edgeSet = set()
    for node in graph.keys():
        for frdNode in graph[node]:
            edgeSet.add((node,frdNode))
    print " done!"
    return edgeSet

def get_empty_dict(nodeSet, type):
    '''
    returns an empty dictionary with full key sets from a node set
    '''
    emptyDict = {}
    for node in nodeSet:
        if type == 'zero':
            emptyDict[node] = 0
        else:
            emptyDict[node] = []
    return emptyDict

def get_reverse_relationship_graph(edgeSet, nodeSetFull):
    '''
    utility to get a reverse relationship (e.g, from following to follower) graph from a set of edges
    '''
    print ">>> building the reversed relationships graph ..."
    reversedGraph = get_empty_dict(nodeSetFull, 'list')
    for edge in edgeSet:
        reversedGraph[edge[1]].append(edge[0])
    print " done!"
    return reversedGraph

def get_commu_missing_edge(edgeSet, testNodeList):
    '''
    to get a missing edge set in order to make a graph fully commutual
    '''
    missingEdgeSet = set()
    print ">>> finding missing edges for commutual graph ...",
    for edge in edgeSet:
        if (edge[1], edge[0]) not in edgeSet:
            missingEdgeSet.add((edge[1], edge[0]))
    
    testNodeSet = set(testNodeList)
    missingEdgeDict = get_empty_dict(testNodeList, 'list')
    for edge in missingEdgeSet:
        if (edge[0] in testNodeSet):
            missingEdgeDict[edge[0]].append(edge[1])
    print " done!"
    return missingEdgeDict
    
def get_mutual_missing_edge(followingGraph, testNodeList, edgeSet, nodeSetFull, minMutualFrd):
    '''
    to get a missing edge set in which are friends who have the mutual followings
    '''
    
    def get_mutual_count(mutual_list):
        '''
        to get a count dict for all mutual followings list
        '''
        exclusiveSet = set(mutual_list)
        mutualCount = get_empty_dict(exclusiveSet, 'zero')
        for node in mutual_list:
            mutualCount[node] += 1
        return mutualCount
    
    def get_mutual_list(followingList, followerGraph):
        '''
        to get the mutual list out of a graph
        '''
        mutual_list = []
        for node in followingList:
            mutual_list.extend(followerGraph[node])
        return mutual_list
    
    def reverse_dict(dict):
        '''
        to reverse a dict, key-value ---> value-key
        '''
        reversed_dict = {}
        for key in dict.keys():
            reversed_dict[dict[key]] = key
        return reversed_dict
    
    print ">>> finding missing edges for mutual graph ...",
    followerGraph = get_reverse_relationship_graph(edgeSet, nodeSetFull)
    
    missingEdgeDict = get_empty_dict(testNodeList, 'list')
    # generate missing edge dict
    for node in testNodeList:
        mutualCount = get_mutual_count(get_mutual_list(followingGraph[node], followerGraph))
        # reverse the dict :)
        mutualCountReverse = reverse_dict(mutualCount)
        # sort keys
        sortedNumMutualFollowingList = sorted(list(mutualCountReverse.keys()))
        # get sorted nodes according to the sorted keys
        sortedNodeList = []
        for count in sortedNumMutualFollowingList:
            if count >= minMutualFrd:
                sortedNodeList.append(mutualCountReverse[count])
        # map to test node
        missingEdgeDict[node] = sortedNodeList
    print " done!"
    return missingEdgeDict
    
def main_entrance(train_data_file, test_data_file, submit_data_file):
    '''
    the main entrance of the program
    '''
    ###############Configs#################
    minMutualFrd = 2
    ############End of Configs#############
    
    print ">>> reading the graph from file ...",
    following_graph = utilities.read_graph(train_data_file)
    print " done!"
    print ">> the graph contains %d ndoes" % len(following_graph)
    
    print ">>> reading test nodes ...",
    testNodeList = utilities.read_nodes_list(test_data_file)
    print " done!"
    
    edgeSet = get_edge_set(following_graph)
    nodeCredit = get_node_credit(edgeSet, following_graph.keys())
    commu_missingEdgeDict = get_commu_missing_edge(edgeSet, testNodeList)
    mutual_missingEdgeDict = get_mutual_missing_edge(following_graph, testNodeList, edgeSet, following_graph.keys(), minMutualFrd)
    
    # union two edge dicts
    finalPrediction = {}
    for node in testNodeList:
        finalPrediction[node] = list(set(mutual_missingEdgeDict[node]) | set(commu_missingEdgeDict[node]))
    
    # customized comparator for final prediction
    def compareCredit(key):
        '''
        utility function to comapre the two credits given the key
        '''
        return nodeCredit[key]
    
    # rank the predictions
    print ">>> sorting the final results according to node credits ...",
    for testNode in testNodeList:
        finalPrediction[testNode].sort(key=compareCredit, reverse=True)
    print " done!"
    
    # write prediction to file
    print ">>> outputing the final result ...",
    utilities.write_submission_file(submit_data_file, testNodeList, [finalPrediction[testNode] for testNode in testNodeList])
    print " done!"
    
if __name__=="__main__":
    main_entrance("../Data/train.csv",
                  "../Data/test.csv",
                  "../Submissions/commutual_mutual_simplenodecredit.csv")