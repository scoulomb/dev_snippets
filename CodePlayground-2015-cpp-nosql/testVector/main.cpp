#include <vector>
#include <algorithm>
#include <iterator>
#include <iostream>

using namespace std;


// Sample coordinate class
class P {
public:
    int x;
    int y;
    P() : x(0), y(0) {}
    P(int i, int j) : x(i), y(j) {}
};


// Just for printing out
std::ostream& operator<<(ostream& o, const P& p) {
    std::cout << p.x << " " << p.y << endl;
    return o;
}

// Tells us if one P is less than the other
bool less_comp(const P& p1, const P& p2) {

    if(p1.x > p2.x)
        return false;
    if(p1.x < p2.x)
        return true;

    // x's are equal if we reach here.
    if(p1.y > p2.y)
        return false;
    if(p1.y < p2.y)
        return true;

    // both coordinates equal if we reach here.
    return false;
}


// Self explanatory
bool equal_comp(const P& p1, const P& p2) {

    if(p1.x == p2.x && p1.y == p2.y)
        return true;

    return false;
}

int main()
{

    vector<P> v;
    vector<P> d;
    v.push_back(P(1,2));
    v.push_back(P(1,3));
    v.push_back(P(1,2));
    v.push_back(P(1,4));
    v.push_back(P(1,2));

    //http://www.geeksforgeeks.org/find-the-two-repeating-elements-in-a-given-array/
    for(std::vector<P>::size_type i = 0; i != v.size(); i++) {
       for(std::vector<P>::size_type j = i+1; j != v.size(); j++) {
            if(equal_comp(v[i],v[j])){
                d.push_back(v[j]);
            }

        }
    }

    for(std::vector<P>::size_type k = 0; k != d.size(); k++) {

        cout << d[k];

    }

    cout << "*****************************";

    //http://stackoverflow.com/questions/3177241/best-way-to-concatenate-two-vectors
    vector<P> vd;
    vd.reserve( v.size() + d.size() ); // preallocate memory
    vd.insert( vd.end(), v.begin(), v.end() );
    vd.insert( vd.end(), d.begin(), d.end() );


    for(std::vector<P>::size_type l = 0; l != vd.size(); l++) {

        cout << vd[l];

    }
    /*
  // Sort the vector. Need for std::unique to work.
  std::sort(v.begin(), v.end(), less_comp);

  // Collect all the unique values to the front.
  std::vector<P>::iterator it;
  it = std::unique(v.begin(), v.end(), equal_comp);
  // Resize the vector. Some elements might have been pushed to the end.
  v.resize( std::distance(v.begin(),it) );

  // Print out.
  std::copy(v.begin(), v.end(), ostream_iterator<P>(cout, "\n"));*/

}
