#!/usr/bin/python
#import sys
import random,math
#class featureType:
EGOFEATURES = 0   # Features based on relationship to 
FRIENDFEATURES = 1
BOTH = 2

#class lossType:
ZEROONE = 0
SYMMETRICDIFF = 1
FSCORE = 2

def sgn(val):
  return int(bool(str(val)>str("0")) - bool(str(val)<str("0")))

def _fopen_(fname, mode):
  """ check that files exist for open """
  try:
    f = open(fname, mode)
  except IOError:
    print "Error: Couldn't open " + fname
    sys.exit(1)
  return f

class graphData
""" An object representing a graph and its features """
  # std::map<std::string, int> nodeIndex;
  # std::map<int, std::string> indexNode;
  # std::vector<std::set<int> > clusters;
  # int nEdgeFeatures;
  # int nNodes;
  # std::map<std::pair<int,int>, std::map<int,int>*> edgeFeatures;
  # std::set<std::pair<int,int> > edgeSet;
  # int directed;
  def __init__(self,nodeFeatureFile, selfFeatureFile, clusterFile, edgeFile, int which, int directed):
  """Load a graph
  char* nodeFeatureFile,
   char* selfFeatureFile,
   char* clusterFile,
   char* edgeFile,
   int which, // What type of features are being used?
   int directed) // Should edges be treated as directed?
   : directed(directed) """
  self.nodeIndex,self.indexNode,self.edgeFeatures = {},{},{}
  self.clusters = []
  self.edgeSet = {}
  nNodeFeatures = 0
  self.directed = directed
  nodeFeatures={}
  simFeatures={}
  #int* selfFeatures;

  # Read node features for the graph
  
  f2 = _fopen_(nodeFeatureFile,'r')

  i = 0
  for line in f:
    line = line.replace('\n','')
    lines_words = lines.split()
    nodeID = lines_words[0]
    del lines_words[0] # to simulate cin(line)>>nodeId to read first word from that line
    if nodeId not in self.nodeIndex:
      print "Got duplicate feature for " + str(nodeID)
      del nodeFeatures[i];

    self.nodeIndex[nodeID] = i;
    self.indexNode[i] = nodeID;
    
    featuresV = []
    
    for lines_word in lines_words  # to simulate reading next words(integers) from that line
      featuresV.append(str(lines_word))

    nNodeFeatures = len(featuresV);
    features = []
    for featuresV_item in featuresV:
      features.append(featuresV_item)
    nodeFeatures[i] = features
    i += 1
  
  self.nNodes = i
  f2.close()
  
  if self.nNodes > 1200:
    print "This code will probably run out of memory with more than 1000 nodes!"
    print "Please see our arxiv paper for more scalable versions of the algorithm: http://arxiv.org/abs/1210.8182"
    print "Delete this line (%s, line %d) to continue" % ("cluster.cpp", 72 + 1)
    sys.exit(0)

  # Read the features of the user who created the graph
  f = _fopen_(selfFeatureFile, "r");
  selfFeatures = [];
  
  selfFeatureFile_words = f.read().replace('\n',' ').split('')
  selfFeatureFile_idx   = 0
  
  for x in range(nNodeFeatures):
    selfFeatures.append(selfFeatureFile_words[selfFeatureFile_idx])
    selfFeatureFile_idx += 1

  f.close()

  for i in range(self.nNodes):
    feature = [None] * nNodeFeatures
    diff(selfFeatures, nodeFeatures[i], nNodeFeatures, feature);
    simFeatures[i] = feature;
  
  # Read the circles
  f = _fopen_(clusterFile, "r");
  clusterFile_text = f.read().split()
  file_idx = 0
  while file_idx < len(clusterFile_text):
    circleName = clusterFile_text[file_idx]
    file_idx = file_idx + 1
    circle = set()
    while True:
      nid = clusterFile_text[file_idx]
      file_idx = file_idx + 1
      nodeID = nid
      if nodeID not in self.nodeIndex:
        print "Got unknown entry in label file: " + str(nodeID)
      else:
        circle.add(self.nodeIndex[nodeID]);
      c = ''
      str_idx = 0
      remaining_clusterFile = ' '.join(clusterFile_text[file_idx:])
      while True:
        c = remaining_clusterFile[str_idx]
        str_idx = str_idx + 1
        if c == '\n': break
        if c >= '0' and c <= '9' :
          #fseek(f, -1, SEEK_CUR);
          str_idx -= 1
          break;
      if c == '\n':
        break
    self.clusters.append(circle);
  
  f.close()

  # Use the appropriate encoding scheme for different feature types
  self.nEdgeFeatures = 1 + nNodeFeatures;
  if which == BOTH :
    self.nEdgeFeatures += nNodeFeatures;
  for i in range(self.nNodes):
    for j in range((0 if self.directed else i+1),self.nNodes):
      if (i == j) continue
      d = [None] * self.nEdgeFeatures
      d[0] = 1
      
      if which == EGOFEATURES :
        diff(simFeatures[i], simFeatures[j], nNodeFeatures, d + 1)
      elif which == FRIENDFEATURES :
        diff(nodeFeatures[i], nodeFeatures[j], nNodeFeatures, d + 1)
      else:
        diff(simFeatures[i], simFeatures[j], nNodeFeatures, d + 1)
        diff(nodeFeatures[i], nodeFeatures[j], nNodeFeatures, d + 1 + nNodeFeatures)

      self.edgeFeatures[(i,j)] = makeSparse(d, self.nEdgeFeatures)
      del d

  # Read the edges for the graph
  f = _fopen_(edgeFile, "r");
  edgeFile_text = f.read().replace('\n',' ').split()
  edgeFile_idx = 0
  while edgeFile_idx < len(edgeFile_text)-1 :
  {
    nID1,nID2 = edgeFile_text[edgeFile_idx],edgeFile_text[edgeFile_idx + 1]
    edgeFile_idx = edgeFile_idx + 1

    self.edgeSet.add((self.nodeIndex[nID1], self.nodeIndex[nID2]))
  }
  del nid1
  del nid2
  f.close()

  for (key,value) in nodeFeatures:
    del value
  for (key,value) in simFeatures:
    del value
  del selfFeatures


  def __del__(self):
    for (key,value) in self.edgeFeatures.items():
      delete value
  

