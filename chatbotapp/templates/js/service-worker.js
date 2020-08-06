const testConnection = () => {
  const xhr = new XMLHttpRequest() || new ActiveXObject("Microsoft.XMLHTTP");
  xhr.onload = () => {
    postMessage("back");
  };
  xhr.onerror = () => {
    setTimeout(testConnection, 2000);
  };
  // http://127.0.0.1:8000
  xhr.open(
    "GET",
    `https://chatbot-patient.herokuapp.com/conversation/question=${encodeURIComponent(
      "test connection"
    )}`
  );
  xhr.send();
};

/**
 * This function handles the script messages.
 * @param {Event} event An event received from the script.
 */
onmessage = (event) => {
  if (event.data === "off") {
    testConnection();
  }
};
