//<!-- order queue -->
var updateOrderItemBtns = document.getElementsByClassName("update-order-item");

for (i = 0; i < updateOrderItemBtns.length; i++) {
  updateOrderItemBtns[i].addEventListener("click", function () {
    var orderItemId = this.dataset.orderitem;
    var action = this.dataset.action;
    console.log("orderItemId: ", orderItemId, "action: ", action);

    console.log("USER: ", user);
    if (user == "AnonymouseUser") {
      console.log("User is not authenticated");
    } else {
      updateUserOrder(orderItemId, action);
    }
  });
}

function updateUserOrder(orderItemId, action) {
  console.log("User is authenticated, sending data...");

  var url = "/update_order_item/";

  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({
      orderItemId: orderItemId,
      action: action,
    }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      console.log("Data: ", data);
      location.reload();
    });
}
