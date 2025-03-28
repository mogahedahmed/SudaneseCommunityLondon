document.addEventListener("DOMContentLoaded", function () {
    const slider = document.querySelector(".news-slider");
    const dots = document.querySelectorAll(".slider-dot");
    const slides = document.querySelectorAll(".news-slide");
    let index = 0;

    function updateSlider() {
        slides.forEach((slide, i) => {
            slide.style.transform = `translateX(${(i - index) * 100}%)`;
        });

        dots.forEach((dot, i) => {
            dot.classList.toggle("active", i === index);
        });

        index = (index + 1) % slides.length;
    }

    updateSlider(); // عرض أولي عند فتح الصفحة

    setInterval(updateSlider, 4000);

    // دعم الضغط على النقاط
    dots.forEach((dot, i) => {
        dot.addEventListener("click", () => {
            index = i;
            updateSlider();
        });
    });
});
