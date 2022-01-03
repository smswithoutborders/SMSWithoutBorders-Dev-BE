let config = require('config'); //we load the db location from the JSON files
let DATABASE = config.get("DATABASE");
const Sequelize = require("sequelize");

module.exports = db = {};

initialize();

async function initialize() {
    // connect to db
    const sequelize = new Sequelize(DATABASE.MYSQL_DATABASE, DATABASE.MYSQL_USER, DATABASE.MYSQL_PASSWORD, {
        host: DATABASE.MYSQL_HOST,
        dialect: "mysql",
        logging: false,
        // define: {
        //     timestamps: false
        // }
    });

    // init models and add them to the exported db object
    db.sequelize = sequelize;
    db.Sequelize = Sequelize;

    db.users = require("./users.model.js")(sequelize, Sequelize);

    //db options
    const options = {
        alter: true,
        alter: {
            drop: false
        }
    }

    // sync all models with database
    await sequelize.sync(options);
}