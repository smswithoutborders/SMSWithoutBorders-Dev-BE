let express = require('express');
let app = express();
let morgan = require('morgan');
let fs = require("fs");
let path = require("path");
const cors = require("cors");
let config = require('config'); //we load the db location from the JSON files
const route = require('./route');
let db = require("./models");
const swaggerUi = require('swagger-ui-express');
const swaggerDocument = require("./docs/openapi.json");


let PORT = config.get("SERVER.PORT")
app.use(cors());

let options = ""

//db options
if (config.util.getEnv('NODE_ENV') !== 'test') {
    options = {
        alter: true,
        alter: {
            drop: false
        }
    }
} else {
    // clear database before running test 
    options = {
        force: true
    }
}

//db connection
db.sequelize.sync(options);

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

// Routes
route(app)

app.listen(PORT);
console.log("Listening on port " + PORT);

module.exports = app; // for testing