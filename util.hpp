#ifndef __UTIL_HPP__
#define __UTIL_HPP__

#include "vector"
#include "set"
#include "map"

#define Scalar float

enum featureType
{
  EGOFEATURES = 0, // Features based on relationship to 
  FRIENDFEATURES = 1,
  BOTH = 2
};

enum lossType
{
  ZEROONE = 0,
  SYMMETRICDIFF = 1,
  FSCORE = 2
};

double inp(std::map<int,int>* x, double* y, int D);
double loss(std::set<int>& l, std::set<int>& lhat, int N);
double totalLoss(std::vector<std::set<int> >& clusters, std::vector<std::set<int> >& chat, int N, int which);

template <typename T> int sgn(T val)
{
  return (val > T(0)) - (val < T(0));
}

std::map<int,int>* makeSparse(int* feat, int D);
void compress(std::vector<int> fol, int* feat, int* res);
void diff(int* f1, int* f2, int D, int* res);

#endif
