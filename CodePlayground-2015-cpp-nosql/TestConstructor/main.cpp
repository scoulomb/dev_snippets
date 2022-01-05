#include <iostream>
#include "classes.h"

using namespace std;
//https://msdn.microsoft.com/en-us/library/63kwz036.aspx
//http://www.uic.edu/classes/eecs/eecs474/LectureNotes/lecture16.pdf

int main()
{
    cout << "Constructor test!" << endl;

    cout << "--------------------------------" << endl;
    X x;
    x.display();
    cout << "--------------------------------" << endl;

    Y y(1);
    y.display();
    //Y y2;

    cout << "--------------------------------" << endl;
    Z z(1);
    z.display();

    cout << "--------------------------------" << endl;
    Z z2;
    z2.display();

 cout << "--------------------------------" << endl;
     T t(1);
    t.display();

    T t2;
    t2.display();


    return 0;
}
