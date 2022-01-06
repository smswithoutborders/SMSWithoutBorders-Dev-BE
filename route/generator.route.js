let db = require("../models");
const Errors = require('../error.js');
let HashGen = require("../tools/hash_generator.js");

let USERS = db.users;

module.exports = (app) => {
    app.post("/users/:id/token", async (req, res) => {
        try {
            // ==================== REQUEST BODY CHECKS ====================
            if (!req.params.id) {
                throw new Errors.BadRequest("User_id cannot be empty");
            };

            if (!req.body.session_id) {
                throw new Errors.BadRequest("Session_id cannot be empty");
            };
            // ============================================================+

            let generator = new HashGen();
            let session_id = req.body.session_id;
            let id = req.params.id

            let user = await USERS.findAll({
                where: {
                    id: id,
                    session_id: session_id
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
                auth_id: generator.hash(32),
                auth_key: generator.hash(32)
            }).catch(error => {
                throw new Errors.InternalServerError(error);
            });

            return res.status(200).json({
                auth_key: user[0].auth_key,
                auth_id: user[0].auth_id
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

    app.put("/users/:id/token", async (req, res) => {
        try {
            // ==================== REQUEST BODY CHECKS ====================
            if (!req.params.id) {
                throw new Errors.BadRequest("User_id cannot be empty");
            };

            if (!req.body.session_id) {
                throw new Errors.BadRequest("Session_id cannot be empty");
            };
            // ============================================================+

            let generator = new HashGen();
            let session_id = req.body.session_id;
            let id = req.params.id

            let user = await USERS.findAll({
                where: {
                    id: id,
                    session_id: session_id
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
                auth_key: generator.hash(32)
            }).catch(error => {
                throw new Errors.InternalServerError(error);
            });

            return res.status(200).json({
                auth_key: user[0].auth_key,
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