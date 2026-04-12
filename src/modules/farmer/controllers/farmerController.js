let farmers = [];

const getFarmers = (req, res) => {
  res.json({
    message: "List of farmers",
    data: farmers,
  });
};

const createFarmer = (req, res) => {
  const { name, location } = req.body;

  if (!name || !location) {
    return res.status(400).json({
      message: "Name and location are required",
    });
  }

  const newFarmer = {
    id: farmers.length + 1,
    name,
    location,
  };

  farmers.push(newFarmer);

  res.status(201).json({
    message: "Farmer created",
    data: newFarmer,
  });
};

const getFarmerById = (req, res) => {
  const id = parseInt(req.params.id);

  console.log("Param ID:", req.params.id);
  console.log("Farmers:", farmers);

  const farmer = farmers.find(f => f.id === id);

  if (!farmer) {
    return res.status(404).json({
      message: "Farmer not found",
    });
  }

  res.json({
    message: "Farmer fetched",
    data: farmer,
  });
};

const updateFarmer = (req, res) => {
  const id = parseInt(req.params.id);
  const { name, location } = req.body;

  const farmer = farmers.find(f => f.id === id);

  if (!farmer) {
    return res.status(404).json({
      message: "Farmer not found",
    });
  }

  if (!name || !location) {
    return res.status(400).json({
      message: "Name and location are required",
    });
  }

  farmer.name = name;
  farmer.location = location;

  res.json({
    message: "Farmer updated",
    data: farmer,
  });
};

const deleteFarmer = (req, res) => {
  const id = parseInt(req.params.id);

  const index = farmers.findIndex(f => f.id === id);

  if (index === -1) {
    return res.status(404).json({
      message: "Farmer not found",
    });
  }

  const deletedFarmer = farmers[index];
  farmers.splice(index, 1);

  res.json({
    message: "Farmer deleted",
    data: deletedFarmer,
  });
};

module.exports = {
  getFarmers,
  createFarmer,
  getFarmerById,
  updateFarmer,
  deleteFarmer,
};