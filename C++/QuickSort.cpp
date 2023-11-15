#include<iostream>
#include<cstdlib>
using namespace std;
void quicksort(int *a, int start, int end);
void swap(int *x, int *y);
int partitioning(int *a, int start, int end);
int main()
{
	int z = 5, b = 10;
	int a[] = { 7, 6, 5, 4, 3, 2, 1, 0 };
	quicksort(a, 0,7);
	for (int i = 0; i < 8; i++)
		cout << a[i] << endl;
	//system("pause");
	char waitUserInput;
	cin >> waitUserInput;
	return 0;
}
void swap(int *x, int *y)
{
	int temp = *x;
	*x = *y;
	*y = temp;
}
int partitioning(int *a , int start , int end)
{
	int pivot = a[end];
	int j = start ;
	for (int i = start; i < end ; i++)
	{
		if (a[i] <= pivot)
		{
			swap(a[i],a[j]);
			j++;
		}	
	}
	swap(a[j],a[end]);
	return j;
}
void quicksort(int *a, int start, int end)
{
	if (start < end)
	{
		int pindex = partitioning(a, start, end);
		quicksort(a, start, pindex - 1);
		quicksort(a, pindex + 1, end);
	}
	return;
}