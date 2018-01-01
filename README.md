# Diogenes
Project to scrape continuously real estate websites, build geo-location based pricing models, and identify mispriced properties.
In order to build xgboost, you need to have gcc-c++ installed in your machine. You can do so by one of the following commands:

On linux:
	sudo yum install gcc gcc-c++
	sudo apt-get install gcc gcc-c++

On mac, with brew installed:
	sudo brew install gcc gcc-c++

Then to install the software, just do the following.
	pip install -r requirements.txt
	scrapy crawl rent -o entire_apartments_tokyo_20171224.csv
