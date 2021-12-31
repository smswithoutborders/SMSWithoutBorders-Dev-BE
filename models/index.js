let config = require('config'); //we load the db location from the JSON files
let DATABASE = config.get("DATABASE");
const Sequelize = require("sequelize");

var sequelize = new Sequelize(DATABASE.MYSQL_DATABASE, DATABASE.MYSQL_USER, DATABASE.MYSQL_PASSWORD, {
    host: DATABASE.MYSQL_HOST,
    dialect: "mysql",
    logging: false,
    // define: {
    //     timestamps: false
    // }
});

var db = {};

db.sequelize = sequelize;
db.Sequelize = Sequelize;

db.users = require("./users.model.js")(sequelize, Sequelize);

module.exports = db;