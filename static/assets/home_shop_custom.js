function loadMore() {
    const loadMoreBtn = document.getElementById("loadMore");
    const productsHolder = document.getElementById("productsHolder");

    loadMoreBtn.addEventListener("click", (event) => {
        event.preventDefault();

        const current = document.querySelectorAll('#product').length;

            $.ajax({
                type: 'GET',
                data: {
                    'current': current,
                },
                beforeSend: function () {
                    loadMoreBtn.style.display = 'none';
                },
                success: function (response) {
                    loadMoreBtn.style.display = 'block';
                    $("#productsHolder").append(response[0]);
                },
                error: function (err) {
                    console.log(err)
                    alert("Couldn't load next products. Please, try again");
                    loadMoreBtn.style.display = 'block'
                }
            })
    })

}

$( document ).ready(function () {

    $.ajax({
    type: 'GET',
    data: {
        'current': 0,
    },
    success: function (response) {
        $("#productsHolder").append(response[0]);
        if (response.length > 1) {
            document.getElementById("productsCount").textContent = `Showing 1 to 16 of ${response[1]} total`;
        }

    },
    error: function (err) {
        console.log(err)
        alert("Couldn't load products. Please, refresh the page.");
    }
})

})

function navigatePrice(ev) {
    const priceIdForSpan = ev.target.parentNode.getAttribute("data-value");
    const priceSpanToDisplay = document.getElementById(priceIdForSpan);
    const priceSpans = [...priceSpanToDisplay.parentNode.children];

    priceSpans.forEach(span => {
        span.style.display = 'none';
    })

    priceSpanToDisplay.style.display = 'block';
}

function categorySubMenu() {
    const subMenus = [...document.getElementsByClassName("submenu")];
    subMenus.forEach(subMenu => {
        if (subMenu.children.length > 15) {
            subMenu.style.overflowY = 'auto';
            subMenu.style.maxHeight = '25.5em';
        }
    })
}

loadMore();

categorySubMenu();