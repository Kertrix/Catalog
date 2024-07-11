const express = require("express");
const cors = require("cors");
const path = require("path");
const yaml = require("js-yaml");
const fs = require("fs");

const app = express();
const port = 8000;

app.use(cors());

app.get("/", (req, res) => {
  res.header("Content-Type", "application/json");
  res.sendFile(path.join(__dirname, "catalog.json"));
});

app.get("/detail/:id", (req, res) => {
  // Send the YAML file for the requested item (in JSON)
  const id = req.params.id;
  try {
    const doc = yaml.load(
      fs.readFileSync(
        path.join(__dirname, "catalog", `${id}/${id}.yaml`),
        "utf8"
      )
    );
    res.json(doc);
  } catch (e) {
    res.status(404).send("Not found");
  }
});

app.get("/detail/:id/bib", (req, res) => {
  // Send the bib file for the requested item
  const id = req.params.id;
  try {
    const bibFileContent = fs.readFileSync(
      path.join(__dirname, "catalog", `${id}/${id}.bib`),
      "utf8"
    );
    res.set("Content-Type", "text/plain");
    res.send(bibFileContent);
  } catch (e) {
    res.status(404).send("Not found");
  }
});

app.listen(port, () => {
  console.log(`Document Datasets API listening on port ${port}`);
});
