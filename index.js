let express = require('express');
let app = express();
let morgan = require('morgan');
let fs = require("fs");
let path = require("path");
const cors = require("cors");
let config = require('config'); //we load the db location from the JSON files
const route = require('./route');
const swaggerUi = require('swagger-ui-express');
const swaggerDocument = require("./docs/openapi.json");
const PORT = config.get("SERVER.PORT");
const DATBASE = config.get("DATABASE");
const mysql = require('mysql2/promise');

app.use(cors());

// Create swagger docs
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDocument));

//don't show the log when it is test
if (config.util.getEnv('NODE_ENV') !== 'test') {
    //use morgan to log at command line and file
    // create a write stream (in append mode)
    var accessLogStream = fs.createWriteStream(path.join(__dirname, 'logs/access.log'), {
        flags: 'a'
    })

    // setup the logger
    app.use(morgan('combined', {
        stream: accessLogStream
    })) //'combined' outputs the Apache style LOGs
    app.use(morgan('dev'))
}

//parse application/json and look for raw text
app.use(express.json());
app.use(express.urlencoded({
    extended: true
}));

//db connection
mysql.createConnection({
    host: DATBASE.MYSQL_HOST,
    user: DATBASE.MYSQL_USER,
    password: DATBASE.MYSQL_PASSWORD,
}).then(connection => {
    connection.query(`CREATE DATABASE IF NOT EXISTS \`${DATBASE.MYSQL_DATABASE}\`;`).then(() => {
        // Routes
        route(app)

        // start server
        app.listen(PORT, () => {
            if (config.util.getEnv('NODE_ENV') !== 'test') {
                console.log(`SERVER RUNNING ON PORT: ${PORT}`);
            }
        });
    })
})

module.exports = app; // for testing