import React, { useState } from "react";
import axios from "axios";
import { Input, Button, notification, Card, Spin, Typography } from "antd";
import { CheckCircleOutlined, WarningOutlined } from "@ant-design/icons";

const { TextArea } = Input;
const { Text } = Typography;

function App() {
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState("");
  const [maliciousCount, setMaliciousCount] = useState(0);
  const [charCount, setCharCount] = useState(0);

  const handleCheckMessage = async () => {
    if (!message.trim()) {
      notification.error({
        message: "Message cannot be empty",
      });
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post("http://localhost:5000/api/predict", {
        message,
      });
      console.log("response", response);
      setResult(response.data.result);
      setMaliciousCount(response.data.maliciousCount);
      if (response.data.result === "SPAM") {
        notification.error({
          message: "Spam Detected",
          description: "This message is classified as SPAM.",
        });
      } else if (response.data.result === "HAM") {
        notification.success({
          message: "Message Safe",
          description: "This message is classified as HAM.",
        });
      } else {
        notification.error({
          message: response.data.result,
        });
      }
    } catch (error) {
      console.error("Error submitting message:", error);
      setResult("Error occurred");
    } finally {
      setLoading(false);
    }
  };

  const handleClearMessage = () => {
    setMessage("");
    setResult("");
    setMaliciousCount(0);
    setCharCount(0);
  };

  const handleMessageChange = (e) => {
    setMessage(e.target.value);
    setCharCount(e.target.value.length);
  };

  return (
    <div className="App" style={{ padding: "20px" }}>
      <Card
        title="SMS/Email Spam Classifier"
        style={{ width: 400, margin: "100px auto" }}
      >
        <TextArea
          rows={4}
          placeholder="Enter your SMS or Email message"
          value={message}
          onChange={handleMessageChange}
          maxLength={500}
        />
        <Text style={{ display: "block", marginBottom: "10px" }}>
          {charCount} / 500 characters
        </Text>

        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            marginBottom: "20px",
          }}
        >
          <Button
            type="primary"
            loading={loading}
            onClick={handleCheckMessage}
            disabled={loading || !message.trim()}
          >
            {loading ? <Spin /> : "Check for Spam"}
          </Button>

          <Button
            type="default"
            onClick={handleClearMessage}
            disabled={!message.trim()}
          >
            Clear
          </Button>
        </div>

        {result && (
          <Card
            style={{
              marginTop: "20px",
              backgroundColor: maliciousCount > 0 ? "#ffccc7" : "#d9f7be",
            }}
          >
            <div
              style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                flexDirection: "column",
              }}
            >
              {maliciousCount > 0 ? (
                <>
                  <WarningOutlined
                    style={{ fontSize: "40px", color: "#ff4d4f" }}
                  />
                  <Text
                    strong
                    style={{
                      fontSize: "18px",
                      color: "#ff4d4f",
                      marginTop: "10px",
                    }}
                  >
                    ⚠️ This message contains a malicious URL ⚠️
                  </Text>
                  <Text
                    style={{
                      fontSize: "16px",
                      color: "#ff4d4f",
                      marginTop: "5px",
                    }}
                  >
                    Malicious URLs detected: {maliciousCount}
                  </Text>
                </>
              ) : (
                <>
                  {result === "HAM" ? (
                    <>
                      <CheckCircleOutlined
                        style={{ fontSize: "40px", color: "#52c41a" }}
                      />
                      <Text
                        strong
                        style={{
                          fontSize: "18px",
                          color: "#52c41a",
                          marginTop: "10px",
                        }}
                      >
                        ✅ This message is safe
                      </Text>
                    </>
                  ) : (
                    <>
                      <WarningOutlined
                        style={{ fontSize: "40px", color: "#ff4d4f" }}
                      />
                      <Text
                        strong
                        style={{
                          fontSize: "18px",
                          color: "#ff4d4f",
                          marginTop: "10px",
                        }}
                      >
                        ⚠️ This message is usafe ⚠️
                      </Text>
                    </>
                  )}
                </>
              )}
            </div>
          </Card>
        )}
      </Card>
    </div>
  );
}

export default App;
