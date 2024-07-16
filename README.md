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


clear
    2  ls
    3  git clone https://github.com/Emmastro/ray.git
    4  cd ray
    5  python 
    6  python3
    7  python3 -m venv venv
    8  sudo apt install python3.12-venv
    9  sudo apt-get install python3.12-venv
   10  clear
   11  sudo apt update
   12  sudo apt upgrade
   13  python3 -m venv venv
   14  sudo apt-get install python3.12-venv
   15  python3 -m venv venv
   16  source venv/bin/activate
   17  clear
   18  cd python/ray/dashboard/client
   19  ls
   20  cd src
   21  ls
   22  cd ..
   23  clear
   24  npm install
   25  sudo apt install npm
   26  npm install
   27  deactivate
   28  npm start
   29  exit
   30  cd ray
   31  ls
   32  git checkout dev
   33  python3 -m venv venv
   34  source venv/bin/activate
   35  pip install ray[default]
   36  python python/ray/setup-dev.py
   37  python python/ray/setup-dev.py -y
   38  sudo apt-get install -y build-essential curl clang-12 pkg-config psmisc unzip
   39  sudo apt-get install -y build-essential curl pkg-config psmisc unzip
   