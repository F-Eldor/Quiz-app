const savollar = JSON.parse(document.getElementById("savollar-data").textContent);
console.log("Savollar data:", savollar); // Debug: Savollar tuzilmasini log qilish
let hozirgiSavol = 0;
let togrilar = 0;
let timerId = null; // Taymer ID si
let timeLeft = 15; // Har bir savol uchun 15 soniya

const questionBox = document.getElementById("question");
const optionsBox = document.getElementById("options");
const feedbackBox = document.getElementById("feedback");
const timerProgress = document.getElementById("timer-progress"); // Progress bar elementi

function startTimer() {
    timeLeft = 15; // Vaqtni 15 soniyaga qaytarish
    timerProgress.style.width = "100%"; // Progress bar 100% dan boshlanadi
    timerProgress.style.transition = "width 15s linear"; // 15 soniyada chiziqli qisqarish

    timerId = setInterval(() => {
        timeLeft--;

        if (timeLeft <= 0) {
            clearInterval(timerId);
            timerProgress.style.transition = "none"; // Tranzitsiyani o‘chirish
            timerProgress.style.width = "0%"; // Progress bar nolga tushadi
            feedbackBox.textContent = `❌ Vaqt tugadi! To'g'ri javob: ${savollar[hozirgiSavol][6]}`;
            hozirgiSavol++; // Keyingi savolga o‘tish
            setTimeout(() => {
                feedbackBox.textContent = "";
                keyingiSavol();
            }, 1000);
        }
    }, 1000);
}

function keyingiSavol() {
    if (hozirgiSavol >= 25) {
        yakunlaTest();
        return;
    }

    const savol = savollar[hozirgiSavol];
    questionBox.textContent = `Savol ${hozirgiSavol + 1}: ${savol[1]}`;
    optionsBox.innerHTML = "";

    for (let i = 0; i < 4; i++) {
        const btn = document.createElement("button");
        btn.textContent = savol[2 + i];
        btn.classList.add("option-btn");
        btn.onclick = function () {
            clearInterval(timerId); // Javob tanlanganda taymer to‘xtatiladi
            timerProgress.style.transition = "none"; // Tranzitsiyani o‘chirish
            timerProgress.style.width = "0%"; // Progress bar nolga tushadi
            if (btn.textContent === savol[6]) {
                togrilar++;
                feedbackBox.textContent = "✅ To‘g‘ri!";
            } else {
                feedbackBox.textContent = `❌ Noto‘g‘ri. To‘g‘ri javob: ${savol[6]}`;
            }

            hozirgiSavol++;
            setTimeout(() => {
                feedbackBox.textContent = "";
                keyingiSavol();
            }, 1000);
        };
        optionsBox.appendChild(btn);
    }

    startTimer(); // Yangi savol uchun taymerni boshlash
}

function yakunlaTest() {
    clearInterval(timerId); // Taymer to‘xtatiladi
    questionBox.textContent = "Test tugadi";
    optionsBox.innerHTML = "";
    feedbackBox.textContent = "Natijangiz hisoblanmoqda...";

    console.log("To‘g‘ri javoblar:", togrilar); // Debug: To‘g‘ri javoblar soni
    fetch("/submit", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            togrilar: togrilar,
            umumiy: 25
        })
    })
    .then(response => response.json())
    .then(data => {
        feedbackBox.innerHTML = `Sizning natijangiz: ${data.foiz}%<br><br>Ingliz tili darajangiz: <strong>${data.daraja}</strong><br><br><a href="/result">To‘liq natijani ko‘rish</a>`;
    })
    .catch(error => {
        console.error("Natijalarni yuborishda xato:", error);
        feedbackBox.textContent = "Xato yuz berdi. Iltimos, qayta urinib ko‘ring.";
    });
}

keyingiSavol();