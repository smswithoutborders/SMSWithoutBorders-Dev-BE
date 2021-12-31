module.exports = (sequelize, Sequelize) => {
    let Users = sequelize.define("users", {
        id: {
            type: Sequelize.STRING(64),
            primaryKey: true
        },
        email: {
            type: Sequelize.STRING,
            unique: true
        },
        password: Sequelize.STRING,
        session_id: Sequelize.STRING,
        auth_key: {
            type: Sequelize.STRING,
            unique: true
        },
        auth_id: {
            type: Sequelize.STRING,
            unique: true
        }
    });

    return Users;
}