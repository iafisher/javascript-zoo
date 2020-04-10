export async function api(url, payload) {
  console.log("Posting data to " + url, payload);
  const options = {
    method: "POST",
    headers: {
      "Accept": "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  };
  const response = await fetch(url, options);
  return await response.json();
}
