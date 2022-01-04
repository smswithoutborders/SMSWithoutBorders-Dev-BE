//During the test the env variable is set to test
process.env.NODE_ENV = 'test';

//Require the dev-dependencies
let chai = require('chai');
let assert = chai.assert;
let HashGen = require("../tools/hash_generator.js");

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