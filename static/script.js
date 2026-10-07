import { initializeApp } from "https://www.gstatic.com/firebasejs/12.11.0/firebase-app.js";
import { getAuth, onAuthStateChanged, signOut } from "https://www.gstatic.com/firebasejs/12.11.0/firebase-auth.js";
// import {
//     getStorage,
//     ref,
//     uploadBytes,
//     getDownloadURL
// } from "https://www.gstatic.com/firebasejs/12.11.0/firebase-storage.js";
// import { initializeApp } from "https://www.gstatic.com/firebasejs/12.11.0/firebase-app.js";

const firebaseConfig = window.firebaseConfig;

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
// const storage = getStorage(app);

const isDashboardPage = document.body.classList.contains("dashboard-body");

function parseUserIdentity(user) {
    const displayName = user && user.displayName ? user.displayName : "";
    const [storedUserId, ...nameParts] = displayName.split("|");

    if (/^[A-Z]{3}\d{3}$/.test(storedUserId)) {
        return {
            userId: storedUserId,
            userName: nameParts.join("|") || "User"
        };
    }

    return {
        userId: localStorage.getItem("userId") || user.uid,
        userName: displayName || "User"
    };
}

// ======================================================
// PROFILE PHOTO - WORKS ON ALL PAGES
// ======================================================

async function uploadProfilePhoto(file) {

    if (!file) {
        return;
    }

    // Check image type
    if (!file.type.startsWith("image/")) {
        alert("Please select an image file.");
        return;
    }

    // Maximum 5 MB
    if (file.size > 5 * 1024 * 1024) {
        alert("Image size must be less than 5 MB.");
        return;
    }

    const user = auth.currentUser;

    if (!user) {
        alert("Please login again.");
        return;
    }

    try {

        console.log("Uploading profile photo...");
        console.log("Firebase UID:", user.uid);

        const formData = new FormData();

        formData.append("photo", file);

        const response = await fetch(
            "/upload-profile-photo",
            {
                method: "POST",
                credentials: "include",
                body: formData
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.error ||
                "Could not upload profile photo"
            );
        }

        console.log(
            "Photo uploaded successfully:",
            data.photo_url
        );

        // Update image immediately
        updateProfileImages(
            data.photo_url
        );

        const photoButton =
            document.getElementById("photoButton");

        if (photoButton) {
            photoButton.innerText =
                "📷 Change Photo";
        }

       

    } catch (error) {

        console.error(
            "Profile photo upload error:",
            error
        );

        alert(
            error.message ||
            "Could not upload profile photo."
        );
    }
}

// ======================================================
// LOAD PROFILE PHOTO FROM MONGODB
// ======================================================

async function loadProfilePhoto() {

    try {

        const response =
            await fetch(
                "/get-profile-photo",
                {
                    method: "GET",
                    credentials: "include"
                }
            );

        if (!response.ok) {

            console.warn(
                "Could not load profile photo. Status:",
                response.status
            );

            return;
        }

        const data =
            await response.json();

        if (data.photo_url) {

            updateProfileImages(
                data.photo_url
            );
        }

    } catch (error) {

        console.error(
            "Error loading profile photo:",
            error
        );
    }
}


// ======================================================
// UPDATE ALL PROFILE IMAGES
// ======================================================

function updateProfileImages(photoURL) {

    const profileImages =
        document.querySelectorAll(
            ".profile-image"
        );

    profileImages.forEach(image => {

        image.src =
            photoURL +
            (
                photoURL.includes("?")
                    ? "&"
                    : "?"
            ) +
            "t=" +
            Date.now();

    });

    const photoButton =
        document.getElementById("photoButton");

    if (photoButton) {

        photoButton.innerText =
            "📷 Change Photo";
    }
}


// ======================================================
// PROFILE PHOTO INPUT
// ======================================================

function setupProfilePhotoUpload() {

    const uploadPhoto =
        document.getElementById(
            "uploadPhoto"
        );

    if (!uploadPhoto) {

        console.log(
            "Profile photo input not found on this page."
        );

        return;
    }

    uploadPhoto.addEventListener(
        "change",
        async function () {

            const file =
                this.files &&
                this.files[0];

            if (!file) {
                return;
            }

            await uploadProfilePhoto(file);

            // Allows selecting same file again
            this.value = "";
        }
    );
}


// ======================================================
// LOAD PROFILE PHOTO ON EVERY PAGE
// ======================================================

document.addEventListener(
    "DOMContentLoaded",
    () => {

        loadProfilePhoto();

        setupProfilePhotoUpload();

    }
);



window.addEventListener("load", () => {
    const features = document.querySelector(".features");

    if (features) {
        features.scrollLeft = 0;
    }
});

window.openCareerPath = function () {
    window.location.href = "/career-path";
};

window.openCareerTest = function () {
    window.location.href = "/form";
};

window.openDashboard = function () {
    window.location.href = "/dashboard";
};

window.openResultPage = function () {
    window.location.href = "/result";
};

