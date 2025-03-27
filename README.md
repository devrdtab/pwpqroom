# E2E Test Automation for q-room.com

This repository contains automated **End-to-End (E2E)** tests for [q-room.com](https://q-room.com), written using **Playwright**, **Pytest**, and **Allure**.

## 📌 Tech Stack

- [Playwright](https://playwright.dev/python/) – Browser testing  
- [Pytest](https://pytest.org/) – Test framework  
- [Allure](https://docs.qameta.io/allure/) – Report generation  

## 📦 Installation

1. **Clone the repository:**
   ```sh
   git https://github.com/devrdtab/pwpqroom.git
   ```

2. **Create a virtual environment:**
   ```sh
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate  # Windows
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers:**
   ```sh
   playwright install
   ```

## 🚀 Running Tests

### Run all tests:
```sh
pytest -s -v
```

### Run tests with Allure reports:
```sh
pytest --alluredir=allure-results
```

### Generate and view the Allure report:
```sh
allure serve allure-results
```

## ⚙️ Project Structure
```
qroom/
│-- .github/               # GitHub Actions
│-- pages/                 # Page Object Model (POM)
│-- tests/                 # Test scenarios
│-- utils/                 # Constants and data
│-- conftest.py            # Pytest fixtures
│-- requirements.txt       # Dependencies list
│-- README.md              # Project documentation
```

## 🔧 Configuration (Environment Variables)
To manage sensitive data, use the **constants.py** file. Example:
```python
BASE_URL = "https://q-room.com"
```

## 📊 Reports
All test results can be viewed [here](https://devrdtab.github.io/pwpqroom/).

## 📩 Contact
[devrdtab@gmail.com](mailto:devrdtab@gmail.com)
