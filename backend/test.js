const axios = require('axios');
const base64 = require('base-64');

// Your VirusTotal API key
const API_KEY = 'dfed97177496710e3c356c61da722500b2b7fb8b25dc39ae2fa5ef1fb9ec1c70';

// Function to get URL info from VirusTotal
async function getUrlInfo(url) {
  // Encode URL in base64 as required by VirusTotal API
  const urlId = base64.encode(url).replace(/=/g, '');

  try {
    // Call VirusTotal API
    const response = await axios.get(`https://www.virustotal.com/api/v3/urls/${urlId}`, {
      headers: {
        'x-apikey': API_KEY,
      },
    });

    // Log the response data
    console.log('VirusTotal Response:', response.data.data.attributes.last_analysis_stats);
  } catch (error) {
    console.error('Error:', error.response ? error.response.data : error.message);
  }
}

// Example URL to test
const testUrl = 'playdr2.tw:53/';

// Call the function with a test URL
getUrlInfo(testUrl);