if (isDashboardPage) {
    onAuthStateChanged(auth, async (user) => {
        const latestCareer = document.getElementById("latestCareer");
        const latestScore = document.getElementById("latestScore");
        const historyDiv = document.getElementById("history");
        const totalAttemptsEl = document.getElementById("totalAttempts");
        const avgScoreEl = document.getElementById("avgScore");
        const bestScoreEl = document.getElementById("bestScore");

        if (historyDiv) historyDiv.innerHTML = "";
        if (latestCareer) latestCareer.innerText = "Loading...";
        if (latestScore) latestScore.innerText = "";

        if (user) {
          
            const identity = parseUserIdentity(user);
            const fallbackUserId = identity.userId;
            
            localStorage.setItem("userId", fallbackUserId);
            
            const userNameElement = document.getElementById("userName");
            const userIdElement = document.getElementById("userId");
            
            // Show temporary details while MongoDB loads
            if (userNameElement) {
                userNameElement.innerText = identity.userName;
            }
            
            if (userIdElement) {
                userIdElement.innerText = "User ID: " + fallbackUserId;
            }
            
            // await loadProfilePhoto();

            // Load the saved profile from MongoDB
            try {
                const response = await fetch("/get-student-profile", {
                    method: "GET",
                    credentials: "include"
                });

                if (response.ok) {
                    const student = await response.json();
            
                    if (student.name && userNameElement) {
                        userNameElement.innerText = student.name;
                    }
            
                    if (student.user_id && userIdElement) {
                        userIdElement.innerText = "User ID: " + student.user_id;
            
                        // Keep the dashboard's existing history key working
                        localStorage.setItem("userId", student.user_id);
                    }
                } else {
                    console.warn(
                        "Could not load MongoDB profile. HTTP status:",
                        response.status
                    );
                }
            } catch (error) {
                console.error("Error loading student profile:", error);
            }
            
            // Preserve your existing dashboard history and charts
            loadDashboard(localStorage.getItem("userId") || fallbackUserId);
            return;
        }

        localStorage.removeItem("userId");

        if (latestCareer) latestCareer.innerText = "No user logged in";
        if (latestScore) latestScore.innerText = "";
        if (totalAttemptsEl) totalAttemptsEl.innerText = 0;
        if (avgScoreEl) avgScoreEl.innerText = 0;
        if (bestScoreEl) bestScoreEl.innerText = 0;

        window.location.href = "/login";
    });

    window.logout = async function () {
        try {
            await fetch("/logout", { credentials: "include" });
        } catch (error) {
            console.warn("Logout request failed", error);
        }

        try {
            await signOut(auth);
        } catch (error) {
            console.warn("Firebase sign-out failed", error);
        }

        localStorage.removeItem("userId");
        window.location.href = "/login";
    };



async function loadDashboard(userId) {
    const latestCareer = document.getElementById("latestCareer");
    const latestScore = document.getElementById("latestScore");
    const historyDiv = document.getElementById("history");
    const totalAttemptsEl = document.getElementById("totalAttempts");
    const avgScoreEl = document.getElementById("avgScore");
    const bestScoreEl = document.getElementById("bestScore");
    const insightText = document.getElementById("insightText");

    if (!historyDiv) return;

    try {
        // Fetch quiz history from MongoDB through Flask
        const response = await fetch("/quiz-history", {
            method: "GET",
            credentials: "include"
        });

        if (!response.ok) {
            throw new Error("Quiz history request failed: " + response.status);
        }

        const history = await response.json();

        // Sort newest attempt first
        history.sort((a, b) =>
            new Date(b.completed_at) - new Date(a.completed_at)
        );

        historyDiv.innerHTML = "";

        if (history.length === 0) {
            if (latestCareer) latestCareer.innerText = "No attempts yet";
            if (latestScore) latestScore.innerText = "Take a quiz to see results";
            if (totalAttemptsEl) totalAttemptsEl.innerText = "0";
            if (avgScoreEl) avgScoreEl.innerText = "0";
            if (bestScoreEl) bestScoreEl.innerText = "0";
            if (insightText) insightText.innerText = "";

            if (window.barChart) {
                window.barChart.destroy();
                window.barChart = null;
            }

            if (window.pieChart) {
                window.pieChart.destroy();
                window.pieChart = null;
            }

            return;
        }

        // Latest quiz result
        const latest = history[0];

        if (latestCareer) {
            latestCareer.innerText = latest.career || "Unknown career";
        }

        if (latestScore) {
            latestScore.innerText =
                `Score: ${latest.score}/${latest.total_questions}`;
        }

        // Calculate dashboard statistics
        let totalScore = 0;
        let bestScore = 0;

        history.forEach(item => {
            const score = Number(item.score) || 0;

            totalScore += score;
            bestScore = Math.max(bestScore, score);
        });

        const totalAttempts = history.length;
        const avgScore = (totalScore / totalAttempts).toFixed(1);

        if (totalAttemptsEl) {
            totalAttemptsEl.innerText = totalAttempts;
        }

        if (avgScoreEl) {
            avgScoreEl.innerText = avgScore;
        }

        if (bestScoreEl) {
            bestScoreEl.innerText = bestScore;
        }

        // Display quiz attempt history
        history.forEach((item, index) => {
            const row = document.createElement("p");
            const title = document.createElement("b");

            title.textContent =
                `Attempt ${history.length - index} - ` +
                `${item.career || "Quiz"} - ` +
                `${item.score}/${item.total_questions}`;

            row.appendChild(title);

            if (index === 0) {
                const badge = document.createElement("span");
                badge.className = "latest-badge";
                badge.textContent = " (Latest)";
                row.appendChild(badge);
            }

            row.appendChild(document.createElement("br"));

            const date = document.createElement("small");

            date.textContent = item.completed_at
                ? new Date(item.completed_at).toLocaleString()
                : "Date unavailable";

            row.appendChild(date);
            historyDiv.appendChild(row);
            historyDiv.appendChild(document.createElement("hr"));
        });

        // Draw charts after the dashboard content is loaded
        setTimeout(() => {
            const barCanvas = document.getElementById("barChart");
            const pieCanvas = document.getElementById("pieChart");

            if (!barCanvas || !pieCanvas) {
                console.error("Chart canvas elements were not found.");
                return;
            }

            if (typeof Chart === "undefined") {
                console.error("Chart.js has not loaded.");
                return;
            }

           
            if (window.barChart instanceof Chart) {
                window.barChart.destroy();
            }
            
            if (window.pieChart instanceof Chart) {
                window.pieChart.destroy();
            }
            
            window.barChart = null;
            window.pieChart = null;

            // Performance chart: oldest attempt first
            const chronologicalHistory = [...history].reverse();

            const labels = chronologicalHistory.map(
                (_, index) => `Attempt ${index + 1}`
            );

            const scores = chronologicalHistory.map(
                item => Number(item.score) || 0
            );

           const performanceInner =
                document.querySelector(".performance-chart-inner");

           performanceInner.style.width =
               `${Math.max(700, labels.length * 75)}px`;

            window.barChart = new Chart(barCanvas.getContext("2d"), {
                type: "bar",
                data: {
                    labels: labels,
                    datasets: [{
                        label: "Quiz Score",
                        data: scores,
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            });

            // Score distribution
            let good = 0;
            let average = 0;
            let poor = 0;

            history.forEach(item => {
                const score = Number(item.score) || 0;

                // Use percentage so quizzes with different question
                // counts can be compared fairly.
                const percentage = Number(item.percentage) ||
                    (Number(item.total_questions)
                        ? score / Number(item.total_questions) * 100
                        : 0);

                if (percentage >= 70) {
                    good++;
                } else if (percentage >= 40) {
                    average++;
                } else {
                    poor++;
                }
            });

            window.pieChart = new Chart(
                pieCanvas.getContext("2d"),
                {
                    type: "doughnut",
                    data: {
                        labels: ["Good", "Average", "Poor"],
                        datasets: [{
                            data: [good, average, poor],
                            backgroundColor: [
                                "#49A9EA",
                                "#FF6384",
                                "#FF9F40"
                            ],
                            borderWidth: 0
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        cutout: "70%",
                        plugins: {
                            legend: {
                                position: "bottom",
                                labels: {
                                    color: "#ccc"
                                }
                            },
                            tooltip: {
                                callbacks: {
                                    label: function(context) {
                                        const total =
                                            context.dataset.data.reduce(
                                                (a, b) => a + b, 0
                                            );

                                        const value = context.raw;
                                        const percent = total
                                            ? ((value / total) * 100).toFixed(1)
                                            : "0.0";

                                        return `${context.label}: ${value} attempts (${percent}%)`;
                                    }
                                }
                            }
                        }
                    },
                   
                    plugins: [{
    id: "centerText",

    beforeDraw(chart) {

        const { ctx, chartArea } = chart;

        if (!chartArea) return;

        const total =
            chart.data.datasets[0].data.reduce(
                (a, b) => a + b,
                0
            );

        const centerX =
            (chartArea.left + chartArea.right) / 2;

        const centerY =
            (chartArea.top + chartArea.bottom) / 2;

        ctx.save();

        // Number
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";

        ctx.font = "bold 26px sans-serif";
        ctx.fillStyle = "#ffffff";

        ctx.fillText(
            total,
            centerX,
            centerY - 10
        );

        // Attempts text
        ctx.font = "14px sans-serif";
        ctx.fillStyle = "#cccccc";

        ctx.fillText(
            "Attempts",
            centerX,
            centerY + 18
        );

        ctx.restore();
    }
}]
                }
            );

            // Performance insight
            if (insightText) {
                if (good >= average && good >= poor) {
                    insightText.innerText =
                        "You are consistently performing well 🎯";
                } else if (average >= good && average >= poor) {
                    insightText.innerText =
                        "Your performance is moderate, improvement needed 📈";
                } else {
                    insightText.innerText =
                        "Your performance needs improvement ⚠️";
                }
            }
        }, 150);

    } catch (error) {
        console.error("Dashboard history error:", error);

        historyDiv.innerText = "Could not load quiz history.";

        if (latestCareer) {
            latestCareer.innerText = "Unable to load result";
        }

        if (latestScore) {
            latestScore.innerText = "";
        }
    }
}
}
