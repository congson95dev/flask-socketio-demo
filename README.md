# flask-socketio-demo
A simple demo to demonstrate using events to perform client-server communication and display data on a web page. Bitcoin prices are fetched using Coinbase API and displayed in real time.

![image](https://user-images.githubusercontent.com/32733783/146593242-79c11b31-b578-4445-9f07-ca0bacecc13a.png)

### Installation:

### Create environment:
```
cd project_name

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt
```

### Pre-requisite:

```
pip install python-socketio
```

### Run:
```
python3 app.py
```
### Go to `127.0.0.1:5000` in your browser to access the flask app.
### You could also run the `index.html` directly in the browser to see the same result.
### This approach could be considered as external system connect to our socketio. (Such as ReactJS, NextJS ...)
### By default, it will be blocked because we don't config the `CORS`, but in `app.py`, we are already config it, so it can be access from the external system.

### Read the dev blog and explanation [here](https://medium.com/the-research-nest/how-to-log-data-in-real-time-on-a-web-page-using-flask-socketio-in-python-fb55f9dad100)
