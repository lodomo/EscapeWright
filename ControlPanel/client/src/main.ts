// camelCase: Use for variables, functions, and method names.
// PascalCase: Use for class names, interface names, type aliases, and enum names.
// UPPER_CASE: Use for constants.
import { setInnerText } from "./funcs.ts";
import { setInnerHTML } from "./funcs.ts";
import { fetchStringFromApi } from "./funcs.ts";
import { updateTimer } from "./funcs.ts";
import { initializeLoadFromAPI } from "./funcs.ts";
import { unblockPage } from "./funcs.ts";
import { setActivePanel } from "./funcs.ts";
import { fullscreenButton } from "./funcs.ts";
import { sendGameControl } from "./funcs.ts";
import { sendPostToAPI } from "./funcs.ts";
//import { Globals } from "./dicts.ts";
//import { RoomStatus } from "./dicts.ts";
//import { ApiRoutes } from "./dicts.ts";
import { kana_ctrl_panel } from "./svg_raw.ts";

// Set all static elements on the page
setInnerText("title", await fetchStringFromApi("control_panel_title"));

setInnerHTML(
  "#app",
  `
  <div id="page_blocker"></div>
  <div id="app_container"></div>
  `,
);

setInnerHTML("#page_blocker", `Load This Dynamically.`);

setInnerHTML(
  "#app_container",
  `
    <div id="header"></div>
    <div id="content_container"></div>
  `,
);

setInnerHTML(
  "#header",
  `
  <div id="page_title"></div>
  <div id="spacer"></div>
  <div id="timer" class="status-or-timer"></div>
  <button id="game-control" class="toggle-btn"></button>
  <div id="spacer"></div>
  <div id="logo"></div>
  `,
);

setInnerHTML(
  "#page_title",
  `
  <h1></h1>
  <div id="kana" class="kana"></div>
  <div class="line purple"></div> 
  <div class="line red"></div>
  <div class="line orange"></div>
  `,
);

setInnerHTML("#kana", kana_ctrl_panel);
setInnerText("#page_title h1", await fetchStringFromApi("room_name"));
setInnerText("#timer", "Load this Dynamically");
setInnerText("#game-control", "Load this Dynamically");

setInnerHTML(
  "#logo",
  `
  <div id="fullscreenBtn" class="logo">
    <img src="/images/logo.png" alt="Logo" />
  </div>
  `,
);

fullscreenButton();

setInnerHTML(
  "#content_container",
  `
  <div id="content"></div>
  <div id="navigation"></div>
`,
);

setInnerHTML(
  "#content",
  `
  <div id="status_panel" class="panel active" ></div>
  <div id="script_panel" class="panel inactive" >
    <div id="script_content"></div>
  </div>
  <div id="override_panel" class="panel inactive" ></div>
  <div id="reset_panel" class="panel inactive" ></div>
  <div id="stop_panel" class="panel inactive" ></div>
`,
);

setInnerHTML(
  "#status_panel",
  `
  WORDS
  `,
);

setInnerHTML("#script_content", await fetchStringFromApi("script"));

setInnerHTML(
  "#override_panel",
  `
  WORDS
  `,
);

