"use strict";

const ERRORS = require("../error.js");
const db = require("../schemas");
let logger = require("../logger");

let User = db.users;

module.exports = async (uid, auth_id, auth_key) => {
    logger.debug(`Verifying tokens for ${uid} ...`);
    let user = await User.findAll({
        where: {
            id: uid,
            auth_id: auth_id,
            auth_key: auth_key
        }
    }).catch(error => {
        logger.error("ERROR VERIFYING TOKENS");
        throw new ERRORS.InternalServerError(error);
    });

    if (user.length < 1) {
        logger.error("NO TOKEN FOUND");
        throw new ERRORS.Forbidden();
    };

    if (user.length > 1) {
        logger.error("DUPLICATE TOKENS FOUND");
        throw new ERRORS.Conflict();
    };

    logger.info("TOKEN SUCCESSFULLY AUTHENTICATED");
    return user[0].id;
}