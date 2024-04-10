#include <iostream>
#include <string>
#include <fstream>
#include <sstream>
#include <vector>
#include <algorithm>
#include <map>

int main(int argc, char** argv) {
  std::ifstream input{argv[1]};
  std::string first_line;
  std::map<std::string, std::vector<std::string>> data;
  std::getline(input, first_line);
	std::istringstream ss{first_line};
	std::string word;
	std::vector<std::string> headers;
	while (std::getline(ss, word, ',')) {
		data[word] = {};
		headers.push_back(word);
	}

	int number_of_lines = 0;
	std::string line;
	while (std::getline(input, line)) {
		++number_of_lines;
		std::istringstream ss{line};
		std::string value;
		int i = 0;
		while (std::getline(ss, value, ',')) {
			data[headers[i]].push_back(value);
			++i;
		}
	}

	// we build a vector with the following strings "Atacar", "Recoger_Armas", "Recoger_Energia", "Explorar", "Huir", "Detectar_Peligro"
	std::vector<std::string> actions{"Atacar", "Recoger_Armas", "Recoger_Energia", "Explorar", "Huir", "Detectar_Peligro"};
	std::vector<double> action_probabilities;
	std::cout << "Probability of St" << std::endl;
	std::cout << "-------------------" << std::endl;
	for (const auto& action : actions) {
		std::cout << action << ": ";
		double probability = std::count(data["St"].begin(), data["St"].end(), action) / static_cast<double>(number_of_lines);
		std::cout << probability << std::endl;
		action_probabilities.push_back(probability);
	}
	std::cout << "-------------------" << std::endl << std::endl;

	std::cout << "Probability of St+1" << std::endl;
	std::cout << "-------------------" << std::endl;
	for (const auto& action : actions) {
		std::cout << action << ": ";
		double probability = std::count(data["st_1"].begin(), data["st_1"].end(), action) / static_cast<double>(number_of_lines);
		double action_probability_at_st = action_probabilities[std::distance(actions.begin(), std::find(actions.begin(), actions.end(), action))];
		//std::cout << action_probability_at_st << " * " << probability << std::endl;
		std::cout << probability  << std::endl;
	}
	std::cout << "-------------------" << std::endl << std::endl;

	std::vector <std::string> health_parameters{"Alta", "Baja"};
	std::cout << "Probability of H" << std::endl;
	std::cout << "-------------------" << std::endl;
	for (const auto& health : health_parameters) {
		std::cout << health << ": ";
		double probability = std::count(data["H"].begin(), data["H"].end(), health) / static_cast<double>(number_of_lines);
		std::cout << probability << std::endl;
	}
	std::cout << "-------------------" << std::endl << std::endl;

	std::vector <std::string> yesno_parameters{"si", "no"};
	std::vector<std::string> yesno_elements{"HN", "NE", "PH", "PW"};
	for (const auto& element : yesno_elements) {
		std::cout << "Probability of " << element << std::endl;
		std::cout << "-------------------" << std::endl;
		for (const auto& yesno : yesno_parameters) {
			std::cout << yesno << ": ";
			double probability = std::count(data[element].begin(), data[element].end(), yesno) / static_cast<double>(number_of_lines);
			std::cout << probability << std::endl;
		}
		std::cout << "-------------------" << std::endl << std::endl;
	}

	std::vector <std::string> weapon_parameters{"armado", "desarmado"};
	std::vector<std::string> weapon_elements{"W", "OW"};
	for (const auto& element : weapon_elements) {
		std::cout << "Probability of " << element << std::endl;
		std::cout << "-------------------" << std::endl;
		for (const auto& weapon : weapon_parameters) {
			std::cout << weapon << ": ";
			double probability = std::count(data[element].begin(), data[element].end(), weapon) / static_cast<double>(number_of_lines);
			std::cout << probability << std::endl;
		}
		std::cout << "-------------------" << std::endl << std::endl;
	}
}