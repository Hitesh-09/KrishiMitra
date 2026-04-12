const express = require("express");

const app = express();

// Middleware
app.use(express.json());

// Routes
const indexRoutes = require("./routes/index");
app.use("/", indexRoutes);

module.exports = app;