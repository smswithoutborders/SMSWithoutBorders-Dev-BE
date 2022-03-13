"use strict";

const ERRORS = require("../error.js");
const db = require("../schemas");
let logger = require("../logger");

const config = require('config');
const SERVER = config.get("SERVER");
let secure = "";
if (SERVER.api.SECURE_SESSIONS == undefined) {
    secure = true;
} else {
    secure = SERVER.api.SECURE_SESSIONS
}
const maxAge = SERVER.api.SESSION_MAXAGE;

var Session = db.sessions;

module.exports = async (unique_identifier, user_agent) => {
    const hour = eval(maxAge) || 2 * 60 * 60 * 1000;
    const data = {
        maxAge: hour,
        secure: secure,
        httpOnly: true,
        sameSite: 'lax'
    }

    logger.debug(`Secure Session: ${secure}`);
    logger.debug(`Session maxAge: ${hour}`);
    logger.debug(`Creating session for ${unique_identifier} ...`);

    let session = await Session.create({
        unique_identifier: unique_identifier,
        user_agent: user_agent,
        expires: new Date(Date.now() + hour),
        data: JSON.stringify(data)
    }).catch(error => {
        logger.error("ERROR CREATING SESSION")
        throw new ERRORS.InternalServerError(error);
    });

    logger.info("SUCCESSFULLY CREATED SESSION");

    return {
        sid: session.sid,
        uid: session.unique_identifier,
        data: data
    };
}