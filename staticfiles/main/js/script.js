document.addEventListener("DOMContentLoaded", function () {
    const texts = [
        "بقوتنا في تواصلنا، نبني مجتمعاً لا يتجزأ",
        "يدٌ واحدة لا تصفق، لكن مجتمعاً مترابطاً ينهض بالأمة",
        "الجالية قلبٌ واحد، وإن تنوعت الأفراد",
        "الترابط ليس خياراً... هو أساس الانتماء",
        "من أجل غدٍ أقوى، نبني اليوم جسور المحبة والتواصل",
        "قوتنا في وحدتنا، ونجاحنا في تعاوننا"
    ];

    let index = 0;
    const textElement = document.getElementById("changing-text");

    // إضافة تأثير الانتقال للتلاشي
    textElement.style.transition = "opacity 1s ease-in-out";

    function typeThenFade(text) {
        textElement.textContent = "";
        textElement.style.opacity = "1";
        let charIndex = 0;

        function typeChar() {
            if (charIndex < text.length) {
                textElement.textContent += text.charAt(charIndex);
                charIndex++;
                setTimeout(typeChar, 50); // سرعة كتابة الحروف
            } else {
                // بعد الانتهاء من الكتابة، انتظر قليلاً ثم أبدأ التلاشي
                setTimeout(() => {
                    textElement.style.opacity = "0";
                    // بعد التلاشي، انتقل للعبارة التالية
                    setTimeout(() => {
                        index = (index + 1) % texts.length;
                        typeThenFade(texts[index]);
                    }, 1000); // وقت التلاشي
                }, 2000); // وقت ظهور العبارة قبل التلاشي
            }
        }

        typeChar();
    }

    typeThenFade(texts[index]); // البداية
});
