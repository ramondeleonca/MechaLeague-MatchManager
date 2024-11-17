// URL
const url = new URL(window.location.href);

// Elements
const timerElement = document.querySelector(".timer");
const blueAllianceElement = document.querySelector(".blue-alliance");
const redAllianceElement = document.querySelector(".red-alliance");

// Red alliance scores
const redAllianceTotalScoreElement = document.querySelector(".red-alliance-total-score");
const redAllianceGoalsElement = document.querySelector(".red-alliance-goals");
const redAllianceFoulsElement = document.querySelector(".red-alliance-fouls");

// Blue alliance scores
const blueAllianceTotalScoreElement = document.querySelector(".blue-alliance-total-score");
const blueAllianceGoalsElement = document.querySelector(".blue-alliance-goals");
const blueAllianceFoulsElement = document.querySelector(".blue-alliance-fouls");

// Controls element
/**
 * @type {HTMLDivElement}
 */
const controlsElement = document.querySelector(".controls");

/**
 * @type {HTMLDivElement}
 */
const noMatchElement = document.querySelector(".no-match");

// Update initial UI
if (url.searchParams.get("alliance") == "blue") {
    blueAllianceElement.classList.add("selected-alliance");
    controlsElement.classList.add("blue-alliance-controls");
} else if (url.searchParams.get("alliance") == "red") {
    redAllianceElement.classList.add("selected-alliance");
    controlsElement.classList.add("red-alliance-controls");
}

// Socket connection
const socket = io(window.location.host);
// const socket = io("localhost:80");

socket.on("connect", () => {
    console.log("Connected to server");
})

socket.on("disconnect", () => {
    noMatchElement.style.opacity = 1;
    noMatchElement.style.pointerEvents = "all";
    console.log("Disconnected from server");
})

socket.on("match_start", () => {
    noMatchElement.style.opacity = 0;
    noMatchElement.style.pointerEvents = "none";
})

socket.on("match_end", () => {
    noMatchElement.style.opacity = 1;
    noMatchElement.style.pointerEvents = "all";
})

socket.on("update", data => {
    redAllianceTotalScoreElement.innerHTML = data.red_alliance_total_score;
    redAllianceGoalsElement.innerHTML = data.red_alliance_goals;
    redAllianceFoulsElement.innerHTML = data.red_alliance_fouls;

    blueAllianceTotalScoreElement.innerHTML = data.blue_alliance_total_score;
    blueAllianceGoalsElement.innerHTML = data.blue_alliance_goals;
    blueAllianceFoulsElement.innerHTML = data.blue_alliance_fouls;
})

socket.on("match_time", data => {
    timerElement.innerHTML = data.match_time;
})

function addGoal() {
    socket.emit("add_goal", { alliance: url.searchParams.get("alliance") });
}

function addFoul() {
    socket.emit("add_foul", { alliance: url.searchParams.get("alliance") });
}

function subGoal() {
    socket.emit("sub_goal", { alliance: url.searchParams.get("alliance") });
}

function subFoul() {
    socket.emit("sub_foul", { alliance: url.searchParams.get("alliance") });
}