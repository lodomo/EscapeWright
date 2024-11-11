// camelCase: Use for variables, functions, and method names.
// PascalCase: Use for class names, interface names, type aliases, and enum names.
// UPPER_CASE: Use for constants.
import { setInnerText } from "./funcs.ts";
import { setInnerHTML } from "./funcs.ts";
import { fetchStringFromApi } from "./funcs.ts";
import { updateTimer } from "./funcs.ts";
import { initializeLoadFromAPI } from "./funcs.ts";
import { unblockPage } from "./funcs.ts";
//import { Globals } from "./dicts.ts";
//import { RoomStatus } from "./dicts.ts";
//import { ApiRoutes } from "./dicts.ts";

// Set all static elements on the page
setInnerText("title", await fetchStringFromApi("control_panel_title"));

setInnerHTML("#app", `
  <div id="page_blocker"></div>
  <div id="app_container"></div>
`);

setInnerHTML("#page_blocker", `Load This Dynamically.`);

setInnerHTML("#app_container", `
    <div id="header"></div>
    <div id="content_container"></div>
`);

setInnerHTML("#header", `
  <div id="page_title"></div>
  <div id="timer" class="status-or-timer"></div>
  <div id="game-control"></div>
  <div id="logo"></div>
`);

setInnerHTML("#page_title", `
  <h1></h1>
  <div class="kana">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 130 13" fill="#463087" xmlns:v="https://vecta.io/nano"><path d="M1.44 4.3C.59 4.25.1 3.72.01 2.98s.63-1.35 1.46-1.3l6.33.04c.9.04 1.27.92 1.25 1.39l-.1 7.7c-.01.58-.66 1.14-1.62 1.13H1.64c-.79-.03-1.61-.49-1.59-1.32 0-.83.67-1.32 1.76-1.33l4.66.09.1-5.06c-.78-.01-4.49.02-5.13-.02zm13.02-1.31c.18-.59 1.01-1.11 2-.58.97.55 2.37 1.44 2.88 1.85.51.42.45 1.02.19 1.51-.25.49-1.07.77-1.82.4s-2.04-1.04-2.67-1.51c-.68-.51-.77-1.08-.58-1.67zm10.06-.1c.55.27.86.92.66 1.76-.21.83-1.12 3.63-3.35 5.49-2.16 1.78-3.81 2.11-5.13 2.03-.97-.06-1.58-.58-1.53-1.35.04-.68.48-1.16 1.55-1.29s2.8-.65 4.13-2.57c.86-1.25 1.52-2.58 1.85-3.26.41-.87 1.28-1.08 1.82-.81zm14.1 4.36c-.19.49-.83 1.05-1.55.89l-3-.49-.01 3.5c-.06.77-.63 1.2-1.34 1.3-.73.1-1.3-.52-1.34-1.33-.07-1.19-.03-8.51.03-9.39.04-.73.55-1.19 1.33-1.19.76 0 1.28.58 1.34 1.25.01.21-.05 2.21-.04 3.08 1.01.28 3.59.64 4.02.88.62.3.78.93.56 1.5zm7.75-5.68l6.38.06c1.21.04 1.97.58 2.03 2.03l.04 6.48c-.03 1.14-.92 1.65-2.29 1.65-1.36 0-5.35-.04-6.42 0-1.09.03-1.79-.77-1.85-1.93l-.04-6.23c.09-1.4.97-2.03 2.15-2.06zm.88 7.74l4.65.06c.28 0 .63-.03.63-.61l-.1-3.74c0-.34.03-.73-.33-.76-.34-.03-4.29-.09-4.77-.09s-.7.19-.7.88l.03 3.59c.05.53.19.67.59.67zm22.39-2.94c.01.3-.07.55-.24.74-.37.4-1.09.5-1.73.53-.43.03-2.32.03-3.23.03-2.35 0-3.44-.03-3.92-.04-1.25-.06-1.45-.7-1.45-1.08 0-.79.6-1.33 1.51-1.39l2.03-.01 3.92.03 1.28.01c.91 0 1.78.13 1.83 1.18zm6.79-5.23c.69.03 1.42.27 1.52 1.59.13 1.63-.03 2.92-.25 4.79-.31 2.49-.66 3.08-1.37 4.03-.46.61-1.15.85-1.67.68-.51-.15-.94-.52-.8-1.36.13-.84.86-1.57 1.21-3.47.27-1.54.19-3.96.13-4.74-.11-1.09.63-1.54 1.23-1.52zm4.17-.12c.42.03 1.22.52 1.21 1.35l-.06 4.61-.01 2.18c.24.04 1.62-.62 1.98-.7.54-.1 1.33.19 1.49.67.18.47.19 1.29-.94 1.9-1.15.61-2.64 1.1-3.28 1.23-1.03.22-1.56-.34-1.71-.82-.16-.52-.09-1.59-.09-2.61l.03-6.49c.08-1.19.95-1.34 1.38-1.32zm11.44 1.81c.76.15 1.16.83 1.06 1.79-.12.95-.46 2.11-1.18 3.78-.73 1.68-1.45 2.79-2.3 3.22-.58.31-1.37.16-1.59-.06-.33-.31-.66-.96.04-2.03 1.04-1.62 2.01-3.96 2.29-5.1.25-.96.86-1.75 1.68-1.6zm4.16-.27c.64-.16 1.45.12 1.8 1.31.78 2.64 2.21 5.38 2.56 6.29.36.92.09 1.45-.43 1.74-.54.28-1.65.21-2.18-.79-.79-1.44-2.09-4.21-2.58-6.6-.21-1.09.19-1.77.83-1.95zm4.86-.25c-.06.53-.88 1.36-1.95 1.19-1.01-.18-1.54-1.01-1.48-2.02.06-.99 1.48-1.94 2.49-1.23 1 .71 1 1.52.94 2.06zm-1.28-.58c-.07-.36-.36-.43-.64-.28-.28.13-.31.64.06.71.35.06.64-.07.58-.43zm14.3 9.1c-.16.22-.98.64-1.8-.06a6.94 6.94 0 0 0-1.98-1.22l-.06 2.43c-.07.62-.55.98-1.21 1.01-.66.01-1.18-.37-1.27-1.08-.04-.3-.03-1.07 0-1.88l-.57.33c-1.13.61-1.98.85-2.67.52-.67-.31-.83-1.3-.1-1.88.73-.59 1.97-1.02 3.23-1.88 1.25-.86 2.76-2.03 2.67-2.22l-4.56.01c-.94-.01-1.53-.42-1.58-1.17-.03-.76.69-1.29 1.73-1.3l1.76-.03.04-.92c.04-.49.64-.98 1.31-.93.66.04 1.06.53 1.04 1.04l-.01.86c1.12.03 2.01.04 2.49.24.52.22.94.92.76 1.63s-.51 1.39-1.51 2.54c-.18.21-.42.43-.69.67.55.21 1.53.64 2.44 1.39 1.16.93.71 1.7.54 1.9zm7.05-9.69c.69.03 1.42.27 1.52 1.59.13 1.63-.03 2.92-.25 4.79-.31 2.49-.66 3.08-1.37 4.03-.46.61-1.15.85-1.67.68-.51-.15-.94-.52-.8-1.36.13-.84.86-1.57 1.21-3.47.27-1.54.19-3.96.13-4.74-.11-1.09.64-1.54 1.23-1.52zm4.18-.12c.42.03 1.22.52 1.21 1.35l-.06 4.61-.01 2.18c.24.04 1.62-.62 1.98-.7.54-.1 1.33.19 1.49.67.18.47.19 1.29-.94 1.9-1.15.61-2.64 1.1-3.28 1.23-1.03.22-1.56-.34-1.71-.82-.16-.52-.09-1.59-.09-2.61l.03-6.49c.08-1.19.94-1.34 1.38-1.32z"/></svg>
  </div>
  <div class="line purple"></div> 
  <div class="line red"></div>
  <div class="line orange"></div>
`);

