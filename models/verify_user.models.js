"use strict";

const ERRORS = require("../error.js");
const db = require("../schemas");
const Security = require("./security.models.js");
const config = require('config');
const SERVER = config.get("SERVER");
let logger = require("../logger");

let User = db.users;

module.exports = async (email, password) => {
    let security = new Security();

    // SEARCH FOR USERINFO IN DB
    logger.debug(`Verifying user ${email} ...`);
    let user = await User.findAll({
        where: {
            email: email,
            password: security.hash(password)
        }
    }).catch(error => {
        logger.error("ERROR VERIFYING USER");
        throw new ERRORS.InternalServerError(error);
    });

    if (user.length < 1) {
        logger.error("NO USER FOUND");
        throw new ERRORS.Unauthorized();
    };

    if (user.length > 1) {
        logger.error("DUPLICATE USERS FOUND");
        throw new ERRORS.Conflict();
    };

    logger.info("USER SUCCESSFULLY AUTHENTICATED");
    return user[0].id;
}