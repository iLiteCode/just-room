const express = require("express");
const cors = require("cors");
const { PythonShell } = require("python-shell");

const app = express();
app.use(express.json());
app.use(cors());

app.post("/api/predict", (req, res) => {
  const { message } = req.body;

  if (!message) {
    return res.status(400).json({ error: "Message is required" });
  }

  let options = {
    mode: "text",
    pythonOptions: ["-u"],
    args: [message],
  };

  let predictionOutput = "";

  let pyshell = new PythonShell("predict.py", options);

  pyshell.on("message", function (message) {
    predictionOutput = message;
  });

  pyshell.end(function (err) {
    if (err) {
      console.error("Error ending PythonShell:", err);
      return res.status(500).send("Error ending PythonShell");
    }
    console.log("PythonShell process ended.");
    res.json({ prediction: predictionOutput });
  });
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
