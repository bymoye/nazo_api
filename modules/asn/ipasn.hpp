#include <iostream>
#include <fstream>
#include <vector>
#include <boost/asio/ip/address.hpp>
#include <boost/algorithm/string.hpp>
using namespace boost::asio::ip;
using namespace boost::algorithm;
using namespace std;
namespace Address {
        vector<address> ipv4;
        vector<address> ipv6;
        vector<vector<string>> ipv4data;
        vector<vector<string>> ipv6data;
        
        void read_file(string filename, vector<vector<string>> &data, vector<address> &ip) {
            ifstream _file(filename);
            string line;
            while (getline(_file, line)) {
                vector<string> row;
                split(row, line, is_any_of("\t"));
                ip.push_back(make_address(row[0]));
                data.push_back(vector<string>(row.begin()+2, row.end()));
                if (_file.peek() == EOF){
                    ip.push_back(make_address(row[1]));
                    break;
                }
            }
            _file.close();
        }

        void init(string ipv4file,string ipv6file){
            read_file(ipv4file,ipv4data,ipv4);
            read_file(ipv6file,ipv6data,ipv6);
            if (ipv4.size() == 0 || ipv6.size() == 0) {
                cout << "\033[31m" << "Error: ipasn.hpp: init(): ipv4 or ipv6 file is empty" << "\033[0m" << endl;
            }else{
                cout << "\033[32m\033[1m" << "ipasn.hpp: init(): ipv4 and ipv6 file loaded"<< endl;
                cout << "ipasn.hpp: init(): ipv4 size: " << "\033[4m" << ipv4.size() << "\033[0m" << endl;
                cout << "\033[32m\033[1m" << "ipasn.hpp: init(): ipv6 size: " << "\033[4m" << ipv6.size() << "\033[0m" << endl;
            }
        }

        auto binary_search(vector<address>& data, address ip){
            return lower_bound(data.begin(), data.end(), ip);
        }

        vector<string> lookup(string ip) {
            address _ip = make_address(ip);
            bool is_ipv4 = _ip.is_v4();
            auto it = binary_search(is_ipv4 ? ipv4 : ipv6, _ip);
            return is_ipv4 ? ipv4data.at(it-ipv4.begin()-1) : ipv6data.at(it-ipv6.begin()-1);
        }
}