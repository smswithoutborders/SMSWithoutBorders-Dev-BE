const config = require('config');
const SERVER = config.get("SERVER");

const Sequelize = require("sequelize");

module.exports = db = {};

initialize();

async function initialize() {
    // connect to db
    const sequelize = new Sequelize(SERVER.database.MYSQL_DATABASE, SERVER.database.MYSQL_USER, SERVER.database.MYSQL_PASSWORD, {
        host: SERVER.database.MYSQL_HOST,
        dialect: "mysql",
        logging: false,
        // define: {
        //     timestamps: false
        // }
    });

    // init models and add them to the exported db object
    db.sequelize = sequelize;
    db.Sequelize = Sequelize;

    db.users = require("./users.schema.js")(sequelize, Sequelize);
    db.sessions = require("./sessions.schema.js")(sequelize, Sequelize);

    // https://sequelize.org/master/manual/assocs.html

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