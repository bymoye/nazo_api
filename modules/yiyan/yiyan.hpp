#include <iostream>
#include <fstream>
#include "./json.hpp"
#include "../rand/Rand.hpp"
using namespace std;
using namespace nlohmann;

namespace Hitokoto
{
    vector<char> sentencesType;
    int sentencesTypeSize;
    unordered_map<char, vector<string>> sentences;

    void init(string path)
    {
        json j;
        ifstream _file(path + "/all.json");
        cout << "Hitokoto::init(): " << path << endl;
        _file >> j;
        for (auto &sentence : j)
            sentencesType.push_back(sentence["key"].get<string>().at(0));

        _file.close();
        j.clear();

        cout << "Hitokoto::init(): all.json parsed" << endl;
        for (auto &sentence : sentencesType)
        {
            ifstream ifs(path + "/" + sentence + ".json");
            json j;
            ifs >> j;
            for (auto &sentence1 : j)
            {
                sentences[sentence].push_back(sentence1.dump(4));
            }
            ifs.close();
            j.clear();
        }
        sentencesTypeSize = sentencesType.size();
        cout << "Hitokoto::init(): success" << endl;
    }

    string getSentence(vector<char> type = vector<char>())
    {
        char _type;
        if (type.size() == 0)
        {
            _type = sentencesType[Storm::random_below(sentencesTypeSize)];
        }
        else
        {
            _type = type[Storm::random_below(type.size())];
        }
        return sentences.at(_type).at(Storm::random_below(sentences[_type].size()));
    }
}