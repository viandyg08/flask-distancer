# How to run

- Acquire API Key from [Yandex maps](https://yandex.ru/dev/maps/geocoder/doc/desc/concepts/about.html)

## 1) Docker-compose:

- Add environment variable for YANDEX_API_KEY by running one of the command below:
  ```
  # Windows Command Prompt
  set YANDEX_API_KEY=yourapikey
  # PowerShell
  $env:YANDEX_API_KEY="yourapikey"
  # bash
  export YANDEX_API_KEY=yourapikey
  ```
  
OR

- Edit docker-compose.yml file and insert the API key to the environment
  ```
  environment:
    - YANDEX_API_KEY=yourapikey
  ```
- run the container with: 
  ```
  docker-compose up
  ```
- open with `localhost:5000`

## 2) Without Docker:

- Add environment variable for YANDEX_API_KEY by running one of the command below:
  ```
  # Windows Command Prompt
  set YANDEX_API_KEY=yourapikey
  
  # PowerShell
  $env:YANDEX_API_KEY = yourapikey
  
  # bash
  export YANDEX_API_KEY=yourapikey
  ```
  
- install the required packages
  ```
  pip install -r requirements.txt
  ```

- run with:
  ```
  flask run
  ```
  
# Usage
Assuming that Flask is on `localhost:5000`, use the following format:
```
http://localhost:5000/?address=someaddress

# For Example:
http://localhost:5000/?address=Sheremetyevo Airport
```

- Error logs will be written to `errors.log` file

# Run Tests
```
python distancer\test_response.py
```