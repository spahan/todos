# todos
Todo task tool

## python
use python3!

## database
for production use it is recommended to use mysql or postgresql.

## venv
use venvs!

### create venv
```
python -m venv venv
```

### activate venv
```
source venv/bin/activate
```

## copy & edit config
```
cp todos/config.cfg.example todos/config.cfg
nano todos/config.cfg
```


## build
```
pip install -r requirements.txt
pip install --editable .
```


## create database
```
python -i
>>> from todos.todos import db
>>> db.create_all()
```

## run
```
export FLASK_APP=todos/todos.py
flask run
```

## debug
```
export FLASK_APP=todos/tods.py
export FLASK_DEBUG=True
flask run
```
