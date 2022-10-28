# UIC-Web-Search-Engine
This project is about creating a multi-threaded web crawler indexing documents from the UIC website. 
Additionally, it will provide data based on the top most relevant documents to the search query provided by the user. The key is to efficiently return search results to a query with &lt;1 second response time.

This Project contains all the necessary files to be run.

The software is built on Django Framework and it also contains an HTML page which presents the GUI to the end-user.
Additionally, there are 3 main Python files that make up the back-end part of the project.

The best way to run the project is through Microsoft Visual Studio Code.

Once you have imported the project folder on to VS Code, please run the below commands in your terminal :-

1. Install virtualenv
	
	Command : pip install virtualenv

2. Create virutal environment

	Command : virtualenv uic_wse_env

Activate environment

For mac--
	source uic_wse_env/bin/activate

For windows--
	./uic_wse_env/Scripts/activate

Install dependencies
	cd uic_wse/	
 
You can double check if the requirements.txt file exists in this folder then run the below command:
	pip install -r requirements.txt

Finally run the project using the below command

	python manage.py runserver


After running the project, please go to the below localhost url in the browser. #make sure no other ports are open

localhost:8000/home

And you should be good to go!
