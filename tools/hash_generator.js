const {
    createHmac,
    randomBytes
} = require('crypto');

class Generator {
    hash(length) {
        let r_hash = randomBytes(length/2).toString('hex');

        return r_hash
    };

    _256(salt, string) {
        const SALT = salt;
        const hash = createHmac('sha256', SALT)
            .update(string)
            .digest('hex');
        return hash;
    };
};

module.exports = Generator;