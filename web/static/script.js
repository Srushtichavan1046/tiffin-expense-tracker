// ==========================================
// 🍱 TIFFIN EXPENSE TRACKER - V6
// ==========================================

const monthPicker = document.getElementById("monthPicker");
const entriesContainer = document.getElementById("entriesContainer");

const lunchDays = document.getElementById("lunchDays");
const dinnerDays = document.getElementById("dinnerDays");
const totalTiffins = document.getElementById("totalTiffins");
const monthlyBill = document.getElementById("monthlyBill");

const lunchAmount = document.getElementById("lunchAmount");
const dinnerAmount = document.getElementById("dinnerAmount");

const entryTitle = document.getElementById("entryTitle");


// ==========================================
// 🇮🇳 INDIAN NATIONAL / MAJOR HOLIDAYS
// ==========================================

const holidays = {
    "01-01": "New Year",
    "01-26": "Republic Day 🇮🇳",
    "08-15": "Independence Day 🇮🇳",
    "10-02": "Gandhi Jayanti 🇮🇳",
    "11-14": "Children's Day",
    "12-25": "Christmas 🎄"
};


// ==========================================
// GET TODAY
// ==========================================

function getToday() {

    const today = new Date();

    const year = today.getFullYear();

    const month =
        String(today.getMonth() + 1).padStart(2, "0");

    const day =
        String(today.getDate()).padStart(2, "0");

    return `${year}-${month}-${day}`;
}


// ==========================================
// SET CURRENT MONTH
// ==========================================

function setCurrentMonth() {

    const today = new Date();

    const year = today.getFullYear();

    const month =
        String(today.getMonth() + 1).padStart(2, "0");

    monthPicker.value = `${year}-${month}`;
}


// ==========================================
// CONVERT DD-MM-YYYY
// TO YYYY-MM-DD
// ==========================================

function convertDate(dateString) {

    if (!dateString) {
        return "";
    }

    const parts = dateString.split("-");

    if (parts.length !== 3) {
        return "";
    }

    const day = parts[0];
    const month = parts[1];
    const year = parts[2];

    return `${year}-${month}-${day}`;
}


// ==========================================
// CONVERT YYYY-MM-DD
// TO DD-MM-YYYY
// ==========================================

function formatDate(date) {

    const day =
        String(date.getDate()).padStart(2, "0");

    const month =
        String(date.getMonth() + 1).padStart(2, "0");

    const year =
        date.getFullYear();

    return `${day}-${month}-${year}`;
}


// ==========================================
// GET HOLIDAY
// ==========================================

function getHoliday(date) {

    const month =
        String(date.getMonth() + 1).padStart(2, "0");

    const day =
        String(date.getDate()).padStart(2, "0");

    const key = `${month}-${day}`;

    return holidays[key] || "";
}


// ==========================================
// FIND ENTRY FOR DATE
// ==========================================

function findEntry(dateString) {

    return entries.find(function(entry) {

        return entry.date === dateString;

    });

}


// ==========================================
// SHOW MONTH DATA
// ==========================================

function showMonthData() {

    const selectedMonth = monthPicker.value;

    if (!selectedMonth) {
        return;
    }

    let monthEntries = [];

    for (let entry of entries) {

        const convertedDate =
            convertDate(entry.date);

        if (convertedDate.startsWith(selectedMonth)) {

            monthEntries.push(entry);

        }

    }


    // ======================================
    // SUMMARY CALCULATION
    // ======================================

    let lunchCount = 0;
    let dinnerCount = 0;

    let total = 0;

    let lunchTotal = 0;
    let dinnerTotal = 0;


    for (let entry of monthEntries) {

        if (entry.lunch === "yes") {

            lunchCount++;

            lunchTotal +=
                Number(entry.lunch_price || 0);

        }


        if (entry.dinner === "yes") {

            dinnerCount++;

            dinnerTotal +=
                Number(entry.dinner_price || 0);

        }


        total +=
            Number(entry.total || 0);

    }


    const totalMeals =
        lunchCount + dinnerCount;


    // ======================================
    // UPDATE SUMMARY
    // ======================================

    lunchDays.textContent =
        `${lunchCount} days`;

    dinnerDays.textContent =
        `${dinnerCount} days`;

    totalTiffins.textContent =
        totalMeals;

    monthlyBill.textContent =
        `₹${total}`;

    lunchAmount.textContent =
        `₹${lunchTotal}`;

    dinnerAmount.textContent =
        `₹${dinnerTotal}`;


    // ======================================
    // MONTH NAME
    // ======================================

    const [year, month] =
        selectedMonth.split("-");

    const monthName =
        new Date(year, month - 1)
            .toLocaleString("en-IN", {
                month: "long"
            });


    entryTitle.textContent =
        `${monthName} ${year} entries`;


    // ======================================
    // DISPLAY
    // ======================================

    displayCalendar(
        Number(year),
        Number(month) - 1
    );

    displayEntries(monthEntries);

}


