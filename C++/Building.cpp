#include<iostream>

class Building
{
private:
	int B_number;
	int B_floors;
	int B_surface;
	int B_elevetor;
	int secret;
public:
	Building(){}

	Building(int number, int floors, int surface, int elevator)
	{
		B_number = number;
		B_floors = floors;
		B_surface = surface;
		B_elevetor = elevator;
	}

	void set_B(int number, int floors, int surface, int elevator)
	{
		B_number = number;
		B_floors = floors;
		B_surface = surface;
		B_elevetor = elevator;
	}

	int getn() { return B_number; }
	int getf() { return B_floors; }
	int gets() { return B_surface; }
	int gete() { return B_elevetor; }

	void print()
	{
		std::cout << "number = " <<B_number << "\nfloors = " << B_floors << "\nsurface = " << B_surface << std::endl;
		if (B_elevetor == 1)
			std::cout << "has an elevator" << std::endl;
		else
			std::cout << "doesn't have an elevator" << std::endl;
	}
};

class Hospital : public Building
{
private:
	int H_beds;
	int H_parts;
public:
	Hospital() {}

	Hospital(int beds, int parts, int number, int floors, int surface, int elevator) 
		: Building (number, floors, surface, elevator)
	{
		H_beds = beds;
		H_parts = parts;
	}

	void set_H(int beds, int parts)
	{
		H_beds = beds;
		H_parts = parts;
	}

	int getb() { return H_beds; }
	int getp() { return H_parts; }

	void print1()
	{
		print();
		std::cout << "beds = " << H_beds << "\nparts = " << H_parts << std::endl;
	}
};

class Residential : public Building
{
private:
	int R_departments;
public:
	Residential(){}

	Residential(int departments, int number, int floors, int surface, int elevator)
		: Building(number, floors, surface, elevator)
	{
		R_departments = departments;
	}

	void set_R(int departments)
	{
		R_departments = departments;
	}

	int getd() { return R_departments; }

	void print2()
	{
		print();
		std::cout << "departments = " << R_departments << std::endl;
	}
};

class Trading : public Building
{
private:
	int T_markets;
	int T_ofices;
public:
	Trading(){}

	Trading(int markets, int ofices, int number, int floors, int surface, int elevator)
		: Building(number, floors, surface, elevator)
	{
		T_markets = markets;
		T_ofices = ofices;
	}

	void set_T(int markets, int ofices)
	{
		T_markets = markets;
		T_ofices = ofices;
	}

	int getm() { return T_markets; }
	int geto() { return T_ofices; }

	void print3()
	{
		print();
		std::cout << "markets = " << T_markets << "\nofices = " << T_ofices << std::endl;
		std::cout << "" << std::endl;
	}
};

class array
{
private:
	Building B;
	Hospital H;
	Residential R;
	Trading T;
	array* everything;
	int n;
	int secret;
public:
	array() {}

	array(int m)
	{
		everything = new array[m];
	}

	void set_secret(int s){	secret = s; }
	int get_secret() { return secret; }

	void addB()
	{
		n++;
		int a, b, c, d;
		std::cout << "add a building" << std::endl;
		std::cout << "number = ?\nfloors = ?\nsurface = ?\nelevator = ?" << std::endl;
		std::cin >> a >> b >> c >> d;
		everything[n].B.set_B(a, b, c, d);
		everything[n].set_secret(1);
		system("cls");
	}

	void addH()
	{
		int a, b, c, d, e, f;
		n++;
		std::cout << "add a Hospital" << std::endl;
		std::cout << "number = ?\nfloors = ?\nsurface = ?\nelevator = ?" << std::endl;
		std::cout << "beds = ?\nparts = ?" << std::endl;
		std::cin >> a >> b >> c >> d >> e >> f;
		everything[n].H.set_B(a, b, c, d);
		everything[n].H.set_H(e, f);
		everything[n].set_secret(2);
		system("cls");
	}

	void addR()
	{
	int a, b, c, d, e;
	n++;
	std::cout << "add a Residential " << std::endl;
	std::cout << "number = ?\nfloors = ?\nsurface = ?\nelevator = ?" << std::endl;
	std::cout << "departments = ?" << std::endl;
	std::cin >> a >> b >> c >> d >> e;
	everything[n].R.set_B(a, b, c, d);
	everything[n].R.set_R(e);
	everything[n].set_secret(3);
	system("cls");
	}

	void addT()
	{
		int a, b, c, d, e, f;
		n++;
		std::cout << "add a Trading" << std::endl;
		std::cout << "number = ?\nfloors = ?\nsurface = ?\nelevator = ?" << std::endl;
		std::cout << "markets = ?\nofices = ?" << std::endl;
		std::cin >> a >> b >> c >> d >> e >> f;
		everything[n].T.set_B(a, b, c, d);
		everything[n].T.set_T(e, f);
		everything[n].set_secret(4);
		system("cls");
	}

	void print_all()
	{
		for (int i = 1; i <= n; i++)
		{
			if (everything[i].get_secret() == 1)
				everything[i].B.print();
			else if (everything[i].get_secret() == 2)
				everything[i].H.print1();
			else if (everything[i].get_secret() == 3)
				everything[i].R.print2();
			else if (everything[i].get_secret() == 4)
				everything[i].T.print3();
			std::cout << "============================" << std::endl;
		}
	}
};

int main()
{
	/*int a, b, c, d, e, f;
	Building BB;
	std::cout << "add a building" << std::endl;
	std::cout << "number = ?\nfloors = ?\nsurface = ?\nelevator = ?" << std::endl;
	std::cin >> a >> b >> c >> d;
	BB.set_B(a, b, c, d);
	

	Hospital HH;
	std::cout << "add a Hospital" << std::endl;
	std::cout << "number = ?\nfloors = ?\nsurface = ?\nelevator = ?" << std::endl;
	std::cout << "beds = ?\nparts = ?" << std::endl;
	std::cin >> a >> b >> c >> d >> e >> f;
	HH.set_B(a, b, c, d);
	HH.set_H(e, f);


	Residential RR;
	std::cout << "add a Residential " << std::endl;
	std::cout << "number = ?\nfloors = ?\nsurface = ?\nelevator = ?" << std::endl;
	std::cout << "departments = ?" << std::endl;
	std::cin >> a >> b >> c >> d >> e;
	RR.set_B(a, b, c, d);
	RR.set_R(e);
	

	Trading TT;
	std::cout << "add a Trading" << std::endl;
	std::cout << "number = ?\nfloors = ?\nsurface = ?\nelevator = ?" << std::endl;
	std::cout << "markets = ?\nofices = ?" << std::endl;
	std::cin >> a >> b >> c >> d >> e >> f;
	TT.set_B(a, b, c, d);
	TT.set_T(e, f);

	BB.print();
	std::cout << "============================" << std::endl;
	HH.print1();
	std::cout << "============================" << std::endl;
	RR.print2();
	std::cout << "============================" << std::endl;
	TT.print3();*/

	array A(100);

	A.addB();
	A.addH();
	A.addR();
	A.addT();

	A.print_all();

	system("pause");
}