# braincheck  installment instructions 

After cloning the repository, type into the terminal:
```
  cd braincheck 
```

After you are in the braincheck directory, create a virtual environment in the terminal and activate it
```
  # This will create the virtual environment (/venv) directory
  python -m venv venv
  
  # If you are on Windows, type this into terminal
  source venv/Scripts/activate
  
  (type venv\Scripts\activate.bat if that doesn't work)
  
  # If you are on Mac, type this instead
  source venv/bin/activate
  
```
Once the virtual environment is running (you will see (venv) in the terminal if it is), install the required modules by typing
```
  pip install -r requirements.txt
```

Finally, to run the app just input
```
  flask run
```
  
  
  
