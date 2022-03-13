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
const GENERATE_TOKENS = require("../models/generate_tokens.models")
const VERIFY_TOKENS = require("../models/verify_tokens.models")

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

router.get("/users/:user_id/tokens",
    async (req, res) => {
        try {
            if (!req.params.user_id) {
                logger.error("NO USERID");
                throw new ERRORS.BadRequest();
            };

            if (!req.cookies.SWOBDev) {
                logger.error("NO COOKIE");
                throw new ERRORS.Unauthorized();
            };

            const SID = req.cookies.SWOBDev.sid;
            const UID = req.params.user_id;
            const COOKIE = req.cookies.SWOBDev.cookie;
            const USER_AGENT = req.get("user-agent");

            const ID = await FIND_SESSION(SID, UID, USER_AGENT, COOKIE);
            let user = await FIND_USERS(ID);
            let tokens = await GENERATE_TOKENS(user);

            let session = await UPDATE_SESSION(SID, ID)

            res.cookie("SWOBDev", {
                sid: session.sid,
                cookie: session.data
            }, session.data)

            return res.status(200).json(tokens);
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

router.post("/users/:user_id/authenticate",
    async (req, res) => {
        try {
            if (!req.params.user_id) {
                logger.error("NO USERID");
                throw new ERRORS.BadRequest();
            };

            if (!req.cookies.SWOBDev) {
                logger.error("NO COOKIE");
                throw new ERRORS.Unauthorized();
            };

            // ==================== REQUEST BODY CHECKS ====================
            if (!req.body.auth_id) {
                logger.error("NO AUTH ID");
                throw new ERRORS.BadRequest();
            };

            if (!req.body.auth_key) {
                logger.error("NO NO AUTH KEY");
                throw new ERRORS.BadRequest();
            };
            // ============================================================+

            const SID = req.cookies.SWOBDev.sid;
            const UID = req.params.user_id;
            const COOKIE = req.cookies.SWOBDev.cookie;
            const USER_AGENT = req.get("user-agent");
            const AUTH_ID = req.body.auth_id;
            const AUTH_KEY = req.body.auth_key;

            const ID = await FIND_SESSION(SID, UID, USER_AGENT, COOKIE);
            const USERID = await VERIFY_TOKENS(ID, AUTH_ID, AUTH_KEY);

            let session = await UPDATE_SESSION(SID, USERID);

            res.cookie("SWOBDev", {
                sid: session.sid,
                userAgent: USER_AGENT,
                uid: USERID,
                cookie: session.data
            }, session.data)

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

// =============================================================

module.exports = router;