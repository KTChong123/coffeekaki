// This is your test publishable API key.
const stripe = Stripe(
  "pk_test_51MPJyGKgVq5fGvtgqHeVgLCwQA9Gc7JZ0AxkNqXW4upgeJJsh5rtc1IDl8rcxoOzmyg5TJKvVPXBrnBTRip3TAkc00O4fLA8C1"
);

const elements = stripe.elements();
const cardElement = elements.create("card");
cardElement.mount("#card-element");

// The items the customer wants to buy
var purchase = {
  items: [{ id: "xl-tshirt" }],
};

async function initializePayment() {
  var url = "/stripe-card-payment/";
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
  });
  const data = await response.json();
  return data;
}

async function confirmPayment(clientSecret) {
  const result = await stripe.confirmCardPayment(clientSecret, {
    payment_method: {
      card: cardElement,
    },
  });
  if (result.error) {
    console.error(result.error);
    const { message } = result.error;
    console.log(message);
    const errorMessage = "Payment unsuccessful. " + message;
    alert(errorMessage);
  } else {
    submitOrder();
    alert(
      "Payment successful and order received. We will be serving you shortly. Thank you."
    );
    window.location.href = home;
  }
}

function submitOrder() {
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

      cart = {};
      document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/";

      window.location.href = home;
    });
}

document
  .getElementById("stripe-card-pay-button")
  .addEventListener("click", async () => {
    const { clientSecret } = await initializePayment();
    console.log("Ready to initialize payment");
    console.log(clientSecret);
    confirmPayment(clientSecret);
  });
