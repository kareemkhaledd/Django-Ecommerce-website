The environment used: Visual Studio Code

Steps to run the project:
1)Open any empty folder using VS
2)Install virtualenv using the command:
	pip install virtualenv
3)Make a virtual ennvironmet using the following command:
	virtualenv env
4)Activate the virtual env you created using the following command:
	env\Scripts\activate
5)install django and pillow in your env using the following commands:
	pip install django
	pip install pillow
6)Create a django project and name it project using this command:
	django-admin startproject project
7)Copy all the files and folders you will find inside our project folder into your project folder 
that you created using the last command
8)using vs open this folder by using the terminal:
	cd project
9)Run the server using the following command:
	python manage.py runserver