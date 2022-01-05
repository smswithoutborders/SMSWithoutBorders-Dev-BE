let db = require("../models");
const Errors = require('../error.js');
const {
    v1: uuidv1
} = require('uuid');

let USERS = db.users;

module.exports = (app) => {
    app.post("/signup", async (req, res) => {
        try {
            // ==================== REQUEST BODY CHECKS ====================
            if (!req.body.email) {
                throw new Errors.BadRequest("Email cannot be empty");
            };

            if (!req.body.password) {
                throw new Errors.BadRequest("Password cannot be empty");
            };
            // ============================================================+

            let email = req.body.email;
            let password = req.body.password;

            await USERS.create({
                id: uuidv1(),
                email: email,
                password: password,
            }).catch(error => {
                if (error.name == "SequelizeUniqueConstraintError") {
                    if (error.original.code == "ER_DUP_ENTRY") {
                        throw new Errors.Conflict("DUPLICATE USERS");
                    };
                };

                throw new Errors.InternalServerError(error);
            });

            return res.status(200).json({
                message: "SUCCESS"
            })

        } catch (err) {
            if (err instanceof Errors.BadRequest)
                return res.status(400).send({
                    message: err.message
                }); // 400
            if (err instanceof Errors.Conflict)
                return res.status(409).send({
                    message: err.message
                }); // 409
            console.log(err);
            return res.status(500).send({
                error: err,
                message: err.message
            });
        }
    });

}