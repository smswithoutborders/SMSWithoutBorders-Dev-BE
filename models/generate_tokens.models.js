"use strict";

const ERRORS = require("../error.js");
let logger = require("../logger");
let HashGen = require("../tools/hash_generator.js");

module.exports = async (user) => {
    let generator = new HashGen();

    logger.debug(`Generating tokens for ${user.email} ...`);
    await user.update({
        auth_id: generator.hash(32),
        auth_key: generator.hash(32)
    }).catch(error => {
        logger.error("ERROR GENERATING USER'S TOKENS");
        throw new ERRORS.InternalServerError(error);
    })

    logger.info("TOKENS SUCCESSFULLY GENERATED");
    return {
        auth_key: user.auth_key,
        auth_id: user.auth_id
    }
}