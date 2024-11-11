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

  let data: string = "";

  if (response === null) {
    console.error("Failed to fetch", endpoint);
    data = "ERROR";
  } else {
    data = await response.text();
  }

  return data;
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
    } else if (Globals.timer === "STOPPED") {
      timerElement.classList.add("stopped");
    } else if (Globals.timer === "PAUSED") {
      timerElement.classList.add("paused");
    } else {
      timerElement.classList.add("mtquart");
    }
  }
  return;
};

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

/*
 * Unblock Page
 */
export function unblockPage(): void {
  let page_block_element = document.querySelector<HTMLDivElement>("#page_blocker")!;
  page_block_element.classList.add("hide");
};
