import React, { useState, useEffect } from "react";

export default function BotMessage({ message }) {
  const [isLoading, setLoading] = useState(false);
  // const [message, setMessage] = useState("");

  // useEffect(() => {
  //   async function loadMessage() {
  //     const msg = await fetchMessage();
  //     setLoading(false);
  //     setMessage(msg);
  //   }
  //   loadMessage();
  // }, [fetchMessage]);

  return (
    <div className="message-container">
      <div className="bot-message">{isLoading ? "..." : message}</div>
    </div>
  );
}
