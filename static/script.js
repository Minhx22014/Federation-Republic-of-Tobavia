const loading = document.getElementById("loading");

// Nếu đã vào web rồi trong phiên này → không loading
if (sessionStorage.getItem("visited")) {
    loading.style.display = "none";
} else {
    // Lần đầu mở web
    sessionStorage.setItem("visited", "yes");

    // Giả loading 1 chút cho có cảm giác
    window.addEventListener("load", () => {
        setTimeout(() => {
            loading.style.display = "none";
        }, 2500); // chỉnh thời gian ở đây
    });
}


// 1. Khi trang vừa load, kiểm tra trí nhớ
if (localStorage.getItem("darkMode") === "on") {
    document.body.classList.add("dark");
}

// 2. Gắn sự kiện cho nút
const darkBtn = document.getElementById("dark");

darkBtn.addEventListener("click", () => {
    document.body.classList.toggle("dark");

    // 3. Lưu trạng thái
    if (document.body.classList.contains("dark")) {
        localStorage.setItem("darkMode", "on");
    } else {
        localStorage.setItem("darkMode", "off");
    }
});

async function sendMessage() {
    const user = document.getElementById("username").value;
    const message = document.getElementById("message").value;
    if (!user || !message) return;

    await fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({user, message})
    });

    document.getElementById("message").value = "";
    loadMessages();
}

async function loadMessages() {
    const res = await fetch("/chat");
    const data = await res.json();
    const container = document.getElementById("messages");
    container.innerHTML = "";
    data.forEach(msg => {
        const div = document.createElement("div");
        div.textContent = `${msg.user}: ${msg.message}`;
        container.appendChild(div);
    });
}

setInterval(loadMessages, 1000); // 1 giây load lại