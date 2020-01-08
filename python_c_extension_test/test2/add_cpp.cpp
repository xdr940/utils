#include <iostream>
extern "C"
void add(int a,int b){
	std::cout<<"the result:"<<a+b<<std::endl;
}