// ==========================================
// DISPLAY CALENDAR
// ==========================================

function displayCalendar(year, month) {

    let firstDay =
        new Date(year, month, 1).getDay();

    let daysInMonth =
        new Date(year, month + 1, 0).getDate();


    let monthName =
        new Date(year, month)
            .toLocaleString("en-IN", {
                month: "long"
            });


    let calendarHTML = `

        <div class="calendar">

            <div class="calendar-header">

                <h3>
                    📅 ${monthName} ${year}
                </h3>

                <div class="calendar-legend">

                    <span>
                        ☀️ Sunday
                    </span>

                    <span>
                        🇮🇳 Holiday
                    </span>

                    <span>
                        🍱 Entry
                    </span>

                </div>

            </div>

            <div class="calendar-week">

                <div>Sun</div>
                <div>Mon</div>
                <div>Tue</div>
                <div>Wed</div>
                <div>Thu</div>
                <div>Fri</div>
                <div>Sat</div>

            </div>

            <div class="calendar-days">
    `;


    // Empty boxes before first day

    for (let i = 0; i < firstDay; i++) {

        calendarHTML += `
            <div class="calendar-day empty"></div>
        `;

    }


    // Days

    for (let day = 1; day <= daysInMonth; day++) {

        const date =
            new Date(year, month, day);

        const formattedDate =
            formatDate(date);

        const entry =
            findEntry(formattedDate);

        const holiday =
            getHoliday(date);


        const isSunday =
            date.getDay() === 0;


        const today =
            date.toISOString().split("T")[0] === getToday();


        let classes =
            "calendar-day";


        if (isSunday) {
            classes += " sunday";
        }


        if (holiday) {
            classes += " holiday";
        }


        if (entry) {
            classes += " has-entry";
        }


        if (today) {
            classes += " today";
        }


        let mealInfo = "";


        if (entry) {

            if (entry.lunch === "yes") {

                mealInfo +=
                    `<span>🍱 Lunch</span>`;

            }


            if (entry.dinner === "yes") {

                mealInfo +=
                    `<span>🍽️ Dinner</span>`;

            }


            if (
                entry.lunch === "no" &&
                entry.dinner === "no"
            ) {

                mealInfo =
                    `<span>❌ No Tiffin</span>`;

            }

        }


        calendarHTML += `

            <div
                class="${classes}"
                onclick="selectCalendarDate('${formattedDate}')"
                title="${holiday || formattedDate}"
            >

                <div class="calendar-date">

                    ${day}

                </div>

                ${holiday
                    ? `<div class="holiday-name">${holiday}</div>`
                    : ""
                }

                <div class="calendar-meals">

                    ${mealInfo}

                </div>

                ${entry
                    ? `<strong class="calendar-total">
                         ₹${entry.total}
                       </strong>`
                    : ""
                }

            </div>

        `;

    }


    calendarHTML += `

            </div>

        </div>

    `;


    // Put calendar before entries

    const oldCalendar =
        document.getElementById("monthlyCalendar");

    if (oldCalendar) {

        oldCalendar.remove();

    }


    const calendarWrapper =
        document.createElement("div");

    calendarWrapper.id =
        "monthlyCalendar";

    calendarWrapper.innerHTML =
        calendarHTML;


    entriesContainer.parentNode.insertBefore(
        calendarWrapper,
        entriesContainer
    );

}


// ==========================================
// SELECT DATE FROM CALENDAR
// ==========================================

function selectCalendarDate(dateString) {

    const dateInput =
        document.getElementById("date");

    dateInput.value = dateString;


    const entry =
        findEntry(formatDate(new Date(dateString + "T00:00:00")));


    if (entry) {

        selectRadio(
            "lunch",
            entry.lunch
        );

        selectRadio(
            "dinner",
            entry.dinner
        );

    } else {

        // Clear selection

        const lunchRadios =
            document.querySelectorAll(
                'input[name="lunch"]'
            );

        lunchRadios.forEach(
            radio => radio.checked = false
        );


        const dinnerRadios =
            document.querySelectorAll(
                'input[name="dinner"]'
            );

        dinnerRadios.forEach(
            radio => radio.checked = false
        );

    }


    document.getElementById("entryForm")
        .scrollIntoView({
            behavior: "smooth",
            block: "center"
        });

}


// ==========================================
// SELECT RADIO
// ==========================================

function selectRadio(name, value) {

    const radio =
        document.querySelector(
            `input[name="${name}"][value="${value}"]`
        );


    if (radio) {

        radio.checked = true;

    }

}


