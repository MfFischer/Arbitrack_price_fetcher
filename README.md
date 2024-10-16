# 🔍 Token Arbitrage Tracker

<img src="./images/token%20arb.png" alt="Token Arbitrage Dashboard" width="800"/>

"Token Arbitrage Tracker Dashboard"

---

## 📖 Table of Contents
- [About the Project](#about-the-project)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Deployment](#deployment)
- [License](#license)
- [Contact](#contact)

---

## 📝 About the Project
The **Token Arbitrage Tracker** is designed to help users track token prices across multiple exchanges to identify potential arbitrage opportunities. With a simple interface, you can monitor token prices, view liquidity, and detect profitable trades by fetching and comparing prices from different subgraphs.

---

## ✨ Features
- **Token Price Comparison:** Fetch token prices from two exchanges.
- **Arbitrage Detection:** Analyze price differences and detect potential arbitrage opportunities.
- **User-Friendly Interface:** Responsive design for a smooth experience on any device.
- **Data Security:** Securely input and toggle visibility of your API keys.

---

## 🚀 Getting Started

### Prerequisites
Ensure you have the following installed:
- Node.js and npm
- Flask (for the backend)
- Python 3.8+
- An API key for The Graph

### Installation
1. **Clone the Repository:**
   ```bash
   git clone  https://github.com/MfFischer/Arbitrack_price_fetcher.git
   cd token-arbitrage-tracker

2. **Backend Setup:**
   Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

   Install dependencies:
   ```bash
   pip install -r requirements.txt

3. **Frontend Setup:**
    Install Node dependencies:
   ```bash
   npm install
### Running the Application
  Start the App:
  ```bash
   python backend/app.py

    Once the application is running, navigate to http://127.0.0.1:5000 in your browser.

## 📊 Usage
- **Dashboard:** View token prices and track arbitrage opportunities in real time.
- **Price Comparison**: Input token addresses and subgraph IDs for exchanges to compare prices.
- **API Key Security**: Securely input and toggle visibility of your API keys with the eye icon.

## 📜 License
Distributed under the MIT License. See LICENSE for more information.

## 📬 Contact
Maria Fe Fischer - afefischer@gmail.com
  

