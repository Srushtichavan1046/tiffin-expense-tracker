// ==========================================
// TIFFIN EXPENSE TRACKER
// JavaScript
// ==========================================


// Get HTML elements

const monthPicker = document.getElementById("monthPicker");

const entriesContainer =
    document.getElementById("entriesContainer");

const lunchDays =
    document.getElementById("lunchDays");

const dinnerDays =
    document.getElementById("dinnerDays");

const totalTiffins =
    document.getElementById("totalTiffins");

const lunchAmount =
    document.getElementById("lunchAmount");

const dinnerAmount =
    document.getElementById("dinnerAmount");

const monthlyBill =
    document.getElementById("monthlyBill");

const entryTitle =
    document.getElementById("entryTitle");


// ==========================================
// Convert DD-MM-YYYY to YYYY-MM
// ==========================================

function getMonth(date) {

    const parts = date.split("-");

    const day = parts[0];
    const month = parts[1];
    const year = parts[2];

    return year + "-" + month;
}


// ==========================================
// Convert DD-MM-YYYY to YYYY-MM-DD
// ==========================================

function getInputDate(date) {

    const parts = date.split("-");

    const day = parts[0];
    const month = parts[1];
    const year = parts[2];

    return year + "-" + month + "-" + day;
}


// ==========================================
// Display Entries
// ==========================================

function displayEntries(selectedMonth) {

    entriesContainer.innerHTML = "";

    let filteredEntries = entries;


    // Filter by month

    if (selectedMonth !== "all") {

        filteredEntries = entries.filter(function(entry) {

            return getMonth(entry.date) === selectedMonth;

        });

    }


    // No entries

    if (filteredEntries.length === 0) {

        entriesContainer.innerHTML = `
            <div class="empty">

                <div class="empty-icon">📭</div>

                <h3>No entries found</h3>

                <p>
                    No tiffin entries for this month.
                </p>

            </div>
        `;

        return;

    }


    // Display entries

    filteredEntries.forEach(function(entry) {

        const entryDiv =
            document.createElement("div");

        entryDiv.className = "entry";


        let lunchText;

        if (entry.lunch === "yes") {

            lunchText =
                `<span class="taken">₹${entry.lunch_price}</span>`;

        } else {

            lunchText =
                `<span class="not-taken">Not Taken</span>`;

        }


        let dinnerText;

        if (entry.dinner === "yes") {

            dinnerText =
                `<span class="taken">₹${entry.dinner_price}</span>`;

        } else {

            dinnerText =
                `<span class="not-taken">Not Taken</span>`;

        }


        entryDiv.innerHTML = `

            <div class="entry-date">

                <div class="date-icon">
                    📅
                </div>

                <div>

                    <strong>
                        ${entry.date}
                    </strong>

                    <small>
                        ${entry.day}
                    </small>

                </div>

            </div>


            <div class="entry-meal">

                <span>🍱 Lunch</span>

                ${lunchText}

            </div>


            <div class="entry-meal">

                <span>🍽️ Dinner</span>

                ${dinnerText}

            </div>


            <div class="entry-total">

                <span>Total</span>

                <strong>
                    ₹${entry.total}
                </strong>

            </div>


            <button
                class="edit-btn"
                onclick="editEntry('${entry.date}')"
            >

                ✏️ Edit

            </button>

        `;


        entriesContainer.appendChild(entryDiv);

    });

}


// ==========================================
// Calculate Monthly Summary
// ==========================================

function calculateSummary(selectedMonth) {

    let monthlyEntries = entries;


    if (selectedMonth !== "all") {

        monthlyEntries = entries.filter(function(entry) {

            return getMonth(entry.date) === selectedMonth;

        });

    }


    let lunchCount = 0;

    let dinnerCount = 0;

    let lunchTotal = 0;

    let dinnerTotal = 0;


    monthlyEntries.forEach(function(entry) {


        if (entry.lunch === "yes") {

            lunchCount++;

            lunchTotal += Number(entry.lunch_price);

        }


        if (entry.dinner === "yes") {

            dinnerCount++;

            dinnerTotal += Number(entry.dinner_price);

        }

    });


    const total = lunchTotal + dinnerTotal;

    const tiffins = lunchCount + dinnerCount;


    // Update screen

    lunchDays.textContent =
        lunchCount + " days";

    dinnerDays.textContent =
        dinnerCount + " days";

    totalTiffins.textContent =
        tiffins;

    lunchAmount.textContent =
        "₹" + lunchTotal;

    dinnerAmount.textContent =
        "₹" + dinnerTotal;

    monthlyBill.textContent =
        "₹" + total;

}


// ==========================================
// Month Changed
// ==========================================

monthPicker.addEventListener("change", function() {

    const selectedMonth =
        monthPicker.value;


    if (selectedMonth === "") {

        calculateSummary("all");

        displayEntries("all");

        entryTitle.textContent =
            "All saved entries";

        return;

    }


    calculateSummary(selectedMonth);

    displayEntries(selectedMonth);


    entryTitle.textContent =
        "Showing entries for " + selectedMonth;

});


// ==========================================
// Edit Entry
// ==========================================

function editEntry(date) {

    const selectedEntry =
        entries.find(function(entry) {

            return entry.date === date;

        });


    if (!selectedEntry) {

        return;

    }


    // Set date

    document.getElementById("date").value =
        getInputDate(selectedEntry.date);


    // Set lunch

    const lunchRadio =
        document.querySelector(
            `input[name="lunch"][value="${selectedEntry.lunch}"]`
        );

    if (lunchRadio) {

        lunchRadio.checked = true;

    }


    // Set dinner

    const dinnerRadio =
        document.querySelector(
            `input[name="dinner"][value="${selectedEntry.dinner}"]`
        );

    if (dinnerRadio) {

        dinnerRadio.checked = true;

    }


    // Scroll to form

    document.getElementById("entryForm")
        .scrollIntoView({
            behavior: "smooth"
        });

}


// ==========================================
// Initial Page Load
// ==========================================

calculateSummary("all");

displayEntries("all");