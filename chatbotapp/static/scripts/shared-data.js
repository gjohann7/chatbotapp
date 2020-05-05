/**
 * This IIFE as object is responsible for the consistency of the shared data
 * between the app's scripts and its worker.
 * - Poscondition: Both app script and worker have the access to this information.
 * @returns {Object} An object with shared information details.
 */
const SharedData = (function () {
  // States of the chat.
  const ON = 1;
  const SILENCE = 2;
  const OFF = 3;
  const BACK = 4;

  /**
   * This function generate the chatbot question request URI.
   * - Poscondition: The request URI was generated.
   * @param {String} ending An event triggered in the window.
   */
  const generateURL = (ending) =>
    "http://localhost:8000/conversation/question=" + encodeURIComponent(ending);

  /**
   * This IIFE as object is responsible for the internal commands to the server, which
   * won't reach the bot.
   * - Poscondition: The internal commands are available for use.
   * @returns {Object} An object with startWebWorker and checkLocalStorageKey functions.
   */
  const InternalCommands = (function () {
    const commands = Object.create(null);
    const base = "INTERNAL COMMAND ";
    commands.silence = { command: base + "SILENCE", message: "Então kk" };
    commands.off = {
      command: base + "CONNECTION ISSUE",
      message: "Em, eu já volto",
    };
    commands.back = {
      command: base + "RECOVERED CONNECTION",
      message: "Voltei kk",
    };
    commands.test = {
      command: "test connection",
    };
    commands.successMessage = "internal command successful";
    return commands;
  })();

  return { InternalCommands, generateURL, ON, SILENCE, OFF, BACK };
})();
