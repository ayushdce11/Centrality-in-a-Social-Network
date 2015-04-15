#ifndef __CLUSTER_HPP__
#define __CLUSTER_HPP__

#include "vector"
#include "set"
#include "map"
#include "utility"
#include "string"
#include "stdio.h"
#include "stdlib.h"
#include "util.hpp"

/** An object representing a graph and its features */
class graphData
{
public:
  void print();
  graphData(char* nodeFeatureFile,
            char* selfFeatureFile,
            char* clusterFile,
            char* edgeFile, int which, int directed);
  ~graphData()
  {
    for (std::map<std::pair<int,int>, std::map<int,int>*>::iterator it = edgeFeatures.begin(); it != edgeFeatures.end(); it ++)
      delete it->second;
  }
  
  std::map<std::string, int> nodeIndex;
  std::map<int, std::string> indexNode;
  
  std::vector<std::set<int> > clusters;
  int nEdgeFeatures;
  int nNodes;
  std::map<std::pair<int,int>, std::map<int,int>*> edgeFeatures;
  std::set<std::pair<int,int> > edgeSet;
  int directed;
};

/** This class contains methods to run the clustering algorithm on a graphData object */
class Cluster
{
public:
  void print(){
    printf("///////////////////////////\n");
    printf("CLUSTER DUMP\n");
    printf("\nnTheta %d",nTheta);
    
    int K = 3,m1,n1;
    n1 = K*gd->nEdgeFeatures;
    m1 = K;

    printf("\ntheta\n");
    for(int i=0;i<n1;i++)printf("%f ",theta[i]);
    printf("\nalpha\n");
    for(int i=0;i<m1;i++)printf("%f ",alpha[i]);
    printf("\nchat ");
    for(int i=0;i<chat.size();i++){
      printf("\n");
      for(std::set<int>::iterator it=chat[i].begin();it!=chat[i].end();it++)
        printf("%d ",*it);
    }
    //gd.print();
    printf("\n///////////////////////////\n");
  }
  Cluster(graphData* gd) : gd(gd)
  {
    theta = NULL;
    alpha = NULL;
  }

  ~Cluster()
  {
    if (theta) delete [] theta;
    if (alpha) delete [] alpha;
  }

  int nTheta;
  double* theta;
  double* alpha;
  std::vector<std::set<int> > chat;
  graphData* gd;

  void train(int K, int reps, int gradientReps, int improveReps, double lambda, int seed, int whichLoss);
  double loglikelihood(double* theta, double* alpha, std::vector<std::set<int> >& chat);
private:
  std::set<int> minimize_graphcuts(int k, int improveReps, int& changed);
  void dl(double* dldt, double* dlda, int K, double lambda);
};

#endif
