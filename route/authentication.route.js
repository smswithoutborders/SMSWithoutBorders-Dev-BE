let db = require("../models");
const {
    ErrorHandler
} = require('../error.js');
const {
    v1: uuidv1
} = require('uuid');

let USERS = db.users;

module.exports = (app) => {
    app.post("/signup", async (req, res, next) => {
        try {
            // ==================== REQUEST BODY CHECKS ====================
            if (!req.body.email) {
                throw new ErrorHandler(400, "Email cannot be empty");
            };

            if (!req.body.password) {
                throw new ErrorHandler(400, "Password cannot be empty");
            };
            // ============================================================+

            let email = req.body.email;
            let password = req.body.password;

            let user = await USERS.findAll({
                where: {
                    email: email
                }
            }).catch(error => {
                throw new ErrorHandler(500, error);
            });

            // IF MORE THAN ONE USER EXIST IN DATABASE
            if (user.length > 0) {
                throw new ErrorHandler(409, "DUPLICATE USERS");
            } else {
                let newUser = await USERS.create({
                    id: uuidv1(),
                    email: email,
                    password: password,
                }).catch(error => {
                    throw new ErrorHandler(500, error);
                });

                return res.status(200).json({
                    message: "SUCCESS"
                })
            };
        } catch (error) {
            next(error);
        }
    });

}