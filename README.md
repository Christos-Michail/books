# books
you will need vitualenv for this:  
pip install virtualenv  
Once installed, you can create a virtual environment with:  
virtualenv [directory]  
source myvenv/bin/activate  
Using Python 3.6+, run pip3 install -r requirements.txt to install the dependencies  
Set the environment variable export FLASK_APP=books.py  
flask run  

GET http://127.0.0.1:5000/book/favourites -->downloads the books
GET http://127.0.0.1:5000/book/OL7353617M -->retrieve a book
