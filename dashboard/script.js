const BACKEND_URL = "http://127.0.0.1:8000";

// =====================================
// LOAD SECURITY EVENTS
// =====================================

async function loadEvents() {
  try {
    const response = await fetch(`${BACKEND_URL}/events`);

    const events = await response.json();

    // =================================
    // TOTAL EVENTS
    // =================================

    document.getElementById("total-events").textContent = events.length;

    // =================================
    // INTRUSIONS
    // =================================

    const intrusionCount = events.filter((event) => {
      return (
        event.event_type && event.event_type.toLowerCase().includes("intrusion")
      );
    }).length;

    document.getElementById("intrusion-events").textContent = intrusionCount;

    // =================================
    // HIGH / CRITICAL RISK
    // =================================

    const highRiskCount = events.filter((event) => {
      return event.risk_level === "HIGH" || event.risk_level === "CRITICAL";
    }).length;

    document.getElementById("high-risk-events").textContent = highRiskCount;

    // =================================
    // EVENTS TABLE
    // =================================

    const table = document.getElementById("events-table");

    if (events.length === 0) {
      table.innerHTML = `

                <tr>

                    <td colspan="7">

                        No security events detected

                    </td>

                </tr>

            `;

      return;
    }

    // Clear table

    table.innerHTML = "";

    // Show latest 20 events

    events.slice(0, 20).forEach((event) => {
      const row = document.createElement("tr");

      row.innerHTML = `

                    <td>
                        ${event.event_type || "Intrusion"}
                    </td>


                    <td>
                        #${event.person_id ?? "-"}
                    </td>


                    <td>
                        ${event.zone || "Restricted Zone"}
                    </td>


                    <td>
                        ${event.date || "-"}
                    </td>


                    <td>
                        ${event.time || "-"}
                    </td>


                    <td>
                        ${event.risk_level || "HIGH"}
                    </td>


                    <td>
                        ${event.status || "Unresolved"}
                    </td>

                `;

      table.appendChild(row);
    });
  } catch (error) {
    console.error("Could not load events:", error);
  }
}

// =====================================
// CHECK LATEST INTRUSION
// =====================================

async function checkLatestEvent() {
  try {
    const response = await fetch(`${BACKEND_URL}/latest-event`);

    const data = await response.json();

    const alertBox = document.getElementById("intrusion-alert");

    const alertMessage = document.getElementById("alert-message");

    // =================================
    // INTRUSION DETECTED
    // =================================

    if (data.status === "event_detected") {
      const event = data.event;

      alertBox.classList.add("danger");

      alertMessage.textContent =
        `🚨 ${event.event} | ` +
        `Person #${event.person_id} | ` +
        `${event.zone} | ` +
        `${event.time}`;
    }

    // =================================
    // NO EVENT
    // =================================
    else {
      alertBox.classList.remove("danger");

      alertMessage.textContent =
        "🟢 System monitoring — " + "No recent intrusion";
    }
  } catch (error) {
    console.error("Could not connect to backend:", error);

    const alertBox = document.getElementById("intrusion-alert");

    const alertMessage = document.getElementById("alert-message");

    alertBox.classList.remove("danger");

    alertMessage.textContent = "🔴 Backend connection error";
  }
}

// =====================================
// INITIAL LOAD
// =====================================

loadEvents();

checkLatestEvent();

// =====================================
// AUTOMATIC REFRESH
// =====================================

// Check latest intrusion every second

setInterval(checkLatestEvent, 1000);

// Refresh event history every 3 seconds

setInterval(loadEvents, 3000);
