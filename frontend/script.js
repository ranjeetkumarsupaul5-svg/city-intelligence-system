const messageInput = document.getElementById("message");
const chatBox = document.getElementById("chatBox");
const sendButton = document.getElementById("sendButton");


/* =========================================
   MARKDOWN & HTML RENDERING HELPERS
   ========================================= */

function escapeHtml(str) {
    if (!str) return "";
    return str
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function renderMarkdown(raw) {
    if (!raw) return "";

    let text = raw.replace(/\r\n/g, "\n").replace(/\r/g, "\n");
    text = escapeHtml(text);

    // Bold: **text**
    text = text.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");

    // Italic: *text* (when not preceded or followed by another asterisk)
    text = text.replace(/(^|[^\*])\*([^\*\n]+?)\*([^\*]|$)/g, "$1<em>$2</em>$3");

    // Inline code: `code`
    text = text.replace(/`([^`]+)`/g, "<code>$1</code>");

    // Markdown links: [text](url)
    text = text.replace(/\[([^\]]+)\]\((https?:\/\/[^\s\)]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>');

    // Bare URLs
    text = text.replace(/(^|[^">])(https?:\/\/[^\s<]+)/g, '$1<a href="$2" target="_blank" rel="noopener noreferrer">$2</a>');

    const lines = text.split("\n");
    let inList = false;
    let inTable = false;
    const output = [];

    for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        const trimmed = line.trim();

        // Bullet lists: - item or * item
        const listMatch = trimmed.match(/^[-*]\s+(.*)$/);
        if (listMatch) {
            if (!inList) {
                if (inTable) { output.push("</table></div>"); inTable = false; }
                output.push("<ul class=\"chat-list\">");
                inList = true;
            }
            output.push(`<li>${listMatch[1]}</li>`);
            continue;
        } else if (inList) {
            output.push("</ul>");
            inList = false;
        }

        // Tables: | col1 | col2 |
        if (trimmed.startsWith("|") && trimmed.endsWith("|")) {
            if (/^\|[\s\-:|]+\|$/.test(trimmed)) {
                continue;
            }
            if (!inTable) {
                output.push("<div class=\"chat-table-wrapper\"><table class=\"chat-table\">");
                inTable = true;
            }
            const cells = trimmed.slice(1, -1).split("|").map(c => c.trim());
            output.push("<tr>" + cells.map(c => `<td>${c}</td>`).join("") + "</tr>");
            continue;
        } else if (inTable) {
            output.push("</table></div>");
            inTable = false;
        }

        // Headings: ### Heading
        const headingMatch = trimmed.match(/^(#{1,6})\s+(.*)$/);
        if (headingMatch) {
            output.push(`<div class="chat-heading"><strong>${headingMatch[2]}</strong></div>`);
            continue;
        }

        // Empty line
        if (trimmed === "") {
            output.push("<div class=\"chat-spacer\"></div>");
            continue;
        }

        // Normal paragraph line
        output.push(`<p>${line}</p>`);
    }

    if (inList) output.push("</ul>");
    if (inTable) output.push("</table></div>");

    return output.join("");
}


function addMessage(message, type) {

    const wrapper = document.createElement("div");

    wrapper.className = `message ${type}`;

    const avatar = document.createElement("div");

    avatar.className = "avatar";

    avatar.innerText = type === "user" ? "YOU" : "AI";


    const content = document.createElement("div");

    content.className = "message-content";


    const label = document.createElement("span");

    label.className = "message-label";

    label.innerText = type === "user"
        ? "YOU"
        : "CITY AGENT";

    content.appendChild(label);

    if (type === "user") {
        const text = document.createElement("p");
        text.textContent = message;
        content.appendChild(text);
    } else {
        const bodyContainer = document.createElement("div");
        bodyContainer.className = "message-body";
        bodyContainer.innerHTML = renderMarkdown(message);
        content.appendChild(bodyContainer);
    }

    wrapper.appendChild(avatar);
    wrapper.appendChild(content);

    chatBox.appendChild(wrapper);

    chatBox.scrollTop = chatBox.scrollHeight;
}


function addActivity(text) {

    const activity = document.getElementById("activity");

    const item = document.createElement("div");

    item.className = "activity-item";

    item.innerHTML = `
        <span class="activity-dot"></span>

        <div>
            <strong>${text}</strong>
            <small>Just now</small>
        </div>
    `;

    activity.prepend(item);
}


/* =========================================
   WEATHER HELPERS & PARSING
   ========================================= */

function formatCondition(condition) {
    if (!condition) return "";
    return condition.charAt(0).toUpperCase() + condition.slice(1);
}

function extractWeatherData(input) {
    if (!input) return null;

    // Handle structured object input
    if (typeof input === "object") {
        if (input.weather && typeof input.weather === "object") {
            input = input.weather;
        }
        if (input.city && (input.temperature !== undefined || input.temp !== undefined)) {
            return {
                city: String(input.city).trim(),
                condition: String(input.condition || input.desc || "").trim(),
                temperature: String(input.temperature !== undefined ? input.temperature : input.temp).trim()
            };
        }
        if (typeof input.response === "string") {
            input = input.response;
        } else {
            return null;
        }
    }

    if (typeof input !== "string") return null;
    const text = input;

    let city = "";
    let condition = "";
    let temperature = "";

    // 1. Try Format A: "Weather in Bhopal: broken clouds, 23.2°C"
    const formatAMatch = text.match(/Weather in ([^:\n\r]+?):\s*([^,\n\r]+?),\s*([+-]?\d+(?:\.\d+)?)\s*°?C/i);
    if (formatAMatch) {
        city = formatAMatch[1].trim();
        condition = formatAMatch[2].trim();
        temperature = formatAMatch[3].trim();
        return { city, condition, temperature };
    }

    // 2. Try Format B and its variations
    // City matchers: **Bhopal Weather**, **Bhopal Weather (current)**, **Weather in Bhopal**, Bhopal Weather
    const cityMatch =
        text.match(/\*\*(?:Weather in\s+)?([A-Za-z\s]+?)(?:\s+Weather)?(?:\s*\([^)]*\))?\*\*/i) ||
        text.match(/(?:^|\n)\s*([A-Za-z\s]+?)\s+Weather/i) ||
        text.match(/Weather (?:in|for)\s+([A-Za-z\s]+?)(?:[:\n]|\*\*)/i);

    if (cityMatch) {
        city = cityMatch[1].replace(/^(?:Weather in|Weather for)\s+/i, "").trim();
    }

    // Condition matcher: - **Condition:** Broken clouds, - **Conditions:** Broken clouds, Condition: Broken clouds
    const conditionMatch =
        text.match(/(?:-\s*)?\*\*Conditions?:\*\*\s*([^\n\r]+)/i) ||
        text.match(/(?:-\s*)?Conditions?:\s*([^\n\r]+)/i);

    if (conditionMatch) {
        condition = conditionMatch[1].trim();
        condition = condition.replace(/\*\*.*$/, "").replace(/\(.*?\)/g, "").trim();
    }

    // Temperature matcher: - **Temperature:** 23.2 °C, Temperature: 23.26\u202f°C, 23.2°C
    const tempMatch =
        text.match(/(?:-\s*)?\*\*Temperature:\*\*\s*([+-]?\d+(?:\.\d+)?)/i) ||
        text.match(/(?:-\s*)?Temperature:\s*([+-]?\d+(?:\.\d+)?)/i) ||
        text.match(/([+-]?\d+(?:\.\d+)?)\s*(?:°|\u202f)*C/i);

    if (tempMatch) {
        temperature = tempMatch[1].trim();
    }

    if (city && temperature) {
        return { city, condition, temperature };
    }

    return null;
}


/* =========================================
   UPDATE WEATHER CARD
   ========================================= */

function updateWeatherCard(weatherInput) {

    if (!weatherInput) {
        return;
    }

    const data = extractWeatherData(weatherInput);

    if (!data || !data.city || !data.temperature) {
        return;
    }

    const temperatureElement = document.getElementById("temperature");
    const cityElement = document.getElementById("weatherCity");
    const weatherIcon = document.getElementById("weatherIcon") || document.querySelector(".weather-icon");

    // Clean temperature: extract numerical value
    const cleanTemp = data.temperature.replace(/[^\d.+-]/g, "");

    if (temperatureElement) {
        temperatureElement.innerText = `${cleanTemp}°C`;
    }

    if (cityElement) {
        const formattedCond = formatCondition(data.condition);
        cityElement.innerText = formattedCond
            ? `${data.city} • ${formattedCond}`
            : data.city;
    }

    if (weatherIcon) {
        const text = (data.condition || "").toLowerCase();

        if (text.includes("thunder") || text.includes("lightning")) {
            weatherIcon.innerText = "⛈️";
        }
        else if (text.includes("drizzle") || text.includes("shower") || text.includes("rain")) {
            weatherIcon.innerText = "🌧️";
        }
        else if (text.includes("snow") || text.includes("sleet") || text.includes("blizzard")) {
            weatherIcon.innerText = "❄️";
        }
        else if (text.includes("mist") || text.includes("fog") || text.includes("haze") || text.includes("smoke") || text.includes("dust")) {
            weatherIcon.innerText = "🌫️";
        }
        else if (text.includes("cloud") || text.includes("overcast")) {
            weatherIcon.innerText = "☁️";
        }
        else if (text.includes("clear") || text.includes("sun")) {
            weatherIcon.innerText = "☀️";
        }
        else {
            weatherIcon.innerText = "🌤️";
        }
    }
}


/* =========================================
   SEND MESSAGE
   ========================================= */

async function sendMessage() {

    const message = messageInput.value.trim();

    if (!message) {
        return;
    }

    addMessage(message, "user");

    addActivity("Processing request");

    messageInput.value = "";

    sendButton.disabled = true;

    try {

        const response = await fetch(
    `https://city-intelligence-system.onrender.com/chat?user_input=${encodeURIComponent(message)}`,
    {
        method: "POST"
    }
);

        const data = await response.json();

        addMessage(
            data.response,
            "bot"
        );

        // Update weather card: supports structured weather payload OR textual response (Format A / Format B)
        updateWeatherCard(data.weather || data.response);

        addActivity(
            "Response received"
        );

    } catch (error) {

        addMessage(
            "Unable to connect to the City Intelligence backend.",
            "bot"
        );

        addActivity(
            "Connection error"
        );

        console.error(error);

    } finally {

        sendButton.disabled = false;

    }
}


/* =========================================
   ENTER KEY
   ========================================= */

messageInput.addEventListener("keydown", function(event) {

    if (event.key === "Enter") {

        sendMessage();

    }

});