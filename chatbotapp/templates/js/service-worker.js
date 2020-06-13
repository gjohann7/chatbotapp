importScripts(origin + "/static/scripts/shared-data.js");

const { InternalCommands, generateURL, ON, SILENCE, OFF, BACK } = SharedData;

/**
 * This IIFE as object is responsible for the worker job.
 * @returns {Object} An object with the update state method.
 */
const Task = (function () {
  let count = 0;
  let isBack = false;
  let timeoutId = [];
  let selfState = ON;
  const TIMEOUT = 120000;

  /**
   * This function clear all the active timeouts.
   */
  const clear = () => {
    if (timeoutId.length) {
      clearTimeout(
        timeoutId.reduce((id, next) => {
          if (next) {
            clearTimeout(id);
          }
          return next;
        })
      );
      timeoutId = [];
    }
  };

  /**
   * This function handles the success response of the sent request.
   */
  const onLoad = () => {
    if (isBack) {
      clear();
      postMessage({ state: BACK });
      selfState = BACK;
      isBack = false;
    } else {
      if (count < 2 && selfState !== BACK) {
        postMessage({ state: SILENCE });
        selfState = SILENCE;
        count++;
      }
    }
  };

  /**
   * This function handles the failed response of the sent request.
   */
  const onError = () => {
    if (!isBack) {
      postMessage({ state: OFF });
      selfState = OFF;
      isBack = true;
    }
  };

  /**
   * This function make the request to the server.
   * @param {String} command A command defined in the shared-data.js.
   */
  const run = (command) => {
    const xhr = new XMLHttpRequest() || new ActiveXObject("Microsoft.XMLHTTP");
    xhr.onload = onLoad;
    xhr.onerror = onError;
    xhr.open("GET", generateURL(command));
    xhr.send();
  };

  /**
   * This function updates the worker state and can be used outside of its scope.
   * @param {Number} state A state defined in the shared-data.js.
   */
  function update(message) {
    let command = InternalCommands.silence.command;
    if (message.state !== SILENCE) {
      count = 0;
    }
    if (message.state === OFF) {
      command = InternalCommands.test.command;
      selfState = OFF;
    } else {
      selfState = SILENCE;
    }
    if (message.state !== ON && !(message.state === SILENCE && count > 1)) {
      run(command);
    }
    clear();
    if (count < 2) {
      timeoutId.push(setTimeout(selfUpdate, TIMEOUT + message.addTime));
    }
  }

  /**
   * This function updates the worker state and can be used only inside its scope.
   * @param {Number} state A state defined in the shared-data.js.
   */
  const selfUpdate = () => {
    update(selfState);
  };

  return { update };
})();

/**
 * This function handles the script messages.
 * @param {Event} event An event received from the script.
 */
onmessage = (event) => {
  if (event.data.hasOwnProperty("state")) {
    Task.update(event.data);
  }
};
