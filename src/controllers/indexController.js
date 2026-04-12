const getHome = (req, res) => {
  res.json({ message: "KrishiMitra API is running" });
};

module.exports = {
  getHome,
};