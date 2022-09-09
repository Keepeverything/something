#include <iostream>
#include <fstream>
#include <filesystem>
#include <vector>
#include <thread>
#include <future>
#include <regex>

std::vector<std::string> reg(std::string firstline, std::string separators);
std::string make_reg(std::vector<std::string>& sep);

class FileParser
{
public:
    void readandparse(std::string filename, std::promise<std::pair<std::string,std::vector<std::string>>> && promise){// Метод для чтения и парса файла 
        std::vector<std::string> lines;

        std::pair<std::string,std::vector<std::string>> lineandSeps;

        std::ifstream file;
        file.open(filename);

        if (file.is_open()){
            std::string line;
            std::string firstline;

            getline(file, firstline);
            lineandSeps.first=firstline;
            
            while (getline(file, line)){
                lines.push_back(line);
            }
            lineandSeps.second=lines;

            file.close();
        } else {
            std::cout << "Unable to open file " << filename << std::endl;
        }

        promise.set_value(lineandSeps);
    }

};

std::vector<std::string> reg(std::string firstline, std::string separators){//обработка регулярным выражением 
    std::vector<std::string> sepline;
    std::regex regular(separators);
    auto words_begin = std::sregex_iterator(firstline.begin(), firstline.end(), regular);
    auto words_end = std::sregex_iterator();
                
    for (std::sregex_iterator i = words_begin; i != words_end; ++i) {
        std::smatch match = *i;                                                 
        std::string match_str = match.str(); 
        
        if(match_str.length()!=0){
            sepline.push_back(match_str);
        }
        
    }
    if(sepline.empty()){
        sepline.push_back("Something goes wrong...");
    }
    return sepline;
    
}

std::string make_reg(std::vector<std::string>& sep){//составление строки разделителей 
        std::string separators=R"(([^)";
        std::string raw = R"(\\)";
        std::string a="";
        for(auto i = sep.begin(); i != sep.end(); i++){
            a=*i;

            if (a.length()>1){
                separators+='('+*i+')';   
            }else{
                separators+=raw+*i;
            }

        }
        separators+="]*";
        separators+=R"())";
        return separators;
}

std::vector<std::string> get_files(std::string dirname, std::string outputFilename){//получение подходящих файлов из директории
    std::vector<std::string> files;

    for (const auto & entry : std::filesystem::directory_iterator(dirname)){
        if(!is_directory(entry) && entry.path().extension()==".txt" && entry.path().filename().string()!=outputFilename){
            files.push_back(entry.path());                                                      
        }
    }

    return files;
}

int main(int argc, char *argv[]){
    setlocale(LC_ALL, "RUS");
    FileParser current_file;    

    std::string dirname=argv[1], outputFilename=argv[2];
    std::vector<std::string> filenames = get_files(dirname, outputFilename);

    std::vector<std::tuple<std::string, std::thread, std::future<std::pair<std::string,std::vector<std::string>>>>> threads;//пустой вектор потоков
    threads.reserve(filenames.size());

    for (std::string filename: filenames){
        std::promise<std::pair<std::string,std::vector<std::string>>> promise;
        std::future<std::pair<std::string,std::vector<std::string>>> future = promise.get_future();

        std::thread thread(&FileParser::readandparse, current_file, filename, std::move(promise));//инициализация потока с вызовом метода парса
        threads.push_back(std::make_tuple(filename, std::move(thread), std::move(future)));//добавление потока в вектор
    }

    std::ofstream outputFile;
    outputFile.open(outputFilename, std::ofstream::app);//создание выходного файла или добавление строк в уже существующий
    for (std::tuple<std::string, std::thread, std::future<std::pair<std::string,std::vector<std::string>>>> & threadTuple: threads){
        auto && [filename, thread, future] = threadTuple;

        thread.join();
        auto lines = future.get();

        std::regex regular("(\\w+)\\.txt");               //получение имени файла из пути к нему и запись в выходной файл
        std::cmatch name;
        std::regex_search(filename.c_str(), name, regular);
        outputFile << name[0] << std::endl;//запись имени

        std::string separators = make_reg(lines.second);

        
        auto sepline = reg(lines.first, separators);//получение вектора из разделенной строки 
        for (std::string line: sepline){
           outputFile << line << std::endl;//запись подстрок 
        }

    }
    outputFile.close();    
    return 0;
}