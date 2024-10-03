const express = require("express");
const bodyParser = require("body-parser");
const { PythonShell } = require("python-shell");
const axios = require("axios");
const base64 = require("base-64");
const cors = require("cors");

const app = express();
app.use(bodyParser.json());
app.use(cors());

const API_KEY =
  "dfed97177496710e3c356c61da722500b2b7fb8b25dc39ae2fa5ef1fb9ec1c70";

async function scanUrlWithVirusTotal(url) {
  const urlId = base64.encode(url).replace(/=/g, "");

  const headers = {
    "x-apikey": API_KEY,
  };

  try {
    const response = await axios.get(
      `https://www.virustotal.com/api/v3/urls/${urlId}`,
      { headers }
    );
    if (response.status === 200) {
      const maliciousCount =
        response.data.data.attributes.last_analysis_stats.malicious || 0;
      return maliciousCount;
    } else {
      return null;
    }
  } catch (error) {
    console.error("Error scanning URL:", error);
    return null;
  }
}

const extractUrls = (message) => {
  const urlRegex = /(https?:\/\/[^\s]+)/g;
  return message.match(urlRegex) || [];
};

app.post("/api/predict", async (req, res) => {
  const { message } = req.body;

  const urls = extractUrls(message);
  let totalMaliciousCount = 0;

  if (urls.length > 0) {
    for (const url of urls) {
      const maliciousCount = await scanUrlWithVirusTotal(url);
      if (maliciousCount !== null) {
        totalMaliciousCount += maliciousCount;
        if (maliciousCount > 0) {
          return res.json({
            result: "Phishing or Malware Detected",
            details: "Malicious URL detected",
            maliciousCount: totalMaliciousCount,
          });
        }
      } else {
        return res.json({
          result: "Error occurred while checking URL",
          maliciousCount: totalMaliciousCount,
        });
      }
    }
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
    res.json({
      result: predictionOutput.toUpperCase(),
      maliciousCount: totalMaliciousCount,
    });
  });
});

app.listen(5000, () => {
  console.log("Server running on port 5000");
});