setInnerText("#page_title h1", await fetchStringFromApi("room_name"));
setInnerText("#timer", "Load this Dynamically");
setInnerHTML("#game-control", `Load this Dynamically`);
setInnerHTML("#logo", 'Load this Dynamically');

setInnerHTML("#content_container", `
  <div id="content"></div>
  <div id="navigation"></div>
`);


setInnerHTML("#content", `
  <div id="status_panel"></div>
  <div id="script_panel"></div>
  <div id="override_panel"></div>
  <div id="reset_panel"></div>
  <div id="stop_panel"></div>
`);

setInnerHTML("#status_panel", `
  WORDS
`);

setInnerHTML("#script_panel", `
  WORDS
`);

setInnerHTML("#override_panel", `
  WORDS
`);

setInnerHTML("#reset_panel", `
  WORDS
`);

setInnerHTML("#stop_panel", `
  WORDS
`);

setInnerHTML("#navigation", `
  <button id="nav_control" class="nav-button nav-act">Status</button>
  <button id="nav_script" class="nav-button nav-pas">Script</button>
  <button id="nav_override" class="nav-button nav-pas">Overrides</button>
  <button id="nav_reset" class="nav-reset">Reset</button>
  <button id="nav_stop" class="nav-stop">Stop</button>
`);




initializeLoadFromAPI();
setInterval(updateTimer, 1000);


await new Promise((resolve) => setTimeout(resolve, 250));
unblockPage();