class Cluster:
  def __init__(self,graphData):
    self.theta = None   # is Scalar Object
    self.alpha = None   # is Scalar Object
    self.gd = graphData # is graphData object
    self.nTheta = 0 
    self.chat = []  # this is a list of set of int, use .append(set[]) to add elements
  def __del__(self):
    if self.theta: del self.theta;
    if self.alpha: del self.alpha;

#  int nTheta;
#  Scalar* theta;
#  Scalar* alpha;
#  std::vector<std::set<int> > chat;
#  graphData* gd;

  def train(self,K, reps, gradientReps, improveReps, lambda1, seed, whichLoss): #returns None
    """ Train the model to predict K clusters 
    K, reps, gradientReps, improveReps, seed, whichLoss are int
    lambda1 is Scalar
    """
    self.nTheta = K * self.gd.nEdgeFeatures
    if(self.theta) del self.theta
    if(self.alpha) del self.alpha
    self.theta = [Scalar(0)]*self.nTheta # Array of nTheta elements
    self.alpha = [Scalar(0)]*K      # Array of K      elements*

    #seed_ = seed
    #seedptr = seed

    # Learning rate
    increment = Scalar(1.0/(1.0 * self.gd.nNodes * self.gd.nNodes))

    # Clusters are initially empty
    self.chat = []
    for k in range(K):
      self.chat.append(set())

    random.seed(seed)
    
    for rep in range(reps):
      # If its the first iter or soln is degenerate, randomly initialize the weights
      for k in range(K):
        if reps == 0 or len(self.chat[k]) == 0 or len(self.chat[k]) == self.gd.nNodes :
          self.chat[k].clear()
          for i in range(self.gd.nNodes):
            if random.randint(0,2147483647) % 2 == 0 : self.chat[k].add(i)

          for i in range(self.gd.nEdgeFeatures):
            self.theta[k * self.gd.nEdgeFeatures + i] = 0

          #Now just set a single feature to 1 as a random initializatoin
          self.theta[k * self.gd.nEdgeFeatures + random.randint(0,2147483647) % self.gd.nEdgeFeatures] = 1.0         
          self.alpha = 1

      # Update the latent variables (cluster assingments) in a random order
      order = []
      for k in range(K):
        order.append(k)
      for k in range(K):
        for o in range(K):
          x1,x2 = o,random.randint(0,2147483647) % K
          order[x1],order[x2] = order[x2],order[x1] 
          # Swapping order[x1] & order[x2]

      changed,ll_prev = 0,0
      for order_item in order:
        (self.chat[order_item],changed) = _minimize_graphcuts(order_item,improveReps,changed)
      print "Loss = " + totalLoss(self.gd.clusters,self.chat,self.gd.nNodes,whichLoss)  
      (ll_prev,self.chat) = loglikelihood(self.theta,self.alpha,self.chat)
      if not changed: break

      # Perform Gradient Ascent
      ll = Scalar(0)
      dlda = [Scalar(0.0)]*K
      dldt = [Scalar(0.0)]*self.nTheta

      for unused_iter in range(gradientReps):
        _dl(dldt, dlda, K, lambda1)
        for i in range(self.nTheta):
          self.theta[i] += increment * dldt[i]
        for k in range(K):
          self.alpha[k] += increment * dlda[k]
        print "."
        sys.stdout.flush()
        ll = loglikelihood(self.theta,self.alpha,self.chat)
        
        # If we reduced the objective, undo the update and stop
        if ll < ll_prev :
          for i in range(self.nTheta):
            self.theta[i] -= increment * dldt[i]
          for k in range(K):
            self.alpha[k] += increment * dlda[k]
          ll = ll_prev
          break
        del dlda
        del dldt
        print "ll = "+ll



  def _minimize_graphcuts(self,int k, int improveReps, int& changed):#returns set of int
    # return a tuple of set<int> and changed
    E = len(self.edgeFeatures)
    K = len(chat)
    largestCompleteGraph = 500
    if E > largestCompleteGraph * largestCompleteGraph :
      E = largestCompleteGraph * largestCompleteGraph
    


    return (ans,changed)

  def _dl(self,dldt, dlda, K, lambda1): 
    #returns None
    """ Partial derivatives of log-likelihood 
    dldt, dlda is Scalar*
    lambda1 is Scalar 
    K is int 
    """
    for i in range(self.nTheta): 
      dldt[i] = -lambda1 * sgn(self.theta[i])
    for k in range(K):
      dlda[k] = 0
    inps = [float(0)] * K
    chatFlat = [[]] * K

    for k in range(K):
      chatFlat[k] = [False] * self.gd.nNodes
      for n in range(self.gd.nNodes):
        chatFlat[k][n] = False
        if n not in self.chat[k]:
          chatFlat[k][n] = True
    
    for (e,value) in self.gd.edgeFeatures.items():
      inp_ = Scalar(0)
      e1,e2 = e[0],e[1]
      exists = 1 if e in self.gd.edgeSet else 0
      for k in range(K):
        inps[k] = inp(value,self.theta + k * self.gd.nEdgeFeatures)
        d = Scalar(1 if chatFlat[k][e1] and chatFlat[k][e2] else -alpha[k])
        inp_ += d * inps[k]

      expinp = Scalar(Math.exp(inp_))
      q = Scalar(expInp)/(1+expinp)
      if (math.isnan(q)) q = 1

      for k in range(K):
        d_ = chatFlat[k][e1] and chatFlat[k][e2]
        d = 1 if d_ else -alpha[k]
        for (key1,value1) in value.items():
          if exists:
            dldt[k * self.gd.nEdgeFeatures + i] += d*f
          dldt[k * self.gd.nEdgeFeatures + i] += -d*f*q

        if not d_ : 
          if exists:
            dlda[k] += -inps[k]
          dlda[k] += inps[k] * q
    
    for k in range(K):
      del chatFlat[k]
    del chatFlat
    del inps

  def loglikelihood(self, theta, alpha, chat): 
    #returns (Scalar ,chat)
    """ Compute the log-likelihood of a parameter vector and cluster assignments
    theta, alpha are Scalar*
    chat is std::vector<std::set<int> >&
    """
    K = len(chat)    
    chatFlat = [[]] * K
    for k in range(K):
      chatFlat[k] = [False] * self.gd.nNodes
      for n in range(self.gd->nNodes):
        chatFlat[k][n] = false
        if n in self.chat[k].find(n) :
         chatFlat[k][n] = true

    ll = Scalar(ll)
    for (e,value1) in self.gd.edgeFeatures.items():
      inp_ = Scalar(0)
      e1,e2 = e[0],e[1]
      exists = 1 if e in self.gd.edgeSet else 0
      for k in range(K):
        d = Scalar( 1 if chatFlat[k][e1] and chatFlat[k][e2] else -self.alpha[k])
        inp_ += d * inp(value1, self.theta + k*self.gd.nEdgeFeatures, self.gd.nEdgeFeatures)

      if exists : ll += inp_
      ll_ = math.log(1 + math.exp(inp_))
      ll += -ll_

    if math.isnan(ll):
      print "ll isnan for user"
      sys.exit(1)

    for k in range(K):
      del chatFlat[k]
    del chatFlat
    return ll

