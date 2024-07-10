const express = require("express");
const path = require("path");

const app = express();
const port = 8000;

app.use(cors());

app.get("/", (req, res) => {
  res.header("Content-Type", "application/json");
  res.sendFile(path.join(__dirname, "catalog.json"));
});

app.listen(port, () => {
  console.log(`Document Datasets API listening on port ${port}`);
});
