# Getting Started

### Add Envs
Create .env file and add the following keys (with values):  
```
DBNAME=xxxx
USER=xxxx
PASSWORD=xxxx
HOST=xxxx
PORT=xxxx
```  

### Steps to run the project  
1. pip install -r requirements  
2. python manage.py migrate  
3. python manage.py makemigrations  
4. python manage.py runserver  
  
<br/>  
  
# Types of APIs covered in this project

### Authentication APIs  
[POST] /api/v1/iam/login/ - Login API  
[POST] /api/v1/iam/refresh/ - Refresh API  
[POST] /api/v1/iam/sign-up/ - Sign up API  
  
### User Management APIs  
[GET]  /api/v1/iam/user/ - Users list API  
[GET] /api/v1/iam/user/:id/ - User details API
[POST] /api/v1/iam/user/ - User create API  
[PUT] /api/v1/iam/user/:id/ - User update API  
[PATCH] /api/v1/iam/user/:id/ - User partial update API  
[DELETE] /api/v1/iam/user/:id/ - Users delete API  