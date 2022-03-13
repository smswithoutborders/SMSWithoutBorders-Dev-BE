"use strict";

const ERRORS = require("../error.js");
const db = require("../schemas");
const config = require('config');
const Security = require("./security.models.js");
const SERVER = config.get("SERVER");
const KEY = SERVER.api.KEY;

let logger = require("../logger");

const User = db.users;

module.exports = async (email, password) => {
    let security = new Security(KEY);

    logger.debug(`Creating User ${email} ...`);

    let newUser = await User.create({
        email: email,
        password: security.hash(password),
    }).catch(error => {
        logger.error("ERROR CREATING USER");
        if (error.name == "SequelizeUniqueConstraintError") {
            if (error.original.code == "ER_DUP_ENTRY") {
                logger.error("USER ALREADY HAS RECORD");
                throw new ERRORS.Conflict();
            };
        };

        throw new ERRORS.InternalServerError(error);
    });

    logger.info("SUCCESSFULLY CREATED USER");
    return newUser.id;
}