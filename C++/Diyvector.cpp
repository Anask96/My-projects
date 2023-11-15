#include <iostream>
using namespace std;

template <typename T> class DiyVector{
    public:
        DiyVector(unsigned int vuserDefinedSize = 1);
        ~DiyVector();
        T& at(unsigned int index) const;
        unsigned int size() const;
        void pushBack(const T& item);
        void popBack();
        void erase(unsigned int index);
        void insert(unsigned int index, const T& item);
        
        class OutOfRange {

            public:
                OutOfRange();

        };

    private:

    T* myArray;
    int vectorSize;
    int arraySize;

};
template <typename T> DiyVector<T>::DiyVector(unsigned int userDefinedSize) {

    unsigned int i;

    myArray = new T[userDefinedSize];
    arraySize = userDefinedSize;
    vectorSize = userDefinedSize - 1;

    if (vectorSize > 0) {
        for (i = 0; i < userDefinedSize; ++i) {

            myArray[i] = 0;
        }
    }
}
template <typename T> DiyVector<T>::~DiyVector() {

    delete[] myArray;
}
template <typename T> T& DiyVector<T>::at(unsigned int index) const {

    return myArray[index];
}
template <typename T> unsigned int DiyVector<T>::size() const {

    return vectorSize;
 }
template <typename T> void DiyVector<T>::pushBack (const T& item) {

    if (vectorSize == arraySize) {

        unsigned int i;
        T* tempArray = new T[arraySize];

        for (i = 0; i < arraySize; ++i) {

            tempArray[i] = myArray[i];
        }
        myArray = new T[arraySize + 1];

        for (i = 0; i < arraySize; ++i) {

            myArray[i] = tempArray[i];
        }
        myArray[arraySize] = item;
        delete[] tempArray;

        ++arraySize;
        ++vectorSize;
    }
    else {

        myArray[vectorSize] = item;
        ++vectorSize;
    }
}

template <typename T> void DiyVector<T>::popBack() {

    myArray[vectorSize - 1] = NULL;
    --vectorSize;
} 

template <typename T> void DiyVector<T>::erase(unsigned int index) {

    myArray[index] = NULL;
    T tempElement;
    unsigned int i;

    for (i = index; i < arraySize; ++i) {

        tempElement = myArray[i];
        myArray[i] = myArray[i + 1];
        myArray[i + 1] = tempElement;
    }
    --vectorSize;
}

template <typename T> void DiyVector<T>::insert(unsigned int index, const T& item) {

    unsigned int i;
    T tempElement;

    if (vectorSize == arraySize) {

        T* tempArray = new T[arraySize];

        for (i = 0; i < arraySize; ++i) {

            tempArray[i] = myArray[i];
        }
        myArray = new T[arraySize + 1];

        for (i = 0; i < arraySize; ++i) {

            myArray[i] = tempArray[i];
        }
        delete[] tempArray;
        ++arraySize;

       /* myArray[arraySize - 1] = item;

        for (i = arraySize - 1; i > index; --i) {

            tempElement = myArray[i];
            myArray[i] = myArray[i - 1];
            myArray[i - 1] = tempElement;
        }*/

        ++vectorSize;
    }
    else {

        unsigned int i;
        myArray[arraySize] = item;

        for (i = arraySize; i > index; --i) {

            tempElement = myArray[i];
            myArray[i] = myArray[i - 1];
            myArray[i - 1] = tempElement;
        }
        ++vectorSize;
    }  
}
int main() {

    DiyVector<int> myVector;

  
    myVector.pushBack(9);
    myVector.pushBack(9);
    myVector.pushBack(9);
    

    myVector.pushBack(3);

    myVector.pushBack(9);



    cout << myVector.size() << endl;


    cout << myVector.at(0) << endl;
    cout << myVector.at(1) << endl;
    cout << myVector.at(2) << endl;
    cout << myVector.at(3) << endl;
    cout << myVector.at(4) << endl;
    

    return 0;
}
