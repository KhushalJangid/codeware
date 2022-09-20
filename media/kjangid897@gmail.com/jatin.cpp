#include <iostream>
using namespace std;

void iter(string s,int n){
  int i;
  for(i=0;i<n;i++){
    cout << s;
  } 
}

int main() {
  int i;
  int n;
  cin >> n;
  for(i=1;i<=n;i++){
    iter("*",i);
    cout << endl;
  }
  return 0;
}