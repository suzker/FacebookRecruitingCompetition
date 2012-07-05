import utilities
'''
output a basic communicative edge adding result
'''

def communicative_basic(train_file, test_file, submission_file, num_predictions):
    '''
    main function
    '''
    
    print ">>> reading the graph from file ...",
    graph = {}
    graph = utilities.read_graph(train_file)
    print " done!"
    print ">> the graph contains %d ndoes" % len(graph)
    
    print ">>> building the edge set ...",
    edgeSet = set()
    nodeCredit = {}
    for node in graph.keys():
        nodeCredit[node] = 0
        for frdNode in graph[node]:
            edgeSet.add((node,frdNode))
    print "done!"
    
    def compareCredit(key):
        '''
        utility function to comapre the two credits given the key
        '''
        return nodeCredit[key]
    
    
    missingEdgeSet = set()
    print ">>> reversing the edge set, computing the credicts of each node and finding missing edges ...",
    for edge in edgeSet:
        if (edge[1], edge[0]) not in edgeSet:
            missingEdgeSet.add((edge[1], edge[0]))
        nodeCredit[edge[1]]+=1
    print " done!"
    
    testResult = {}
    testNodeList = utilities.read_nodes_list(test_file)
    testNodeSet = set(testNodeList)
    print ">> %d test Nodes read." % len(testNodeList)
    print ">>> making the missing edge dictionary for test nodes ...",
    for testNode in testNodeList: # pre-build the dictionary
        testResult[testNode] = []
    
    for edge in missingEdgeSet:
        if (edge[0] in testNodeSet):
            testResult[edge[0]].append(edge[1])
    print " done!"
    
    print ">>> sorting the final results according to node credits ...",
    for testNode in testNodeList:
        testResult[testNode].sort(key=compareCredit, reverse=True)
    print " done!"
    
    print ">>> outputing the final result ...",
    utilities.write_submission_file(submission_file, testNodeList, [testResult[testNode] for testNode in testNodeSet])
    print " done!"
    
if __name__=="__main__":
    communicative_basic("../Data/train.csv",
                  "../Data/test.csv",
                  "../Submissions/communicative_basic.csv",
                  10)