// This is ugly asf, I want to change this code but it works right now.
setInnerHTML(
  "#reset_panel",
  `
  <div class="message-container">
    <div class="symbol">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 50 50" style="enable-background:new 0 0 50 50" xml:space="preserve"><path style="fill:#639fab" d="M21.13 19.99h24.49l-2.25-1.12 2.23-4.86-5.31-.69.53-5.32-5.24 1.07-1.23-5.21-4.61 2.72-2.86-4.53-3.48 4.07-4.16-3.36-1.97 4.98-5.04-1.82-.24 5.34-5.35-.08 1.5 5.13-5.09 1.66 3.09 4.37-4.28 3.22 4.34 3.13-2.99 4.43 5.11 1.55-1.39 5.17 5.34-.2.36 5.34 4.99-1.92 2.08 4.93 1.43-1.2z"/><path style="fill:#222" d="m19.17 43.89-.94-2.24-4.59 1.76-.33-4.91-4.92.18 1.28-4.75-4.71-1.43 2.76-4.08-3.99-2.88 3.93-2.96-2.84-4.02 4.68-1.53-1.38-4.72 4.92.08.23-4.92 4.63 1.67 1.81-4.57 3.84 3.08 3.2-3.74 2.62 4.16 4.25-2.49 1.13 4.79 4.82-.99-.48 4.9 4.88.63-1.43 3.12h2.44l1-2.2 1.25-2.72-2.98-.39-2.75-.36.27-2.76.3-2.99-2.94.6-2.72.56-.64-2.7-.69-2.92-2.59 1.52-2.39 1.41-1.48-2.35-1.6-2.54-1.95 2.28-1.81 2.11-2.16-1.74L18.76.96l-1.11 2.79-1.02 2.58-2.61-.94-2.82-1.02-.14 3-.13 2.77-2.78-.04-3-.05.85 2.88.77 2.66-2.64.86-2.85.93 1.73 2.46 1.6 2.26-2.21 1.67L0 25.58l2.43 1.75 2.25 1.63-1.55 2.3-1.68 2.48 2.87.88 2.66.8-.73 2.68-.78 2.9 3-.11 2.77-.1.19 2.77.2 2.99 2.8-1.07 2.59-1 1.08 2.56 1.07 2.56z"/></svg>
    </div>
    <div class="symbol">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 50 50"><path d="M40.28 24.98c-.18-.36-.48-.66-.84-.78 0-.06 0-.12-.06-.18-.24-.54-.78-.84-1.38-.84h-.6c-.12-1.02-.42-1.98-.78-2.94-.6-1.38-1.44-2.64-2.46-3.66-.18-.18-.3-.3-.48-.42-.12-.18-.3-.3-.42-.48-1.08-1.08-2.28-1.92-3.66-2.46-1.44-.6-2.94-.9-4.5-.9-2.34-.06-4.5.6-6.36 1.8-.36.24-.6.6-.66 1.02s0 .84.24 1.14l1.62 2.22c.18.24.36.36.6.48l.3.42c.3.36.72.6 1.2.6.3 0 .54-.06.78-.24.9-.54 1.98-.84 3.06-.84 1.32 0 2.58.48 3.66 1.26.66.84 1.14 1.86 1.26 3h-1.14c-.6 0-1.08.3-1.38.84-.24.54-.18 1.14.18 1.62l1.92 2.4 2.28 2.82c.12.18.3.3.54.42l.42.48c.3.36.72.54 1.2.54s.9-.18 1.2-.54l2.28-2.82 1.92-2.4c.3-.42.36-1.02.06-1.56zm-9.54 5.28c-.18-.24-.36-.36-.6-.48l-.3-.42c-.3-.36-.72-.6-1.2-.6-.24 0-.54.06-.72.18-.9.48-1.86.78-2.88.78-1.38 0-2.64-.48-3.66-1.26-.66-.84-1.08-1.86-1.26-2.94h1.14c.6 0 1.08-.3 1.38-.84s.18-1.14-.18-1.62l-1.92-2.4-2.28-2.88c-.12-.18-.3-.3-.54-.42l-.42-.48c-.3-.36-.72-.54-1.2-.54s-.9.18-1.2.54l-2.28 2.82-1.92 2.4c-.3.42-.36 1.02-.06 1.56.18.36.48.66.84.78 0 .06 0 .12.06.18.24.54.78.84 1.38.84h.6c.12 1.02.42 1.98.78 2.94.6 1.38 1.44 2.64 2.46 3.66.18.18.3.3.48.42.12.18.3.3.42.48 1.08 1.08 2.28 1.92 3.66 2.46 1.44.6 2.94.9 4.5.9 2.1 0 4.2-.6 6-1.68.36-.24.6-.6.72-1.02.06-.42 0-.84-.24-1.2l-1.56-2.16z" style="fill:#222"/><path d="M24.99 13.1c5.94 0 10.8 4.86 10.8 10.8v.18h2.28c.6 0 .9.66.54 1.14l-1.92 2.4-2.28 2.82c-.12.18-.36.24-.54.24s-.42-.06-.54-.24l-2.28-2.82-1.92-2.4c-.36-.48-.06-1.14.54-1.14h1.92c.06-3.72-2.94-6.78-6.66-6.78-1.26 0-2.46.36-3.48.96 0 0-.18.06-.3.06a.63.63 0 0 1-.54-.3l-1.62-2.22c-.24-.3-.12-.78.18-.96 1.68-1.14 3.66-1.74 5.82-1.74m-8.82 4.02c.18 0 .42.06.54.24l2.28 2.82 1.92 2.4c.36.48.06 1.14-.54 1.14h-1.92v.18c0 3.66 3 6.66 6.66 6.66 1.2 0 2.28-.3 3.3-.84.12-.06.24-.12.36-.12.24 0 .42.12.54.3l1.62 2.28c.24.3.12.78-.18 1.02-1.62 1.02-3.54 1.56-5.58 1.56-5.94 0-10.8-4.86-10.8-10.8v-.18h-2.4c-.6 0-.9-.66-.54-1.14l1.92-2.4 2.28-2.82c.12-.24.3-.3.54-.3" style="fill:#639fab"/></svg>
    </div>
    <div class="symbol">
      <div class="exclamation jiggle">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 50 50"><path d="M31 18.89c0-.06-.06-.11-.11-.17-.11-.28-.22-.56-.33-.78-.39-.61-.89-1.22-1.5-1.67-1.11-.78-2.61-1.28-4.11-1.28s-2.89.5-4.06 1.33c-.67.5-1.17 1.06-1.5 1.72-.39.72-.61 1.56-.61 2.39v.89h.44v.94h3.06l.11 3.67.06.83h.39v.39l-.06.06c-.61.61-.94 1.39-.94 2.22 0 .67.22 1.28.56 1.78.17.5.39.94.78 1.33.61.61 1.39.94 2.22.94a3.17 3.17 0 0 0 3.17-3.17c0-.67-.22-1.22-.56-1.78-.11-.33-.28-.67-.44-1v-2.06c1-.22 1.78-.61 2.39-1.06.5-.39.89-.83 1.17-1.39s.44-1.22.44-1.94-.17-1.5-.56-2.22z" style="fill:#222"/><path d="M24.89 15.94c2.44 0 5.39 1.44 5.39 4.39 0 2.39-1.94 3.33-4 3.67v1.94h-3l-.22-4c1.94 0 3.11-.33 3.11-1.39 0-.72-.5-1.06-1.28-1.06-.83 0-1.11.61-1.11 1.06h-4.17c0-3.11 2.94-4.61 5.28-4.61M25 27.16c1.28 0 2.28 1 2.28 2.28s-1.06 2.28-2.28 2.28-2.28-1-2.28-2.28 1-2.28 2.28-2.28" style="fill:#f9f4e9"/></svg>
      </div>
    </div>
    <div class="message-text">
      ARE YOU SURE<br>YOU WANT TO RESET?
    </div>
    <button id="resetButton" class="message-btn yes">Yes</button>
    <button data-target="status_panel" class="message-btn no">No</button>
  </div>
`,
);

