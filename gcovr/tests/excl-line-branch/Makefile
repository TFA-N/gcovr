all:
	$(CXX) -fprofile-arcs -ftest-coverage -fPIC main.cpp -o testcase

run: txt xml html sonarqube json_summary coveralls

coverage.json:
	./testcase
	$(GCOVR) --exclude-unreachable-branches --json-pretty --json $@

txt: coverage.json
	$(GCOVR) -a $< -b -o coverage.txt

xml: coverage.json
	$(GCOVR) -a $< -b --cobertura-pretty --cobertura coverage.xml

html: coverage.json
	$(GCOVR) -a $< -b --html-details -o coverage.html

sonarqube: coverage.json
	$(GCOVR) -a $< -b --sonarqube sonarqube.xml

coveralls: coverage.json
	$(GCOVR) -a $< -b --coveralls-pretty --coveralls coveralls.json

json_summary:
	./testcase
	$(GCOVR) --exclude-unreachable-branches -b -d --json-summary-pretty -o summary_coverage.json

clean:
	rm -f testcase
	rm -f *.gc*
	rm -f coverage*.* sonarqube*.* summary_coverage.json coveralls.json
