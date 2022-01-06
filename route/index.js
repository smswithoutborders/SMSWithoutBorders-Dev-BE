module.exports = (app) => {
    require("./authentication.route")(app);
    require("./generator.route")(app);
}