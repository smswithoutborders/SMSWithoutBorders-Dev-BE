"use strict";

const express = require('express');
const router = express.Router();

const config = require('config');
const SERVER = config.get("SERVER");

let logger = require("../logger");

const fs = require('fs')
const ERRORS = require("../error.js");
const FIND_USERS = require("../models/find_users.models");
const STORE_SESSION = require("../models/store_sessions.models");
const STORE_USERS = require("../models/store_users.models");
const FIND_SESSION = require("../models/find_sessions.models");
const UPDATE_SESSION = require("../models/update_sessions.models");

var rootCas = require('ssl-root-cas').create()

require('https').globalAgent.options.ca = rootCas

// ==================== PRODUCTION ====================
if ((SERVER.hasOwnProperty("ssl_api") && SERVER.hasOwnProperty("PEM")) && fs.existsSync(SERVER.ssl_api.PEM)) {
    rootCas.addFile('/var/www/ssl/server.pem')
}

// =============================================================

module.exports = router;