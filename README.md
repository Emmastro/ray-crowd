Running the Application
Install dependencies:

sh
Copy code
pip install -r requirements.txt
Set up the database:

```
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```

Run the application:

```
python run.py
```
