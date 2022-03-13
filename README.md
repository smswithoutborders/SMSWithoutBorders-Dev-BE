## SMSwithoutBorders DevAPI Guide

### Requirements
- MySQL (MariaDB)
- nodejs
- npm

### Getting Started

**Clone the Project**
```
git clone https://github.com/smswithoutborders/SMSWithoutBorders-DevAPI.git
```

**Installation**

* Install all node packages
```
npm install
```

**Setup**

- Create configuration files

    __config (./config)__

    * Copy the template file "example.default.json" and rename to "default.json"
        ```
        cp config/example.default.json config/default.json
        ```
        > This is required to run the API server
    * Copy the template file "example.test.json" and rename to "test.json"
        ```
        cp config/example.test.json config/test.json
        ```
        > This is required to run the API tests 
        
**Start Sever**
```
npm start
```

**Run TESTS**
```
npm test
```

**API SandBox**
```
<host>:{PORT}/{version}/api-docs/
```
