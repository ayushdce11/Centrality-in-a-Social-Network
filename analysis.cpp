#include<iostream>
#include<fstream>
#include<map>
#include<stack>
#include<vector>
#include<algorithm>
using namespace std;

struct node{
	int id;
	vector<int> alist;
	node(){
		id=-999;
	}
	node(int i){
		id = i;		
	}
};	
map<int,node> nodes;

void dfs(int src, int &no_of_hops, int &no_of_messages);

int main(int argc,char* argv[]){
	string input_file = "output.edges";
	if(argc < 2){
		cout<<"Expected 1 argument \nUsage: "<<argv[0]<<" output.edges"<<endl;
		cout<<"Continue with "<<input_file<<" as input ?(y/n)"<<endl;
		char c;
		cin>>c;
		if(c!='y' && c!='Y')exit(1);
	}
	else input_file = argv[1];

	fstream in(input_file.c_str());
	int a,b;
	int no_of_hops,no_of_messages,no_of_nodes,no_of_edges;
	no_of_nodes=no_of_edges=0;
	while(!in.eof()){
		in>>a>>b;
		// Create nodes for a and b if not already present
		if(nodes.find(a)==nodes.end()){
			nodes[a]=node(a);
			no_of_nodes++;
		}
		if(nodes.find(b)==nodes.end()){
			nodes[b]=node(b);
			no_of_nodes++;
		}		

		no_of_edges++;

		if(find(nodes[a].alist.begin(),nodes[a].alist.end(),b)==nodes[a].alist.end())nodes[a].alist.push_back(b);
		//if(find(nodes[b].alist.begin(),nodes[b].alist.end(),a)==nodes[b].alist.end())nodes[b].alist.push_back(a);
	}
	cout<<"# of nodes: "<<no_of_nodes<<endl<<"# of edges: "<<no_of_edges<<endl;
	/*for(map<int,node>::iterator i = nodes.begin();i!=nodes.end();i++){
		cout<<endl<<i->first;
		for(vector<int>::iterator j = i->second.alist.begin(); j!=i->second.alist.end(); j++)
			cout<<" "<<*j;
	}*/
	dfs(-1,no_of_hops,no_of_messages);	
	cout<<"# of hops: "<<no_of_hops<<endl<<"# of messages: "<<no_of_messages<<endl;
		
}

void dfs(int src, int &no_of_hops, int &no_of_messages){
	map<int,bool> visi;
	stack<pair<int,int> > stk;
	no_of_hops = no_of_messages = 0;
	stk.push(make_pair(src,0));

	int curr_node,curr_level;
	while(!stk.empty()){
		curr_node  = stk.top().first;
		curr_level = stk.top().second;
		stk.pop();

		if(visi.find(curr_node)!=visi.end())continue;

		no_of_hops = max(no_of_hops,curr_level);
		
		visi[curr_node]=true;
		for(int i=0;i<nodes[curr_node].alist.size();i++)
		{
			//if(visi.find(nodes[curr_node].alist[i])==visi.end())
			{
				stk.push(make_pair(nodes[curr_node].alist[i],curr_level + 1));
				no_of_messages++;
			}
		}
	}

}