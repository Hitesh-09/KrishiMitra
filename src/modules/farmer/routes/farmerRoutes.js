const express = require("express");
const router = express.Router();

const { getFarmers, createFarmer, getFarmerById, updateFarmer, deleteFarmer } = require("../controllers/farmerController");

router.get("/", getFarmers);
router.post("/", createFarmer);
router.get("/:id", getFarmerById);
router.put("/:id", updateFarmer);
router.delete("/:id", deleteFarmer);

module.exports = router;