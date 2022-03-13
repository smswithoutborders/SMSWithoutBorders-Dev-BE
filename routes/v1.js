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
const VERIFY_USERS = require("../models/verify_user.models");

var rootCas = require('ssl-root-cas').create()

require('https').globalAgent.options.ca = rootCas

// ==================== PRODUCTION ====================
if ((SERVER.hasOwnProperty("ssl_api") && SERVER.hasOwnProperty("PEM")) && fs.existsSync(SERVER.ssl_api.PEM)) {
    rootCas.addFile('/var/www/ssl/server.pem')
}

router.post("/signup",
    async (req, res) => {
        try {
            // ==================== REQUEST BODY CHECKS ====================
            if (!req.body.email) {
                logger.error("NO EMAIL");
                throw new ERRORS.BadRequest();
            };

            if (!req.body.password) {
                logger.error("NO PASSWORD");
                throw new ERRORS.BadRequest();
            };
            // ============================================================+

            let email = req.body.email;
            let password = req.body.password;

            await STORE_USERS(email, password);

            return res.status(200).json();
        } catch (err) {
            if (err instanceof ERRORS.BadRequest) {
                return res.status(400).send(err.message);
            } // 400
            if (err instanceof ERRORS.Forbidden) {
                return res.status(403).send(err.message);
            } // 403
            if (err instanceof ERRORS.Unauthorized) {
                return res.status(401).send(err.message);
            } // 401
            if (err instanceof ERRORS.Conflict) {
                return res.status(409).send(err.message);
            } // 409
            if (err instanceof ERRORS.NotFound) {
                return res.status(404).send(err.message);
            } // 404

            logger.error(err);
            return res.status(500).send("internal server error");
        }
    });

router.post("/login",
    async (req, res) => {
        try {
            // ==================== REQUEST BODY CHECKS ====================
            if (!req.body.email) {
                logger.error("NO EMAIL");
                throw new ERRORS.BadRequest();
            };

            if (!req.body.password) {
                logger.error("NO PASSWORD");
                throw new ERRORS.BadRequest();
            };
            // ============================================================+

            let email = req.body.email;
            let password = req.body.password;
            const USER_AGENT = req.get("user-agent");

            const USERID = await VERIFY_USERS(email, password);
            let user = await FIND_USERS(USERID);
            let session = await STORE_SESSION(USERID, USER_AGENT);

            res.cookie("SWOBDev", {
                sid: session.sid,
                cookie: session.data
            }, session.data)

            return res.status(200).json({
                uid: user.id,
                email: user.email,
                auth_key: user.auth_key,
                auth_id: user.auth_id
            });
        } catch (err) {
            if (err instanceof ERRORS.BadRequest) {
                return res.status(400).send(err.message);
            } // 400
            if (err instanceof ERRORS.Forbidden) {
                return res.status(403).send(err.message);
            } // 403
            if (err instanceof ERRORS.Unauthorized) {
                return res.status(401).send(err.message);
            } // 401
            if (err instanceof ERRORS.Conflict) {
                return res.status(409).send(err.message);
            } // 409
            if (err instanceof ERRORS.NotFound) {
                return res.status(404).send(err.message);
            } // 404

            logger.error(err);
            return res.status(500).send("internal server error");
        }
    });

// =============================================================

module.exports = router;