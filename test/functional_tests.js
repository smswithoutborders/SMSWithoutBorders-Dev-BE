//During the test the env variable is set to test
process.env.NODE_ENV = 'test';

//Require the dev-dependencies
let chai = require('chai');
let chaiHttp = require('chai-http');
let server = require('../index');
let assert = chai.assert;
let config = require('config'); //we load the db location from the JSON files
const PORT = config.get("SERVER.PORT");
let db = require("../models");
let USERS = db.users;
let HashGen = require("../tools/hash_generator.js");

chai.use(chaiHttp);

//Our parent block
describe('Functional Tests', function () {

    describe('Authentication', function () {
        // Each test should completely test the response of the API end-point including response status code!

        console.log(`SERVER RUNNING ON PORT: ${PORT}`);

        before('Clear database', async function () {
            await USERS.destroy({
                where: {}
            })
        });

        describe('/POST /signup', function () {
            it('it should CREATE a USER', function (done) {
                chai.request(server)
                    .post('/signup')
                    .send({
                        email: "test@test.com",
                        password: "testpassword"
                    })
                    .end((err, res) => {
                        if (err) {
                            return console.log(err)
                        }

                        assert.equal(res.status, 200, "request successful");
                        assert.typeOf(res.body, "object", "response is an OBJECT");
                        assert.property(res.body, "message", "response has property message");
                        done();
                    });
            });

            it('it should FAIL with no EMAIL', function (done) {
                chai.request(server)
                    .post('/signup')
                    .send({
                        email: "",
                        password: "testpassword"
                    })
                    .end((err, res) => {
                        if (err) {
                            return console.log(err)
                        }

                        assert.equal(res.status, 400, "request Failed");
                        assert.typeOf(res.body, "object", "response is an OBJECT");
                        assert.property(res.body, "message", "response has property message");
                        done();
                    });
            });

            it('it should FAIL with no PASSWORD', function (done) {
                chai.request(server)
                    .post('/signup')
                    .send({
                        email: "test@test.com",
                        password: ""
                    })
                    .end((err, res) => {
                        if (err) {
                            return console.log(err)
                        }

                        assert.equal(res.status, 400, "request Failed");
                        assert.typeOf(res.body, "object", "response is an OBJECT");
                        assert.property(res.body, "message", "response has property message");
                        done();
                    });
            });

            it('it should FAIL with duplicate EMAIL', function (done) {
                chai.request(server)
                    .post('/signup')
                    .send({
                        email: "test@test.com",
                        password: "testpassword"
                    })
                    .end((err, res) => {
                        if (err) {
                            return console.log(err)
                        }

                        assert.equal(res.status, 409, "request Failed");
                        assert.typeOf(res.body, "object", "response is an OBJECT");
                        assert.property(res.body, "message", "response has property message");
                        done();
                    });
            });
        });

        describe('/POST /signin', function () {
            it('it should AUTHENTICATE a USER', function (done) {
                chai.request(server)
                    .post('/signin')
                    .send({
                        email: "test@test.com",
                        password: "testpassword"
                    })
                    .end((err, res) => {
                        if (err) {
                            return console.log(err)
                        }

                        assert.equal(res.status, 200, "request successful");
                        assert.typeOf(res.body, "object", "response is an OBJECT");
                        assert.property(res.body, "Id", "response has property Id");
                        assert.property(res.body, "email", "response has property email");
                        assert.property(res.body, "auth_key", "response has property auth_key");
                        assert.property(res.body, "auth_id", "response has property auth_id");
                        assert.notProperty(res.body, "password", "response should not have property password");
                        assert.property(res.body, "session_id", "response has property session_id");
                        done();
                    });
            });

            it('it should FAIL with no EMAIL', function (done) {
                chai.request(server)
                    .post('/signin')
                    .send({
                        email: "",
                        password: "testpassword"
                    })
                    .end((err, res) => {
                        if (err) {
                            return console.log(err)
                        }

                        assert.equal(res.status, 400, "request Failed");
                        assert.typeOf(res.body, "object", "response is an OBJECT");
                        assert.property(res.body, "message", "response has property message");
                        done();
                    });
            });

            it('it should FAIL with no PASSWORD', function (done) {
                chai.request(server)
                    .post('/signin')
                    .send({
                        email: "test@test.com",
                        password: ""
                    })
                    .end((err, res) => {
                        if (err) {
                            return console.log(err)
                        }

                        assert.equal(res.status, 400, "request Failed");
                        assert.typeOf(res.body, "object", "response is an OBJECT");
                        assert.property(res.body, "message", "response has property message");
                        done();
                    });
            });

            it('it should FAIL with duplicate EMAIL', function (done) {
                chai.request(server)
                    .post('/signin')
                    .send({
                        email: "test@test.com",
                        password: "testpassword"
                    })
                    .end((err, res) => {
                        if (err) {
                            return console.log(err)
                        }

                        assert.equal(res.status, 409, "request Failed");
                        assert.typeOf(res.body, "object", "response is an OBJECT");
                        assert.property(res.body, "message", "response has property message");
                        done();
                    });
            });

            it('it should FAIL with invalid PASSWORD', function (done) {
                chai.request(server)
                    .post('/signin')
                    .send({
                        email: "test@test.com",
                        password: "invalidtestpassword"
                    })
                    .end((err, res) => {
                        if (err) {
                            return console.log(err)
                        }

                        assert.equal(res.status, 401, "request Failed");
                        assert.typeOf(res.body, "object", "response is an OBJECT");
                        assert.property(res.body, "message", "response has property message");
                        done();
                    });
            });

            it('it should FAIL with invalid EMAIL', function (done) {
                chai.request(server)
                    .post('/signin')
                    .send({
                        email: "invalidtest@test.com",
                        password: "testpassword"
                    })
                    .end((err, res) => {
                        if (err) {
                            return console.log(err)
                        }

                        assert.equal(res.status, 401, "request Failed");
                        assert.typeOf(res.body, "object", "response is an OBJECT");
                        assert.property(res.body, "message", "response has property message");
                        done();
                    });
            });
        });
    });

    describe('Hash Test', function () {
        it('random_hash', function (done) {
            let generator = new HashGen()
            let length = 32
            let result = generator.hash(length);

            assert.typeOf(result, "string", "Hash should be a string");
            assert.lengthOf(result, length, "Hash should be of length 32");
            done();
        });

        it('256', function (done) {
            let generator = new HashGen()
            let salt = "test@secret";
            let string = "98104d23-2ac8-4c4e-aa15-2d246efde76d";
            let length = 64;
            let test = "ca917ddc83026327be0c61e5c0d0bd5249ac7371c6a57a97ec9aad367d24c5ff";
            let result = generator._256(salt, string);

            assert.typeOf(result, "string", "Hash_256 should be a string");
            assert.lengthOf(result, length, "Hash_256 should be of length 64");
            assert.strictEqual(result, test, "Hash_256 should match test Hash");
            done();
        });
    });

});