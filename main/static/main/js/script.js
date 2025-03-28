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

    if (textElement) {
        // إعداد التلاشي بتأثير سلس
        textElement.style.transition = "opacity 0.6s ease-in-out";

        function typeThenFade(text) {
            textElement.textContent = "";
            textElement.style.opacity = "1";
            let charIndex = 0;

            function typeChar() {
                if (charIndex < text.length) {
                    textElement.textContent += text.charAt(charIndex);
                    charIndex++;
                    setTimeout(typeChar, 30); // سرعة الحروف
                } else {
                    setTimeout(() => {
                        textElement.style.opacity = "0";
                        setTimeout(() => {
                            index = (index + 1) % texts.length;
                            typeThenFade(texts[index]);
                        }, 800); // مدة التلاشي
                    }, 2000); // مدة بقاء العبارة
                }
            }

            typeChar();
        }

        typeThenFade(texts[index]);
    }
});
