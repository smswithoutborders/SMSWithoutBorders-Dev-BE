//During the test the env variable is set to test
process.env.NODE_ENV = 'test';

//Require the dev-dependencies
let chai = require('chai');
let chaiHttp = require('chai-http');
let server = require('../index');
let assert = chai.assert;

chai.use(chaiHttp);

//Our parent block
describe('Authentication', function () {

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
    });

    describe('/POST /signin', function () {
        it('it should AUTHENTICATE a USER', function (done) {
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
        });
    });

});