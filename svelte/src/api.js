export async function api(url, payload) {
  console.log("Posting data to " + url, payload);
  // Django requires a server-generated CSRF token to be included with all POST
  // requests.
  const csrf = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
  const options = {
    method: "POST",
    headers: {
      "Accept": "application/json",
      "Content-Type": "application/json",
      "X-CSRFToken": csrf,
    },
    body: JSON.stringify(payload),
  };
  const response = await fetch(url, options);
  return await response.json();
}
