import sys,commands,os,ast
import pydot
testrun = "--testrun" in sys.argv
#testrun = True
if len(sys.argv) < 3 and not testrun:
  print "Usage: python main.py facebook/<userid> result.txt"
  sys.exit(1)

if not testrun:
  cluster_output = "./results/lastrun/temp_output/results.out"
  input_file = sys.argv[1]
  ouput_file = sys.argv[2] # "./results/lastrun/"+
  userid = str(input_file.split('/')[-1])
else:
  cluster_output = "./results/lastrun/temp_output/results.out"
  input_file = "facebook/698"
  ouput_file = "./results/lastrun/test_results.out"
  userid = str(input_file.split('/')[-1])

#"results/"+str(userid)+"/temp_output"):os.mkdir("results/"+str(userid)+"/temp_output"
if not os.path.isdir("results"):os.mkdir("results")
if not os.path.isdir("results/lastrun"):os.mkdir("results/lastrun")
if not os.path.isdir("results/lastrun/temp_output"):os.mkdir("results/lastrun/temp_output")
if not os.path.isdir("results/"+str(userid)):os.mkdir("results/"+str(userid))
#if not os.path.isdir("results/"+str(userid)+"/temp_output"):os.mkdir("results/"+str(userid)+"/temp_output")


if not testrun:
  print "executing: "+"./cluster "+input_file+" "+cluster_output
  (status,output)=commands.getstatusoutput("./cluster "+input_file+" "+cluster_output)
  if status!=0:print output 
  else: print "done"


user_circles = []
f = open(input_file+".circles",'r')
for line in f:user_circles.append(line.split())
f.close()
user_edges = []
node_edges = {}
f = open(input_file+".edges",'r')
for line in f:
  user_edges.append(line.split())
  if line.split()[0] not in node_edges: node_edges[int(line.split()[0])]=[]
  node_edges[int(line.split()[0])].append(int(line.split()[1]))
f.close()
user_feat = {}
f = open(input_file+".egofeat",'r')
for line in f:user_feat[userid]=line.split()
f.close()
f = open(input_file+".feat",'r')
for line in f:user_feat[line.split()[0]]=line.split()[1:]
f.close()
clusters = []
f = open(cluster_output,'r')
for line in f:
  if line.split()[0] == "clusters":
    clusters = ast.literal_eval(line.split()[-1])
print clusters
cno = 0
central_nodes = set()
cluster_map = {}
for cluster in clusters:
  cno += 1
  cluster_head = str(userid if int(userid) in cluster else cluster[0])
  if not os.path.isdir("./results/lastrun/temp_output/"+str(cno)):os.mkdir("./results/lastrun/temp_output/"+str(cno))
  fedges = open("./results/lastrun/temp_output/"+str(cno)+"/"+cluster_head+".edges",'w')
  fcircles = open("./results/lastrun/temp_output/"+str(cno)+"/"+cluster_head+".circles",'w')
  fegofeat = open("./results/lastrun/temp_output/"+str(cno)+"/"+cluster_head+".egofeat",'w')
  ffeat = open("./results/lastrun/temp_output/"+str(cno)+"/"+cluster_head+".feat",'w')
  for edges in user_edges:
    if int(edges[0]) in cluster and int(edges[1]) in cluster:fedges.write(edges[0]+" "+edges[1]+'\n')
  fedges.close()

  for circles in user_circles:  
    if len(circles)==0:break
    circlename = circles[0]
    new_circles = []
    del circles[0]
    for uid in circles:
      if int(uid) in cluster:
        new_circles.append(uid)
    if len(new_circles) > 0:
      fcircles.write(circlename)
      for item in new_circles:fcircles.write(" "+item)
      fcircles.write("\n")
  fcircles.close()
  if str(cluster_head) in user_feat:
    for item in user_feat[str(cluster_head)]:
      fegofeat.write(item+" ") 
  fegofeat.close()
  for uid in cluster:
    if int(uid) != int(cluster_head):
      ffeat.write(str(uid))
      if str(uid) in user_feat:
        for item in user_feat[str(uid)]:
          ffeat.write(" "+item)
      ffeat.write("\n")
  ffeat.close()

  #Just try and run the first module to recluster this cluster, goal is to make this cluster non overlapping by tweaking the first module using some parameters
  # if len(cluster) > 1000:
  #   print "executing: "+"./cluster temp_output/"+str(cno)+"/"+cluster_head+" temp_output/"+str(cno)+"/results.out"
  #   (status,output)=commands.getstatusoutput("./cluster temp_output/"+str(cno)+"/"+cluster_head+" temp_output/"+str(cno)+"/results.out")
  #   if status!=0:print output 
  #   else: print "done"
  # else:
  print "executing: "+"./spanning results/lastrun/temp_output/"+str(cno)+"/"+cluster_head+".edges"
  (status,output)=commands.getstatusoutput("./spanning results/lastrun/temp_output/"+str(cno)+"/"+cluster_head+".edges")
  if status!=0:print output 
  else: print "done"
  print "Central Node for This cluster: "+str(output)
  central_nodes.add(int(output));
  cluster_map[int(output)]=cluster

print "Set of Target Nodes are ",central_nodes

graph = pydot.Dot(graph_type='graph')

f = open("results/lastrun/output.edges",'w')

for node in central_nodes:
  edge = pydot.Edge("S", str(node))
  f.write("-1\t"+str(node)+"\n")
  graph.add_edge(edge)


pic_edges = set()
for node in central_nodes:
  #for cluster_node in cluster_map[node]:  
  visi = set()
  stk = [node]
  visi.add(node)
  while(len(stk)>0):
    curr = stk.pop()    
    for cluster_node in node_edges[curr]:
      if cluster_node not in visi:
        stk.append(cluster_node)
        visi.add(cluster_node)
        if cluster_node != node and cluster_node in cluster_map[node]:
          edge = (str(curr), str(cluster_node))
          pic_edges.add(edge)

for (curr,cluster_node) in pic_edges:    
  f.write(str(curr)+"\t"+str(cluster_node)+"\n")
  edge = pydot.Edge(str(curr), str(cluster_node))
  graph.add_edge(edge)  
# for node in central_nodes:
#   for cluster_node in cluster_map[node]:
#     if cluster_node not in central_nodes:
#       edge = pydot.Edge(str(node), str(cluster_node))
#       f.write(str(node)+"\t"+str(cluster_node)+"\n")
#       graph.add_edge(edge)

f.close()

graph.write_png('results/lastrun/output_graph.png')
