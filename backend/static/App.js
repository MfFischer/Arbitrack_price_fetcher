// frontend/app.js

document.getElementById("fetch-btn").addEventListener("click", async () => {
  const apiKey = document.getElementById("api-key").value;
  const subgraphId1 = document.getElementById("subgraph-id1").value;
  const subgraphId2 = document.getElementById("subgraph-id2").value;
  const token1 = document.getElementById("token1").value;
  const token2 = document.getElementById("token2").value;
  const feeTier = document.getElementById("fee-tier").value || null;

  const resultsContainer = document.getElementById("results");
  resultsContainer.innerHTML = "<p>Loading...</p>";

  try {
    // Use relative URL to connect to the backend
    const response = await fetch("/fetch-prices", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ apiKey, subgraphId1, subgraphId2, token1, token2, feeTier }),
    });

    if (!response.ok) {
      throw new Error(`Server error: ${response.statusText}`);
    }

    const results = await response.json();
    resultsContainer.innerHTML = ""; // Clear loading message

    if (results.length === 0) {
      resultsContainer.innerHTML = "<p>No results found.</p>";
      return;
    }

    results.forEach((result) => {
      const resultBox = document.createElement("div");
      resultBox.className = "result-box";
      resultBox.innerHTML = `
        <p><strong>Pool ID:</strong> ${result.pool_id}</p>
        <p><strong>Token0:</strong> ${result.token0}</p>
        <p><strong>Token1:</strong> ${result.token1}</p>
        <p><strong>Exchange1 Price:</strong> ${result.exchange1_price}</p>
        <p><strong>Exchange2 Price:</strong> ${result.exchange2_price}</p>
        <p><strong>Liquidity:</strong> ${result.liquidity}</p>
        <p><strong>Fee Tier:</strong> ${result.feeTier}</p>
        <p><strong>Price Difference %:</strong> ${result.price_difference_percentage}</p>
        <p><strong>Buy on Exchange:</strong> ${result.buy_on_exchange}</p>
      `;
      resultsContainer.appendChild(resultBox);
    });
  } catch (error) {
    resultsContainer.innerHTML = `<p>Error: ${error.message}</p>`;
  }
});

// Toggle API Key Visibility
document.getElementById("toggle-api-key").addEventListener("click", () => {
  const apiKeyInput = document.getElementById("api-key");
  const toggleIcon = document.getElementById("toggle-api-key");

  if (apiKeyInput.type === "password") {
    apiKeyInput.type = "text";
    toggleIcon.classList.remove("fa-eye");
    toggleIcon.classList.add("fa-eye-slash");
  } else {
    apiKeyInput.type = "password";
    toggleIcon.classList.remove("fa-eye-slash");
    toggleIcon.classList.add("fa-eye");
  }
});
