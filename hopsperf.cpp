#include<iostream>
#include<fstream>
#include<vector>
#include<map>
#include<string>
#include<cstdlib>
#include<algorithm>
#include<stack>
#include<queue>
using namespace std;

struct Graph
{
    int V;
    map<int,vector<int> > adjlist;
}gph;
map<int,int> visited;
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
	}
/*	for(map<int,vector<int> >::iterator it=gph.adjlist.begin();it!=gph.adjlist.end();it++){
		cout<<it->first<<" ";
		for(vector<int>::iterator it2=it->second.begin();it2!=it->second.end();it2++){
			cout<<*it2<<" ";
		}
		cout<<endl;
	}*/
	in.close();
}
map<int,int> bfs(int source)
{
queue<int> que;
que.push(source);
int temp;
int flag=0;
map<int,int> hp;
hp[source] = 0;
while(!que.empty())
    {
    temp=que.front();
    //cout<<"Current Node: "<<temp<<endl;
    que.pop();
    /*if (temp==dest)
    {
        flag=1;
        break;
    }*/
    //cout<<"Current node Not destination, 1 hop added\n";
    visited[temp]=1;
    for(vector<int>::iterator it=gph.adjlist[temp].begin();it!=gph.adjlist[temp].end();it++)
        {
        if(visited[*it]==0)
            {
            //cout<<"Pushing "<<*it<<" to queue\n";
            if(hp.find(*it)==hp.end())hp[*it]=hp[temp]+1;
            hp[*it]=min(hp[*it],hp[temp]+1);
            que.push(*it);
            }
        }
    }
/*if(flag==1)
    return hp[dest];
else
    return -1;*/
return hp;
}

/*map<int,int> perf_anal(int source)
{
    map<int,int> hplist;
    for()
}*/

int main(int argc,char* argv[])
{
	if(argc < 3) return 1;
	get_input(argv[1]);
	//cout<<endl<<endl;
	int hopsum=0;
	int no_of_reachable_nodes;
	//int hops=bfs(2,8);
	int source=atoi(argv[2]);
	map<int,int> hplist = bfs(source);
	//cout<<endl<<hops<<endl;
	for(map<int,int>::iterator it=hplist.begin();it!=hplist.end();it++){
		//cout<<it->first<<" "<<it->second<<endl;
		hopsum+=it->second;
		no_of_reachable_nodes+=1;
	}
    float avghop=float(hopsum)/float(no_of_reachable_nodes);
    	cout<<avghop<<endl;
	/*for(map<int,int>::iterator it=hplist.begin();it!=hplist.end();it++){
		cout<<it->first<<" "<<it->second<<endl;	
	}*/
}

