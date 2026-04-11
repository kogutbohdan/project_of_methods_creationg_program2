// дістаємо XPath з адресного рядка
let params = new URLSearchParams(window.location.search);
let xpath = params.get("xpath");

if (xpath) {
    let el = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
    if (el) {
        // прокрутка до елемента
        el.scrollIntoView({ behavior: "smooth", block: "center" });
        // підсвічування
        el.style.outline = "3px solid red";

        const hover=()=>{
            el.style.outline = "";
            el.removeEventListener("mouseenter",hover)
        }
        el.addEventListener("mouseenter",hover)
    } else {
        console.log("Елемент не знайдено за XPath:", xpath);
    }
} else {
    console.log("В URL немає параметра xpath");
}