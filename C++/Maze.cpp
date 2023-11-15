#include <iostream>
#include <ctime>
#include <vector>
#include <stack>
using namespace std;

class coord 
{
    public:

        int x;
        int y;
        coord() {}
        coord(int x, int y)
        {
            this->x = x; 
            this->y = y;
        }
        void assignCoord(int x, int y)
        {
            this->x = x; 
            this->y = y;
        }    
        char compareCoords(coord coordToBeCopared)
        {
            if(coordToBeCopared.x < this->x && coordToBeCopared.y == this->y) return 0;
            else if(coordToBeCopared.x == this->x && coordToBeCopared.y < this->y) return 1;
            else if(coordToBeCopared.x > this->x && coordToBeCopared.y == this->y) return 2;
            else return 3;
        }    
};

class cell 
{
    public:
        bool isVisited = false;
        vector<coord> neighbours; 
        coord location;
        bool cell_on_path = false;
        cell() {}
        cell(int x, int y)
        {
            location.assignCoord(x,y);
        }
        void setLocation(int x, int y)
        {
            location.assignCoord(x,y);
        }
        void make_visited() 
        {
            isVisited = true;
        }
        void addToPath()
        {
            cell_on_path = true;
        }
        void addNeighbor(coord neighbour)
        {
            neighbours.push_back(neighbour);
        }
        void print_cell(int side)
        {
            bool openTop = false;
            bool openLeft = false;
            for(int i = 0; i < neighbours.size(); i++)
            {
                if(side == 0 && this->location.compareCoords(neighbours[i]) == 1) openTop = true;
                else if((side == 1 || side == 2) && this->location.compareCoords(neighbours[i]) == 0) openLeft = true; 
            }

            if(cell_on_path)
            {
                if(openLeft && side == 2) cout << "  . |";
                else if(side == 2) cout << "| . |";

                if(openLeft && side == 1) cout << "  . ";
                else if(side == 1) cout << "| . ";
            }
            else
            {
                if(openLeft && side == 2) cout << "    |";
                else if(side == 2) cout << "|   |";

                if(openLeft && side == 1) cout << "    ";
                else if(side == 1) cout << "|   ";
            }

            if(openTop && side == 0) cout << "+   ";
            else if(side == 0)cout << "+---";

            if(side == 3) cout << "+---";
        }
};

class maze
{
    public:
        stack<coord> myStack;                   //Stack is used to find the path while creating the maze
        vector<vector<cell> > myMaze;
        bool pathFound = false;

        int length;
        int width;

        maze(int length, int width)
        { 
            this->length = length;
            this->width = width;
            vector<vector<cell> > rows(width);
            for(int i = 0; i < width; i++)
            { 
                rows[i] = vector<cell>(length);
                for(int j = 0; j < length; j++)
                {
                    rows[i][j].setLocation(i,j);
                }
            }
            myMaze = rows;
            createMaze();
        }

        void createMaze()
        {
            mazeGenerator(myMaze[0][0].location);
            printMaze();
        }
        
        void mazeGenerator(coord currentCoord)
        {
            coord newCoord;
            coord possibleNeighbours;

            if(myStack.size() == 0) myStack.push(currentCoord);

            newCoord = nextCell(currentCoord.x,currentCoord.y);
            myMaze[currentCoord.x][currentCoord.y].make_visited();
            if(newCoord.x == -1) 
            {
                return;
            }
            breakWallsBetweenNeighbors(newCoord, currentCoord);
            if(!pathFound) 
            {
                myStack.push(newCoord);
                checkPath();
            }
            while(true)
            {
                mazeGenerator(newCoord);
                possibleNeighbours = nextCell(newCoord.x,newCoord.y);
                if(possibleNeighbours.x == -1)
                {
                    myStack.pop();
                    break;
                }
            }
        }

        void breakWallsBetweenNeighbors(coord newCoord, coord currentCoord)
        {
            myMaze[currentCoord.x][currentCoord.y].addNeighbor(newCoord);
            myMaze[newCoord.x][newCoord.y].addNeighbor(currentCoord);
        }

        void checkPath()
        {
            if(myStack.top().x == width-1 && myStack.top().y == length-1)
            {
                pathFound = true;
                while(myStack.size() > 0)
                {
                    myMaze[myStack.top().x][myStack.top().y].addToPath();
                    myStack.pop();
                }
            }
        }

        coord nextCell(int x,int y)
        {
            int direction;
            bool canMoveUp = false;
            bool canMoveDown = false;
            bool canMoveLeft = false;
            bool canMoveRight = false;
            if(x > 0) if(!myMaze[x-1][y].isVisited) canMoveLeft = true;
            if(y > 0) if(!myMaze[x][y-1].isVisited) canMoveUp = true;
            if(x < width-1) if(!myMaze[x+1][y].isVisited) canMoveRight = true;
            if(y < length-1) if(!myMaze[x][y+1].isVisited) canMoveDown = true;

            if(!canMoveUp  && !canMoveDown  && !canMoveLeft  && !canMoveRight) return coord(-1,-1);
            else
            {
                while(true)
                {   
                    direction = rand()%4; 
                    if(direction == 0 && canMoveLeft) return coord(x-1, y);
                    if(direction == 1 && canMoveUp) return coord(x, y-1);
                    if(direction == 2 && canMoveRight) return coord(x+1, y);
                    if(direction == 3 && canMoveDown) return coord(x, y+1);
                }
            }
        }

        void printMaze()
        {
            int repeat;
            int side_of_cell_to_print;
            for(int i = 0; i < length; i++)
            {
                if(i == length - 1) repeat = 2;
                else repeat = 1;
                side_of_cell_to_print = 0;
                for(int j = 0; j < width; j++)
                {
                    if(j == width - 1 && side_of_cell_to_print == 1) side_of_cell_to_print = 2;
                    myMaze[j][i].print_cell(side_of_cell_to_print);
                    if(j == width - 1 && repeat > 0) 
                    {
                        j = -1;
                        if(side_of_cell_to_print == 0) cout<< "+";
                        repeat -= 1;
                        side_of_cell_to_print += 1;
                        cout << "\n";
                    }
                }
                if(side_of_cell_to_print == 3) cout<< "+";
                cout << "\n";
            }
        }
};

int main(int argc, char** argv)
{
    int height, width;

    if(argc >= 3) {
        height = std::stoi(argv[1]);
        width = std::stoi(argv[2]);
        if(argc==4) srand((unsigned) std::stoi(argv[3]));
        else srand(time(NULL));
        maze newMaze = maze(height, width);
    }
}