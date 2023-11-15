#include <iostream>
#include <iomanip>
#include <vector>
using namespace std;

class BST {
    public:
        BST();
        ~BST();
        void insertKey(int newKey);
        bool hasKey(int searchKey);
        std::vector<int> inOrder();
        int getHeight();
        void prettyPrint();

    private:
        int height;
        class t_node{
            public:
              t_node() {};
              t_node(int key);
              ~t_node() {};
              void destoryTree();
              void appendNode(int key, int &treeHeight);
              void setLeftKey(int key);
              void setRightKey(int key);
              void changeNodePosition(vector<int>&vect,bool&mostLeft);
              bool keyExist();
              int getKey();
              void findNode(int key, int &depthPointer);
              t_node* leftKey;
              t_node* rightKey;
              int depth;
              int height;
            private:
              bool hasLeftKey = false;
              bool hasRightKey = false;
              int key;
              bool hasKey = false;
        };
        t_node* tree;
};

BST::BST(){
  tree = new t_node();
}

void BST::t_node::destoryTree() {
  if(hasLeftKey) {
    leftKey->destoryTree();
    delete(leftKey);
  }
  if(hasRightKey) {
    rightKey->destoryTree();
    delete(rightKey);
  }
}

BST::~BST(){
  tree->destoryTree();
  delete(tree);
}

int BST::t_node::getKey(){
  return this->key; 
}

BST::t_node::t_node(int key){
  this->key = key;
  this->depth = 0;
  this->height = 0;
  this->hasKey = true;
}

int BST::getHeight(){
  return tree->height;
}

bool BST::hasKey(int searchKey){
  int depth = -1;
  tree->findNode(searchKey, depth);
  if(depth > -1) return true ;
  return false;
}

bool BST::t_node::keyExist(){
  return this->hasKey;
}

void BST::insertKey(int key){
  int treeHeight = 0;
  if(!tree->keyExist())
  {
    delete(tree);
    tree = new t_node(key);
  }
  else tree->appendNode(key, treeHeight);
  if(treeHeight > tree->height) tree->height = treeHeight;
}

void BST::t_node::setRightKey(int key) {
  this->rightKey = new t_node(key);  
  this->hasRightKey = true;
}

void BST::t_node::setLeftKey(int key) {
  this->leftKey = new t_node(key);
  this->hasLeftKey = true;
}

void BST::t_node::appendNode(int key, int &treeHeight)
{
  treeHeight += 1;
  if(key > this->key && !hasRightKey){
    this->setRightKey(key);
    rightKey->depth = treeHeight;
  }
  else if(key > this->key && hasRightKey) this->rightKey->appendNode(key,treeHeight);
  else if(key < this->key && !this->hasLeftKey) {
    this->setLeftKey(key);
    leftKey->depth = treeHeight;
  }
  else if (key < this->key && this->hasLeftKey) this->leftKey->appendNode(key,treeHeight); 
}

void BST::t_node::changeNodePosition(vector<int>&vect, bool &mostLeft)
{
  if(hasLeftKey) this->leftKey->changeNodePosition(vect, mostLeft);
  if(mostLeft == false) 
  {
    mostLeft = true;
    if(this->keyExist()) vect.push_back(this->key);
  }
  else if(this->keyExist()) vect.push_back(this->key);
  if(hasRightKey) this->rightKey->changeNodePosition(vect, mostLeft);
}

vector<int> BST::inOrder(){
  std::vector<int> vect;
  bool mostLeft = false;
  tree->changeNodePosition(vect, mostLeft);
  return vect;
}

void BST::t_node::findNode(int key, int &depthPointer)
{
  if(this->getKey() == key) {
    depthPointer = this->depth;
    return;
  }
  if(this->hasRightKey) rightKey->findNode(key, depthPointer);
  if(this->hasLeftKey) leftKey->findNode(key, depthPointer);
}

void BST::prettyPrint(){
  std::vector<int> vect = this->inOrder();
  int height = getHeight();
  int repeat;
  int repeatLimit;
  int nodeDepth;
  for(int i = 0; i <= height; i++){
    repeat = 0;
    if(vect.size() == 0) break;
    if(i == height) repeatLimit = 2;
    else repeatLimit = 1;
    for(int j = 0; j < vect.size(); j++) {
      tree->findNode(vect[j], nodeDepth);
      if((repeat == 0 || repeat == 2) && j == vect.size() - 1)cout << "------";
      else if(repeat == 0 || repeat == 2)cout << "-----";
      else if(repeat == 1 && j == vect.size() - 1 && nodeDepth == i) cout << "|" << std::setw (4) << vect[j] << "|";
      else if(repeat == 1 && j == vect.size() - 1)cout << "|    |";
      else if(repeat == 1 && nodeDepth == i)cout << "|" << std::setw (4) << vect[j];
      else if(repeat == 1)cout << "|    ";
      if(j == vect.size() - 1 && repeat < repeatLimit) { 
        cout << endl;
        j = -1;
        repeat += 1;
      }
    }
    cout << "\n";
  }
}
  
int main() {
  
  BST tree; 
  std::vector<int> vect; 
  vect.push_back(0);
  vect.push_back(4);
  vect.push_back(-4);
  vect.push_back(6);
  vect.push_back(-6);
  vect.push_back(-3);
  vect.push_back(3);
  vect.push_back(-7);
  vect.push_back(9);
  for(int x = 0; x < vect.size(); x++){ 
    tree.insertKey(vect[x]); //use insertKey to save data
  }
  vect = tree.inOrder(); //string of ordered numbers is in vect at this point 

  tree.prettyPrint();
  return 0;
}