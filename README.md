# AutoReport
This is a set of automation test scripts based on [Robot Framework](https://github.com/robotframework/robotframework) used for [TD-shim](https://github.com/confidential-containers/td-shim) test.

## Setup
### Install Robot Framework
```
pip install robotframework
```

### Install python dependencies
```
pip install bs4
```

### Configure the JSON file

- **email**
    ```
    eg:
        "sender":"xx.xx@xx.com",
        "to": ["xx.xx@xx.com"],
        "cc": ["xx.xx@xx.com"]
    ```

## Run Test
```
python main.py
```