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
<host>:9000/api-docs/
```
