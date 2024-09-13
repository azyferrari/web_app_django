# Bank Comparison Web App

## Overview

This project is a Django-based web application designed to visualize company data in order to compare and analyze banks across various financial metrics. The app uses Django, Django REST Framework, Chart.js, and Redis for caching. It provides charts that allow users to compare banks based on ownership share, historical financials, historical valuation, market capitalization, and employee numbers.

## Features

- **Data Visualization:** Displays charts comparing different banks based on ownership share, historical financials, historical valuation, market cap, and employee numbers.
- **Caching:** Utilizes Redis for caching data to improve performance.
- **Data Source Integration:** Fetches data from an API, processes it, and stores it in an SQLite3 database.

## Technologies Used

- **Django:** Web framework for developing the web application.
- **Django REST Framework:** To build the RESTful API endpoints.
- **Chart.js:** For rendering interactive charts.
- **Redis:** Caching data to optimize performance.
- **SQLite3:** Database to store the processed data.


## Database Tables

1. **viz_historical_financials**
2. **viz_historical_valuation**
3. **viz_ownership**
4. **viz_overview**

## Setup and Installation

1. **Clone the repository:**

    ```bash
    git clone  https://github.com/azyferrari/web_app_django.git
    cd data_banks
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run migrations:**

    ```bash
    python manage.py migrate
    ```

5. **Load initial data:**
   
    - Fetch data from the API and generate CSV files:
    
        ```bash
        python getdata_historicalfinancial.py
        python getdata_historicalvaluation.py
        python getdata_overview.py
        python getdata_ownership.py
        ```

    - Import data into the database:
    
        ```bash
        python manage.py runscript viz.import_data -v2
        ```

6. **Run the development server:**

    ```bash
    python manage.py runserver
    ```

7. **Access the web app:**

    Open your web browser and go to `http://127.0.0.1:8000/login/`.



## Usage

- **Visualize Data:** Navigate to the visualization page to view interactive charts comparing banks.
- **Compare Banks:** Use the provided charts to analyze and compare banks based on different financial metrics.

## Caching

Redis is used to cache data and improve the performance of the web application. Make sure Redis is running on your system. Update the Redis configuration in `settings.py` if necessary.

## Contributing

If you want to contribute to this project, please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/azyferrari/web_app_django?tab=MIT-1-ov-file) file for details.

---

Enjoy using the Bank Comparison Web App!
