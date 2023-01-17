//<!-- JavaScript Bundle with Popper -->
src =
  "https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js";
integrity =
  "sha384-kenU1KFdBIe4zVF0s0G1M5b4hcpxyD9F7jL+jjXkk+Q2h455rYXK/7HAuoJl+0I4";
crossorigin = "anonymous";

//<!-- dropdown menu -->
document.getElementsByClassName("fa")[3].addEventListener("click", function () {
  document.getElementsByClassName("links")[0].classList.toggle("showmylinks");
});

//<!-- fix navbar to the top -->
document.addEventListener("DOMContentLoaded", function () {
  window.addEventListener("scroll", function () {
    if (window.scrollY > 0) {
      document.getElementById("mynavbarmainid").classList.add("fixed-top");
      // add padding top to show content behind navbar
      navbar_height = document.querySelector(".mynavbarmain").offsetHeight;
      document.body.style.paddingTop = navbar_height + "px";
    } else {
      document.getElementById("mynavbarmainid").classList.remove("fixed-top");
      // remove padding top from body
      document.body.style.paddingTop = "0";
    }
  });
});

//<!-- cart -->
var updateBtns = document.getElementsByClassName("update-cart");

for (i = 0; i < updateBtns.length; i++) {
  updateBtns[i].addEventListener("click", function () {
    var productId = this.dataset.product;
    var action = this.dataset.action;
    console.log("productId: ", productId, "action: ", action);

    console.log("USER: ", user);
    if (user == "AnonymousUser") {
      console.log("Not logged in");
      addCookieItem(productId, action);
    } else {
      updateUserOrder(productId, action);
    }
  });
}

function addCookieItem(productId, action) {
  console.log("User is not authenticated");

  if (action == "add") {
    if (cart[productId] == undefined) {
      cart[productId] = { quantity: 1 };
    } else {
      cart[productId]["quantity"] += 1;
    }
  }

  if (action == "remove") {
    cart[productId]["quantity"] -= 1;

    if (cart[productId]["quantity"] <= 0) {
      console.log("Iyem should be deleted");
      delete cart[productId];
    }
  }

  console.log("Cart: ", cart);
  document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/";
  location.reload();
}

function updateUserOrder(productId, action) {
  console.log("User is authenticated, sending data...");

  var url = "/update_item/";

  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ productId: productId, action: action }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      console.log("Data: ", data);
      location.reload();
    });
}

//<!-- checkout -->
document
  .getElementById("make-payment-atcounter")
  .addEventListener("click", function (e) {
    submitFormData();
  });

function submitFormData() {
  console.log("Payment button clicked");

  var userFormData = {
    name: null,
    email: null,
    total: total,
  };

  var url = "/process_order/";
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ form: userFormData }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Success:", data);
      alert("Transaction completed");

      cart = {};
      document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/";

      window.location.href = home;
    });
}

//<!-- show or hide customer order history -->
function show_or_hide_customer_order_history() {
  var x = document.getElementById("customer_order_history");
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}
