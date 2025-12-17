# ShortCat - TUI (Text User Interface) 🐱🖥️

Welcome to the **ShortCat TUI**! This command-line interface allows you to interact with the URL shortening service directly from your terminal, without needing a browser or mobile app.

The TUI provides an essential and fast experience for managing your account and links by communicating via API with the ShortCat Backend.

---

## ✨ Features

Through an interactive text-based menu, you can perform all main operations:

* **Authentication:**
    * 🔐 Login (Access with username and password).
    * 📝 Sign Up (New user registration).
    * 🚪 Logout.
* **Short Link Management:**
    * ➕ **Create:** Input a long URL and get a short code.
    * 👀 **View:** List all your active links.
    * ✏️ **Edit:** Change the destination or link settings.
    * ❌ **Delete:** Remove links you no longer need.

---

## ⚠️ Fundamental Prerequisites

The TUI is just a "client". **For it to work, the ShortCat Backend server must be running.**

Before starting, make sure you have configured and started the Backend.
📖 **Read the Backend documentation here:** [shortcat-ssd/backend](https://github.com/shortcat-ssd/backend)

### ⚙️ Backend Configuration (.env)
For the TUI to communicate correctly with the server, you need to configure Django's security policies.

In the **Backend's** `.env` file, ensure that the `DJANGO_ALLOWED_HOSTS` variable includes the IP address of the machine running the TUI (in addition to localhost).

Copy and paste this configuration into the backend's `.env`:

```env
DJANGO_ALLOWED_HOSTS=localhost,0.0.0.0,127.0.0.1,192.168.1.2,8080,172.20.10.2,YOUR_LOCAL_IP

```

*(Replace `YOUR_LOCAL_IP` with your machine's IP address if it differs from those listed).*

---

## 🧪 Development Methodology: Test First

This project was developed strictly following the **TDD (Test Driven Development)** approach, or "Test First, Code Later".

This means that every single feature (API calls, error handling, input logic) was defined via an automated test first and implemented in the code afterwards. This guarantees:

1. **Robustness:** The code does exactly what it is supposed to do.
2. **Reliability:** Backend calls are verified and handled correctly.
3. **Documentation:** The tests themselves serve as technical documentation of the expected behavior.

---

## 🚀 Installation and Usage

### 1. Clone the Repository

The TUI code resides in the same repository as the backend. Clone it using:

```bash
git clone [https://github.com/shortcat-ssd/backend.git](https://github.com/shortcat-ssd/backend.git)
cd backend

```

### 2. Dependency Management with Poetry

We use **Poetry** for dependency and virtual environment management.

* **Install Poetry** (if you haven't already):
[Follow the official guide](https://www.google.com/search?q=https://python-poetry.org/docs/%23installation)
* **Install Project Dependencies:**
Inside the project folder, run:
```bash
poetry install

```


*This will automatically install all necessary libraries (requests, pytest, coverage, etc.) in an isolated environment.*

### 3. Run the TUI

Ensure the backend server is running in another terminal window. Then start the text interface:

```bash
poetry run python tui_main.py

```

*(Note: Replace `tui_main.py` with the exact filename of your TUI entry point if different).*

---

## 📊 Testing and Coverage

Thanks to the Test First approach, you can verify the integrity of the code at any time.

### Run Tests (Pytest)

To launch the automated test suite and verify that all API calls work as expected:

```bash
poetry run pytest

```

### View Code Coverage

To see what percentage of the code is covered by tests (it should be very high given the TDD approach):

1. **Run tests with coverage calculation:**
```bash
poetry run pytest --cov=.

```


2. **Generate a detailed HTML report (optional):**
```bash
poetry run pytest --cov=. --cov-report=html

```


Then open the `htmlcov/index.html` file in your browser to see line-by-line what has been tested.

---

## 📝 License
This project was developed for educational purposes.

**ShortCat Team** - *Short links, big impact (via terminal).*