// This is ugly asf, I want to change this code but it works right now.
setInnerHTML(
  "#stop_panel",
  `
  <div class="message-container bg-red">
    <div class="symbol">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 50 50" style="enable-background:new 0 0 50 50" xml:space="preserve"><path style="fill:#639fab" d="M21.13 19.99h24.49l-2.25-1.12 2.23-4.86-5.31-.69.53-5.32-5.24 1.07-1.23-5.21-4.61 2.72-2.86-4.53-3.48 4.07-4.16-3.36-1.97 4.98-5.04-1.82-.24 5.34-5.35-.08 1.5 5.13-5.09 1.66 3.09 4.37-4.28 3.22 4.34 3.13-2.99 4.43 5.11 1.55-1.39 5.17 5.34-.2.36 5.34 4.99-1.92 2.08 4.93 1.43-1.2z"/><path style="fill:#222" d="m19.17 43.89-.94-2.24-4.59 1.76-.33-4.91-4.92.18 1.28-4.75-4.71-1.43 2.76-4.08-3.99-2.88 3.93-2.96-2.84-4.02 4.68-1.53-1.38-4.72 4.92.08.23-4.92 4.63 1.67 1.81-4.57 3.84 3.08 3.2-3.74 2.62 4.16 4.25-2.49 1.13 4.79 4.82-.99-.48 4.9 4.88.63-1.43 3.12h2.44l1-2.2 1.25-2.72-2.98-.39-2.75-.36.27-2.76.3-2.99-2.94.6-2.72.56-.64-2.7-.69-2.92-2.59 1.52-2.39 1.41-1.48-2.35-1.6-2.54-1.95 2.28-1.81 2.11-2.16-1.74L18.76.96l-1.11 2.79-1.02 2.58-2.61-.94-2.82-1.02-.14 3-.13 2.77-2.78-.04-3-.05.85 2.88.77 2.66-2.64.86-2.85.93 1.73 2.46 1.6 2.26-2.21 1.67L0 25.58l2.43 1.75 2.25 1.63-1.55 2.3-1.68 2.48 2.87.88 2.66.8-.73 2.68-.78 2.9 3-.11 2.77-.1.19 2.77.2 2.99 2.8-1.07 2.59-1 1.08 2.56 1.07 2.56z"/></svg>
    </div>
    <div class="symbol">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 50 50"><path d="m38.06 20.08-1.09-1.09c-.16-.21-.31-.47-.52-.63l-5.31-5.37c-.57-.57-1.35-.89-2.19-.89h-7.56c-.83 0-1.62.31-2.19.89l-5.31 5.31c-.63.57-.94 1.35-.94 2.19v7.5c0 .83.31 1.62.94 2.19l1.09 1.09c.16.21.31.47.52.63l5.31 5.31c.57.57 1.35.89 2.19.89h7.56c.83 0 1.62-.31 2.19-.89l5.31-5.31c.57-.57.94-1.35.94-2.19v-7.45c0-.83-.31-1.62-.94-2.19z" style="fill:#222"/><path d="M28.94 13.41c.47 0 .94.21 1.25.52l5.31 5.31c.31.31.52.78.52 1.25v7.5c0 .47-.21.94-.52 1.25l-5.31 5.31c-.31.31-.78.52-1.25.52h-7.56c-.47 0-.94-.21-1.25-.52l-5.31-5.31c-.31-.31-.52-.78-.52-1.25v-7.5c0-.47.21-.94.52-1.25l5.31-5.31c.31-.31.78-.52 1.25-.52h7.56" style="fill:#dd3353"/></svg>
    </div>

    <div class="symbol">
      <div class="exclamation jiggle">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 50 50"><path d="M31 18.89c0-.06-.06-.11-.11-.17-.11-.28-.22-.56-.33-.78-.39-.61-.89-1.22-1.5-1.67-1.11-.78-2.61-1.28-4.11-1.28s-2.89.5-4.06 1.33c-.67.5-1.17 1.06-1.5 1.72-.39.72-.61 1.56-.61 2.39v.89h.44v.94h3.06l.11 3.67.06.83h.39v.39l-.06.06c-.61.61-.94 1.39-.94 2.22 0 .67.22 1.28.56 1.78.17.5.39.94.78 1.33.61.61 1.39.94 2.22.94a3.17 3.17 0 0 0 3.17-3.17c0-.67-.22-1.22-.56-1.78-.11-.33-.28-.67-.44-1v-2.06c1-.22 1.78-.61 2.39-1.06.5-.39.89-.83 1.17-1.39s.44-1.22.44-1.94-.17-1.5-.56-2.22z" style="fill:#222"/><path d="M24.89 15.94c2.44 0 5.39 1.44 5.39 4.39 0 2.39-1.94 3.33-4 3.67v1.94h-3l-.22-4c1.94 0 3.11-.33 3.11-1.39 0-.72-.5-1.06-1.28-1.06-.83 0-1.11.61-1.11 1.06h-4.17c0-3.11 2.94-4.61 5.28-4.61M25 27.16c1.28 0 2.28 1 2.28 2.28s-1.06 2.28-2.28 2.28-2.28-1-2.28-2.28 1-2.28 2.28-2.28" style="fill:#f9f4e9"/></svg>
      </div>
    </div>
    <div class="message-text">
      ARE YOU SURE<br>YOU WANT TO STOP?
    </div>
    <button id="stopButton" class="message-btn yes">Yes</button>
    <button data-target="status_panel" class="message-btn no">No</button>
  </div>
`,
);

