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

module.exports = async (sid, unique_identifier) => {
    const hour = eval(maxAge) || 2 * 60 * 60 * 1000;
    const data = {
        maxAge: hour,
        secure: secure,
        httpOnly: true,
        sameSite: 'lax'
    };

    logger.debug(`Secure Session: ${secure}`);
    logger.debug(`Session maxAge: ${hour}`);
    logger.debug(`Finding session ${sid} ...`);

    let session = await Session.findAll({
        where: {
            sid: sid,
            unique_identifier: unique_identifier
        }
    }).catch(error => {
        logger.error("ERROR FINDING SESSION");
        throw new ERRORS.InternalServerError(error);
    });

    if (session.length < 1) {
        logger.error("NO SESSION FOUND");
        throw new ERRORS.Forbidden();
    };

    if (session.length > 1) {
        logger.error("DUPLICATE SESSION FOUND");
        throw new ERRORS.Conflict();
    };

    logger.debug(`Updating session ${sid} ...`);

    await session[0].update({
        expires: new Date(Date.now() + hour),
        data: JSON.stringify(data)
    })

    logger.info("SUCCESSFULLY UPDATED SESSION");
    return {
        sid: session[0].sid,
        uid: session[0].unique_identifier,
        data: data
    };
}