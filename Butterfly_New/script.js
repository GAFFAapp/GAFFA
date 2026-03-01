function createButterfly() {
    const butterfly = document.createElement('div');
    butterfly.className = 'butterfly-particle';
    
    // وضع الفراشة في مكان أفقي عشوائي
    butterfly.style.left = Math.random() * 100 + 'vw';
    
    // حجم عشوائي للفراشة
    const size = Math.random() * 15 + 10 + 'px';
    butterfly.style.width = size;
    butterfly.style.height = size;
    
    // مدة طيران عشوائية
    const duration = Math.random() * 5 + 5 + 's';
    butterfly.style.animationDuration = duration;

    // إضافة شكل الفراشة (إيموجي أو رمز)
    butterfly.innerHTML = '🦋';
    
    document.body.appendChild(butterfly);

    // حذف الفراشة بعد انتهاء الأنميشن لتوفير ذاكرة الهاتف
    setTimeout(() => {
        butterfly.remove();
    }, parseFloat(duration) * 1000);
}

// توليد فراشة جديدة كل 600 مللي ثانية
setInterval(createButterfly, 600);

// دالة إرسال الرسائل (التي برمجناها سابقاً)
function sendMessage() {
    let input = document.getElementById("userInput");
    let chatBox = document.getElementById("chatBox");
    
    if (input.value.trim() !== "") {
        let msg = document.createElement("div");
        msg.className = "message outgoing";
        msg.textContent = input.value;
        chatBox.appendChild(msg);
        input.value = "";
        chatBox.scrollTop = chatBox.scrollHeight;
    }
}
.butterfly-particle {
    position: absolute;
    bottom: -50px;
    pointer-events: none; /* لكي لا تعيق الضغط على الأزرار */
    z-index: 1;
    animation: flyUp linear forwards;
    filter: drop-shadow(0 0 5px rgba(255, 255, 255, 0.5));
}

@keyframes flyUp {
    0% {
        transform: translateY(0) rotate(0deg) translateX(0);
        opacity: 0;
    }
    10% { opacity: 0.8; }
    50% {
        transform: translateY(-50vh) rotate(180deg) translateX(50px);
    }
    100% {
        transform: translateY(-110vh) rotate(360deg) translateX(-50px);
        opacity: 0;
    }
}

