"use strict"

const fs = require("fs");
const config = require('config');
const SERVER = config.get("SERVER");

module.exports = (path_crt_file, path_key_file, path_pem_file) => {
    if ((SERVER.hasOwnProperty("ssl_api")) && fs.existsSync(path_crt_file) && fs.existsSync(path_key_file) && fs.existsSync(path_pem_file)) {
        let privateKey = fs.readFileSync(SERVER.ssl_api.KEY, 'utf8');
        let certificate = fs.readFileSync(SERVER.ssl_api.CERTIFICATE, 'utf8');

        let ca = [
            fs.readFileSync(SERVER.ssl_api.PEM)
        ]

        return {
            credentials: {
                key: privateKey,
                cert: certificate,
                ca: ca
            }
        };
    } else {
        return false;
    }
}