const express = require("express");

const app = express();

// Middleware
app.use(express.json());

// Routes
const indexRoutes = require("./routes/index");
const farmerRoutes = require("./modules/farmer/routes/farmerRoutes");

app.use("/", indexRoutes);
app.use("/api/farmers", farmerRoutes);

module.exports = app;