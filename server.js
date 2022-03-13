"use strict";

let config = require('config');
const SERVER = config.get("SERVER");

let express = require('express');
let app = express();

let morgan = require('morgan');
let fs = require("fs");
let path = require("path");
const cors = require("cors");
const swaggerUi = require('swagger-ui-express');

const checkIsSSL = require("./models/checkSSL.models");
let logger = require("./logger");

let cookieParser = require('cookie-parser');
const https = require("https")

const API_DOCS_V1 = require("./routes/api-docs-v1.json");

app.use(cors());
app.use(cookieParser());

//parse application/json and look for raw text
app.use(express.json());
app.use(express.urlencoded({
    extended: true
}));

// Create swagger docs
var options = {}
app.use('/v1/api-docs', swaggerUi.serveFiles(API_DOCS_V1, options), swaggerUi.setup(API_DOCS_V1));

// logger
let successLogStream = fs.createWriteStream(path.join(__dirname, "logs/http_success.log"), {
    flags: 'a'
})
let errorLogStream = fs.createWriteStream(path.join(__dirname, "logs/http_error.log"), {
    flags: 'a'
});

// setup the logger middleware
if (config.util.getEnv('NODE_ENV') !== 'test') {
    app.use([morgan('combined', {
            skip: function (req, res) {
                return (res.statusCode <= 599 && res.statusCode >= 400)
            },
            stream: successLogStream
        }),
        morgan('combined', {
            skip: function (req, res) {
                return (res.statusCode <= 399 && res.statusCode >= 100)
            },
            stream: errorLogStream
        })
    ]);

    if (config.util.getEnv('NODE_ENV') !== 'production') {
        app.use(morgan('dev'));
    } else {
        app.use(morgan('combined'));
    }
};

// ROUTES
let v1 = require("./routes/v1");
app.use("/v1", v1);

// Check SSL
let isSSL = checkIsSSL(SERVER.ssl_api.CERTIFICATE, SERVER.ssl_api.KEY, SERVER.ssl_api.PEM);
let httpsServer = ""

if (config.util.getEnv('NODE_ENV') !== 'production') {
    logger.debug(`Environment: ${config.util.getEnv('NODE_ENV')}`);
    logger.warn("This is a development server. Do not use it in a production deployment.");

    if (isSSL) {
        httpsServer = https.createServer(isSSL.credentials, app);
        httpsServer.listen(SERVER.ssl_api.API_PORT);
        logger.info("Running secured on port: " + SERVER.ssl_api.API_PORT)
        app.runningPort = SERVER.ssl_api.API_PORT
        app.is_ssl = true
    } else {
        logger.info("Running in-secured on port: " + SERVER.api.PORT)
        app.listen(SERVER.api.PORT);
        app.runningPort = SERVER.api.PORT
        app.is_ssl = false
    }
} else {
    logger.debug(`Environment: ${config.util.getEnv('NODE_ENV')}`);

    if (isSSL) {
        httpsServer = https.createServer(isSSL.credentials, app);
        httpsServer.listen(SERVER.ssl_api.API_PORT);
        logger.info("Running secured on port: " + SERVER.ssl_api.API_PORT)
        app.runningPort = SERVER.ssl_api.API_PORT
        app.is_ssl = true
    } else {
        logger.info("Running in-secured on port: " + SERVER.api.PORT)
        app.listen(SERVER.api.PORT);
        app.runningPort = SERVER.api.PORT
        app.is_ssl = false
    }
};

module.exports = app; // for testing