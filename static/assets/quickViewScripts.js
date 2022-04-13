function quickView(ev) {
    let tabContent = ev.target.parentNode.parentNode.parentNode;
    let activeImg = tabContent.querySelector('div > .active');
    if (activeImg == null) {
        tabContent = tabContent.parentNode;
        activeImg = tabContent.querySelector('div > .active');
    }
    let productInventorySku = activeImg.id.replace("ptab1_", "");
    const productInventoryPrice = document.querySelector(`#priceId${productInventorySku}`).querySelector('strong').textContent;
    const imgUrl = activeImg.querySelector('img').src;
    const description = tabContent.querySelector('input[name="product_description"]').value;
    const categories = [...tabContent.querySelectorAll('a[class="product_category_links"]')];
    const productName = tabContent.querySelector('input[name="product_name"]').value;

    const quickViewDiv = document.querySelector('#quickview_modal');
    let quickViewImg = quickViewDiv.querySelector('div > .item_image').querySelector('img');
    let quickViewPrice = quickViewDiv.querySelector('#quickViewPrice');
    let quickViewCategoriesLi = quickViewDiv.querySelector('#quickViewCategories');
    let quickViewDescription = quickViewDiv.querySelector('#quickViewDescription');
    let quickViewProductName = quickViewDiv.querySelector('#quickViewProductName');

    quickViewImg.src = imgUrl;
    quickViewPrice.textContent = productInventoryPrice;
    quickViewCategoriesLi.innerHTML = '';
    quickViewCategoriesLi.innerHTML += '<strong class="list_title">Category:</strong>'
    for (let i = 0; i < categories.length; i++) {
        let a = document.createElement('a');
        a.href = categories[i].href;
        a.textContent = categories[i].textContent;
        quickViewCategoriesLi.append(a);
    }
    quickViewDescription.textContent = description;
    quickViewProductName.textContent = productName;


    $.ajax({
        type: 'GET',
        data: {
            'get_variants_etc': productInventorySku
        },
        success: function (response) {
            document.getElementById("quickViewSizes").innerHTML = response;
        },
        error: function (err) {
            alert("Couldn't load product sizes, please try again.");
            console.log(err);
        }
    })

}