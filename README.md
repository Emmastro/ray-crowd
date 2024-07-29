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

python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. service.proto


hypercorn asgi:app -b 0.0.0.0:5000 --log-level info --access-log - --error-log - --reload