setInnerHTML(
  "#navigation",
  `
  <button data-target="status_panel" id="nav_status" class="nav-btn nav-act">Status</button>
  <button data-target="script_panel" id="nav_script" class="nav-btn nav-pas">Script</button>
  <button data-target="override_panel" id="nav_override" class="nav-btn nav-pas">Overrides</button>
  <button data-target="reset_panel" id="nav_reset" class="nav-btn nav-pas">Reset</button>
  <button data-target="stop_panel" id="nav_stop" class="nav-btn nav-pas">Stop</button>
`,
);

setInnerHTML("#nav_status", `<img src="/images/status.png" alt="Status" />`);
setInnerHTML("#nav_script", `<img src="/images/script.png" alt="Script" />`);
setInnerHTML(
  "#nav_override",
  `<img src="/images/override.png" alt="Overrides" />`,
);
setInnerHTML("#nav_reset", `<img src="/images/reset.png" alt="Reset" />`);
setInnerHTML("#nav_stop", `<img src="/images/stop.png" alt="Stop" />`);

initializeLoadFromAPI();
setInterval(updateTimer, 1000);

const NAV_BUTTONS: NodeListOf<HTMLButtonElement> =
  document.querySelectorAll(".nav-btn");
const NO_BUTTONS: NodeListOf<HTMLButtonElement> =
  document.querySelectorAll(".message-btn.no");
