#ifndef CLASSES_H
#define CLASSES_H

#include <iostream>
#include <string>

/*
Hypothesis
When no constructor is defined a default constructor is generated
The default constructor is calling member attribute default constructor (std::string included)
For built in type it is doing what it want sometimes we get à but random

*/

class A
{
public:
    A(){
        std::cout<< "A's awesome default constructor"<<std::endl;
    }

};

class X
{
public:
    void display(){
        std::cout << "s:" << "//n:" << n <<std::endl;
    }
private:
    std::string s;
    int n;
    A a;
};

class Y
{
public:
    void display(){
        std::cout << "s:" << "//n:" << n <<std::endl;
    }

    Y(int i){};
private:
    std::string s;
    int n;
    A a;
};

class Z
{
public:
    void display(){
        std::cout << "s:" << "//n:" << n <<std::endl;
    }

    Z(int i){};
    Z(){std::cout << "Z cosntr"<<std::endl;};
private:
    std::string s;
    int n;
    A a;
};


class T
{
public:
    void display(){
        std::cout << "s:" << "//n:" << n <<std::endl;
    }

    T(int i){};
    T() = default;
private:
    std::string s;
    int n;
    A a;
};


#endif // CLASSES_H
