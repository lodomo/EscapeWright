/*
 * This file contains all the functions that are used in the main.ts
 * file. This is to keep the main.ts file clean and easy to read.
 */
import { ApiRoutes } from "./dicts.ts";
import { RoomStatus } from "./dicts.ts";
import { Globals } from "./dicts.ts";

/*
 * This function sets the inner text of an element.
 * @param element The element to set the inner text of.
 * @param text The text to set the inner text to.
 * @returns void
 *
 * All text sent as a string, not HTML
 *
 * Sister function to setInnerHTML
 */
export function setInnerText(element: string, text: string): void {
  document.querySelector<HTMLDivElement>(element)!.innerText = text;
}

/*
 * This function sets the inner html of an element.
 * @param element The element to set the inner html of.
 * @param html The html to set the inner html to.
 * @returns void
 *
 * All text sent as HTML, not a string
 *
 * Sister function to setInnerText
 */
export function setInnerHTML(element: string, html: string): void {
  document.querySelector<HTMLDivElement>(element)!.innerHTML = html;
}

/*
 *
 */
export async function fetchStringFromApi(
  endpoint: string,
  max_retries: number = 10,
): Promise<string> {
  endpoint = `${ApiRoutes.api}${endpoint}`;
  let response = null;
  while (max_retries > 0) {
    try {
      console.log("Fetching", endpoint);
      response = await fetch(endpoint);
      max_retries = 0;
    } catch (TypeError) {
      console.error("Error fetching", endpoint);
      max_retries--;
      await new Promise((resolve) => setTimeout(resolve, 1000));
      continue;
    }
  }

  let data: string = ``;

  if (response === null) {
    console.error("Failed to fetch", endpoint);
    data = "ERROR";
  } else {
    data = await response.text();
  }

  return data;
};

export async function sendPostToAPI(route: string): Promise<void> {
  await fetch(`${ApiRoutes.api}${route}`, {
    method: "POST",
  });
  return;
}

/*
 * Get Updates from the API
 */
export async function getStatusFromAPI(): Promise<void> {
  Globals.status = await fetchStringFromApi(ApiRoutes.status);
  console.log(Globals.status);
  return;
};

/*
 * Function that requests the current time from the API and updates the timer text.
 * It times out after 10 seconds of errors, this allows for only real errors to be shown
 * and not just skipping a beat in the API.
 *
 * This needs to work much better.
 * First it should check LOADING constantly, maybe every 10 seconds?
 * If ready it should chill until the player presses start
 * If the timer is running it should check every 10 seconds for an update,
 * and simulate updates for the other 10 seconds.
 * If the user presses pause, it should pause the timer and stop checking
 * If the user resumes the timer, it should get a time and then start checking again.
 * If the user stops the timer, it should stop checking and show the timer as stopped.
 * If the user resets the timer, it should restart the loop and be back in LOADING territory.
 *
 * Right now all it does it check every second and update the timer text.
 * The above way will be added in the future if the load on the API is too high.
 */
export async function updateTimer(): Promise<void> {
  let updatedTimerText: string = await fetchStringFromApi("time_remaining");

  if (updatedTimerText === Globals.timer) {
    return;
  } else {
    Globals.timer = updatedTimerText;
    updateGameControl(updatedTimerText);
  }


  // Update the timer element
  const timerElement = document.getElementById("timer");
  if (timerElement === null) {
    throw new Error("Timer element not found");
  } else {
    timerElement.innerText = Globals.timer;

    timerElement.classList.remove(
      "ready",
      "paused",
      "stopped",
      "error",
      "mtquart",
    );

    if (Globals.timer === "READY") {
      timerElement.classList.add("ready");
    } else if (Globals.timer === "ERROR") {
      timerElement.classList.add("error");
    } else if (Globals.timer === "00:00:00") {
      timerElement.classList.add("stopped");
    } else if (Globals.timer === "PAUSED") {
      timerElement.classList.add("paused");
    } else {
      timerElement.classList.add("mtquart");
    }
  }
  return;
};

function updateGameControl(status: string): void {
  const controlButton = document.getElementById("game-control");
  if (controlButton === null) {
    throw new Error("Control Button not found");
  }

  controlButton.classList.remove(
    "ready",
    "pause",
    "resume",
    "disabled",
  );

  switch (status) {
    case "READY":
      controlButton.classList.add("ready");
      controlButton.innerText = "START";
      break;
    case "PAUSED":
      controlButton.classList.add("pause");
      controlButton.innerText = "RESUME";
      break;
    case "STOPPED":
      controlButton.classList.add("disabled");
      controlButton.innerText = "DONE";
      break;
    case "ERROR":
      controlButton.classList.add("disabled");
      controlButton.innerText = "ERROR";
      break;
    case "LOADING":
      controlButton.classList.add("disabled");
      controlButton.innerText = "WAIT";
      break;
    case "00:00:00":
      controlButton.innerText = "DONE";
      break;
    default:
      controlButton.innerText = "PAUSE";
      controlButton.classList.add("resume");
  }
  return;
}

