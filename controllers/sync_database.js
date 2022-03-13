const config = require('config');
const SERVER = config.get("SERVER");

const mysql = require('mysql2/promise');

//db connection
mysql.createConnection({
    host: SERVER.database.MYSQL_HOST,
    user: SERVER.database.MYSQL_USER,
    password: SERVER.database.MYSQL_PASSWORD,
}).then(connection => {
    console.log(`Creating Database ${SERVER.database.MYSQL_DATABASE} ...`)
    connection.query(`CREATE DATABASE IF NOT EXISTS \`${SERVER.database.MYSQL_DATABASE}\`;`)
        .then(() => {
            console.log("Synchronizing database schema ...");
            setTimeout(async () => {
                process.exit();
            }, 3000)
        })
})