const NAV_AND_NO_BUTTONS: NodeListOf<HTMLButtonElement> =
  document.querySelectorAll(".nav-btn, .message-btn.no");
const NAV_PANELS: NodeListOf<HTMLDivElement> =
  document.querySelectorAll(".panel");
const RESET_BUTTON: HTMLButtonElement = document.getElementById(
  "resetButton",
) as HTMLButtonElement;
const STOP_BUTTON: HTMLButtonElement = document.getElementById(
  "stopButton",
) as HTMLButtonElement;

function navButtonHandler(event: MouseEvent) {
  setActivePanel(event, NAV_AND_NO_BUTTONS, NAV_PANELS);
}

// Add click event listeners to each button
NAV_BUTTONS.forEach((button) => {
  button.addEventListener("click", navButtonHandler);
});

// Seperated this incase I switch the logic later
NO_BUTTONS.forEach((button) => {
  button.addEventListener("click", navButtonHandler);
});

const GAME_CONTROL_BUTTON: HTMLButtonElement = document.getElementById(
  "game-control",
) as HTMLButtonElement;
GAME_CONTROL_BUTTON.addEventListener("click", sendGameControl);

function resetButtonHandler() {
  sendPostToAPI("reset");
}

function stopButtonHandler() {
  sendPostToAPI("stop");
}

RESET_BUTTON.addEventListener("click", resetButtonHandler);
STOP_BUTTON.addEventListener("click", stopButtonHandler);

await new Promise((resolve) => setTimeout(resolve, 250));
console.log("Unblocking page automatically.. This needs to be turned off in future versions.");
unblockPage();