export function sendGameControl(): void {
  const controlButton = document.getElementById("game-control");
  if (controlButton === null) {
    throw new Error("Control Button not found");
  }

  console.log("Control Button Clicked");

  if (controlButton.classList.contains("ready")) {
    console.log("TODO, THIS NEEDS TO BRING UP A MODAL TO CONFIRM");
    fetch(`${ApiRoutes.api}toggle`, {
      method: "POST",
    });
  }

  if (controlButton.classList.contains("pause")) {
    fetch(`${ApiRoutes.api}toggle`, {
      method: "POST",
    });
  }

  if (controlButton.classList.contains("resume")) {
    fetch(`${ApiRoutes.api}toggle`, {
      method: "POST",
    });
  }
}

/*
 * THIS IS JUST A TEST FOR NOW, THIS NEEDS TO BE CHANGED TO DO LOTS OF BLOCKING
 * THIS IS JUST PROOF OF CONCEPT
 *
 * FINAL VERSION WILL NEED TO:
 * BLOCK IF THE ROOM IS RUNNING
 * BLOCK IF THE ROOM IS STOPPED
 * BLOCK IF THE ROOM IS LOADING
 * Only will go away if the user clicks a close button OR the page loads.
 */
export async function initializeLoadFromAPI(): Promise<void> {
  Globals.status = await fetchStringFromApi(ApiRoutes.status);
  console.log(Globals.status);

  // Check if It's Loading
  while (Globals.status === RoomStatus.loading) {
    await new Promise((resolve) => setTimeout(resolve, 1000));
    Globals.status = await fetchStringFromApi(ApiRoutes.status);
    console.log(Globals.status);
  }

  // Then Check if it's Running.
  // Then Check if it's Stopped.
  // Then Load the rest of the page.

  updateTimer();
  console.log("API Loaded");
};

export function unblockPage(): void {
  let page_block_element = document.querySelector<HTMLDivElement>("#page_blocker")!;
  page_block_element.classList.add("hide");
}

/*
 * Handle Button Click and set the active panel
 * Hide all other panels
 */
export function setActivePanel(event: MouseEvent, buttons: NodeListOf<HTMLButtonElement>, divs: NodeListOf<HTMLDivElement>): void {
    // Don't let the nav button be pressed twice
    if ((event.target as HTMLElement).classList.contains('nav-act')) {
        return;
    };

    // Find the target panel
    const targetPanelID = (event.target as HTMLElement).getAttribute('data-target');
    const targetPanel = document.querySelector(`#${targetPanelID}`);

    // Set buttons to be active or inactive in the nav bar
    // This allows buttons NOT in the nav bar to activate the navigation.
    // (Like saying no in a popup)
    buttons.forEach(button => {
      if (button.getAttribute('data-target') === targetPanelID) {
        button.classList.add('nav-act');
        button.classList.remove('nav-pas');
      } else {
        button.classList.remove('nav-act');
        button.classList.add('nav-pas');
      }
    });

    // Check if the associated div exists
    if (targetPanel) {
        while (targetPanel.classList.contains('inactive')) {
            targetPanel.classList.remove('inactive');
        }
        targetPanel.classList.add('active');
        console.log(targetPanel);

        // Loop over all divs to reset others
        divs.forEach(div => {
            if (div.id !== targetPanelID) {
                while (div.classList.contains('active')) {
                  div.classList.remove('active');
                }
                div.classList.add('inactive');
            }
        });
    } else {
        console.error(`No div found with ID: ${targetPanelID}`);
    }
};

/*
 * Prep the fullscreen button
 */
export function fullscreenButton(): void {
  // Find the fullscreen button
  const fullscreenBtn = document.getElementById('fullscreenBtn');

  if (fullscreenBtn === null) {
    console.error('Fullscreen Button not found');
    return;
  }

  fullscreenBtn.addEventListener('click', function () {
    if (!document.fullscreenElement) {
      // Request fullscreen
      document.documentElement.requestFullscreen()
        .catch(err => console.error("Error attempting to enable full-screen mode:", err));
    } else {
      // Exit fullscreen
      document.exitFullscreen()
        .catch(err => console.error("Error attempting to exit full-screen mode:", err));
    }
  });
};
