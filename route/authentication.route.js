let config = require('config'); //we load the db location from the JSON files
const SECRET = config.get("SERVER.SECRET");
let db = require("../models");
const Errors = require('../error.js');
const {
    v1: uuidv1
} = require('uuid');
let HashGen = require("../tools/hash_generator.js");

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

            let generator = new HashGen();
            let email = req.body.email;
            let password = generator._256(SECRET, req.body.password);

            await USERS.create({
                id: uuidv1(),
                email: email,
                password: password
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

    app.post("/signin", async (req, res) => {
        try {
            // ==================== REQUEST BODY CHECKS ====================
            if (!req.body.email) {
                throw new Errors.BadRequest("Email cannot be empty");
            };

            if (!req.body.password) {
                throw new Errors.BadRequest("Password cannot be empty");
            };
            // ============================================================+

            let generator = new HashGen();
            let email = req.body.email;
            let password = generator._256(SECRET, req.body.password);

            let user = await USERS.findAll({
                where: {
                    email: email,
                    password: password
                }
            }).catch(error => {
                throw new Errors.InternalServerError(error);
            });

            // INVALID USER
            if (user.length < 1) {
                throw new Errors.Forbidden("USER NOT FOUND");
            };

            // DUPLICATE USERS
            if (user.length > 1) {
                throw new Errors.Conflict("DUPLICATE USERS");
            };

            await user[0].update({
                session_id: generator.hash(32)
            }).catch(error => {
                throw new Errors.InternalServerError(error);
            });

            return res.status(200).json({
                id: user[0].id,
                email: user[0].email,
                session_id: user[0].session_id,
                auth_key: user[0].auth_key,
                auth_id: user[0].auth_id
            });

        } catch (err) {
            if (err instanceof Errors.BadRequest)
                return res.status(400).send({
                    message: err.message
                }); // 400
            if (err instanceof Errors.Forbidden)
                return res.status(401).send({
                    message: err.message
                }); // 401
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