// ==========================================
// DISPLAY ENTRIES
// ==========================================

function displayEntries(monthEntries) {

    entriesContainer.innerHTML = "";


    if (monthEntries.length === 0) {

        entriesContainer.innerHTML = `

            <div class="entry empty-entry">

                <p>
                    📭 No entries found for this month.
                </p>

                <small>
                    Add an entry using the form above.
                </small>

            </div>

        `;

        return;

    }


    // Newest first

    monthEntries.sort(function(a, b) {

        return convertDate(b.date)
            .localeCompare(
                convertDate(a.date)
            );

    });


    for (let entry of monthEntries) {

        const date =
            new Date(
                convertDate(entry.date) + "T00:00:00"
            );


        const holiday =
            getHoliday(date);


        const sunday =
            date.getDay() === 0;


        const lunchText =
            entry.lunch === "yes"
                ? `₹${entry.lunch_price}`
                : "Not Taken";


        const dinnerText =
            entry.dinner === "yes"
                ? `₹${entry.dinner_price}`
                : "Not Taken";


        let badges = "";


        if (sunday) {

            badges += `
                <span class="badge sunday-badge">
                    ☀️ Sunday
                </span>
            `;

        }


        if (holiday) {

            badges += `
                <span class="badge holiday-badge">
                    🇮🇳 ${holiday}
                </span>
            `;

        }


        const entryHTML = `

            <div class="entry">

                <div class="entry-top">

                    <div>

                        <strong>
                            📅 ${entry.date}
                        </strong>

                        <p class="entry-day">
                            ${entry.day}
                        </p>

                    </div>

                    <div class="badges">

                        ${badges}

                    </div>

                </div>


                <div class="meal-result">

                    <div class="meal-result-row">

                        <span>
                            🍱 Lunch
                        </span>

                        <strong>
                            ${lunchText}
                        </strong>

                    </div>


                    <div class="meal-result-row">

                        <span>
                            🍽️ Dinner
                        </span>

                        <strong>
                            ${dinnerText}
                        </strong>

                    </div>

                </div>


                <div class="entry-total">

                    <span>
                        Total
                    </span>

                    <strong>
                        ₹${entry.total}
                    </strong>

                </div>


                <button
                    class="edit-btn"
                    onclick="editEntry('${entry.date}')"
                >

                    ✏️ Edit This Date

                </button>

            </div>

        `;


        entriesContainer.innerHTML +=
            entryHTML;

    }

}


// ==========================================
// EDIT ENTRY
// ==========================================

function editEntry(dateString) {

    const selectedDate =
        convertDate(dateString);


    document.getElementById("date").value =
        selectedDate;


    const entry =
        entries.find(function(item) {

            return item.date === dateString;

        });


    if (!entry) {
        return;
    }


    selectRadio(
        "lunch",
        entry.lunch
    );


    selectRadio(
        "dinner",
        entry.dinner
    );


    const formCard =
        document.querySelector(".form-card");


    if (formCard) {

        formCard.classList.add("editing");

        setTimeout(function() {

            formCard.classList.remove("editing");

        }, 1500);

    }


    document.getElementById("entryForm")
        .scrollIntoView({
            behavior: "smooth",
            block: "center"
        });

}


// ==========================================
// MONTH CHANGE
// ==========================================

monthPicker.addEventListener(
    "change",
    showMonthData
);


// ==========================================
// DATE CHANGE
// ==========================================

const dateInput =
    document.getElementById("date");


if (dateInput) {

    dateInput.addEventListener(
        "change",
        function() {

            const selectedDate =
                this.value;

            const displayDate =
                selectedDate.split("-")
                    .reverse()
                    .join("-");


            const entry =
                findEntry(displayDate);


            if (entry) {

                selectRadio(
                    "lunch",
                    entry.lunch
                );

                selectRadio(
                    "dinner",
                    entry.dinner
                );

            }

        }
    );

}


// ==========================================
// INITIALIZE
// ==========================================

setCurrentMonth();


// Automatically select today's date

if (dateInput) {

    dateInput.value =
        getToday();

}


showMonthData();


// ==========================================
// ANIMATION FOR NUMBERS
// ==========================================

function animateValue(element, finalValue) {

    if (!element) {
        return;
    }

    let start = 0;

    const duration = 400;

    const startTime =
        performance.now();


    function update(currentTime) {

        const progress =
            Math.min(
                (currentTime - startTime) / duration,
                1
            );


        const value =
            Math.floor(
                progress * finalValue
            );


        element.textContent = value;


        if (progress < 1) {

            requestAnimationFrame(update);

        }

    }


    requestAnimationFrame(update);

}