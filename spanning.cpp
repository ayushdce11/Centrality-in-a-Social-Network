#include<iostream>
#include<fstream>
#include<vector>
#include<map>
#include<string>
#include<cstdlib>
#include<algorithm>
#include<stack>
#include<queue>
#include<climits>
using namespace std;

struct Graph
{
    int V;
    map<int,vector<int> > adjlist;
    map<pair<int,int>,int> wt;
    void print(){
    	for(map<int,vector<int> >::iterator it=adjlist.begin();it!=adjlist.end();it++){
			cout<<it->first<<" ";
			for(vector<int>::iterator it2=it->second.begin();it2!=it->second.end();it2++){
				cout<<*it2<<" ";
			}
			cout<<endl;
		}
    }
}gph;
void get_input(char* filename){
	fstream in(filename);
	string s1,s2;
	gph.V = 0;
	while(!in.eof()){
		in>>s1>>s2;
		if(gph.adjlist.find(atoi(s1.c_str()))==gph.adjlist.end() || gph.adjlist.find(atoi(s2.c_str()))==gph.adjlist.end())
		{
			gph.V++;
			if(gph.adjlist.find(atoi(s1.c_str()))==gph.adjlist.end())
				gph.adjlist[atoi(s1.c_str())]=vector<int>();
			if(gph.adjlist.find(atoi(s2.c_str()))==gph.adjlist.end())
				gph.adjlist[atoi(s2.c_str())]=vector<int>();
		}
		if(std::find(gph.adjlist[atoi(s1.c_str())].begin(), gph.adjlist[atoi(s1.c_str())].end(),atoi(s2.c_str()) )==gph.adjlist[atoi(s1.c_str())].end())
			gph.adjlist[atoi(s1.c_str())].push_back(atoi(s2.c_str()));
		if(std::find(gph.adjlist[atoi(s2.c_str())].begin(), gph.adjlist[atoi(s2.c_str())].end(),atoi(s1.c_str()) )==gph.adjlist[atoi(s2.c_str())].end())
			gph.adjlist[atoi(s2.c_str())].push_back(atoi(s1.c_str()));

		gph.wt[make_pair(atoi(s1.c_str()),atoi(s2.c_str()))]=1;
		gph.wt[make_pair(atoi(s2.c_str()),atoi(s1.c_str()))]=1;

	}
	//gph.print();
	in.close();
}
void dfs(int source,Graph &g1,map<int,int> &visited)
{
stack<int> stk;
stk.push(source);
int temp;
while(!stk.empty())
    {
    temp=stk.top();
    stk.pop();
    visited[temp]=1;
    //cout<<endl<<"Node "<<temp<<" is being traversed"<<endl;
    for(vector<int>::iterator it=gph.adjlist[temp].begin();it!=gph.adjlist[temp].end();it++){
        if(visited[*it]==0)
            {
            stk.push(*it);
            //cout<<temp<<","<<*it<<" is added to the graph"<<endl;
            g1.adjlist[temp].push_back(*it);
            g1.adjlist[*it].push_back(temp);
            visited[*it]=1;
            }
        }
   }
}
bool comp(const pair<int,int>& a, const pair<int,int>& b){
          return a.second<b.second?true:false;
}

/*Graph prims(){
	Graph g1;
    g1.V=gph.V;
	vector<pair<int,int> > hp;
	map<int,int> parent,key;
	for(map<int,vector<int> >::iterator it=gph.adjlist.begin();it!=gph.adjlist.end();it++){
		parent[it->first] = -1;
		key[it->first] = INT_MAX;
		if(it==gph.adjlist.begin())key[it->first]=0;
		hp.push_back(make_pair(it->first,key[it->first]));
	}
	while(hp.size()>0){
		make_heap(hp.begin(),hp.end(),comp);
		int u = hp[0].first;
		for(vector<int>::iterator it2=gph.adjlist[u].begin();it2!=gph.adjlist[u].end();it2++){
			int v = *it2;
			if(find(hp.begin(),hp.end(),v)!=hp.end() && gph.wt[make_pair(u,v)]<key[v]){
				key[v] = gph.wt[make_pair(u,v)];
				parent[v] = u;
			}
		}
	}	
}*/
Graph get_spantree()
{
    Graph g1;
    g1.V=gph.V;
    map<int,int> visited;
    visited.clear();
    for(map<int,vector<int> >::iterator it=gph.adjlist.begin();it!=gph.adjlist.end();it++){
        visited[it->first]=0;
	}
    for(map<int,vector<int> >::iterator it=gph.adjlist.begin();it!=gph.adjlist.end();it++){
        if(visited[it->first]==0)
            {
            	dfs(it->first,g1,visited);
            }
	}
return g1;
}
int main(int argc,char* argv[]){
	char* edges_input;
	if(argc<2){
		edges_input = "temp_output/1/test.edges";
		//cout<<"using "<<"temp_output/1/861.edges"<<" as input"<<endl;
	}
	else edges_input = argv[1];
	get_input(edges_input);
	Graph g=get_spantree();
	//cout<<endl<<endl;
	//g.print();

	// Do Topological Sort to get the Central Node
	queue<int> q;
	bool flag;
	int prev=-1;
	do{
		flag=false;
		for(map<int,vector<int> >::iterator it=g.adjlist.begin();it!=g.adjlist.end();it++){
				if(it->second.size()==1){					
					prev=it->second[0];
					flag=true;					
					g.adjlist[prev].erase(remove(g.adjlist[prev].begin(), g.adjlist[prev].end(), it->first), g.adjlist[prev].end());
					it->second.clear();
				}
		}
	}while(flag);
	cout<<prev;
}