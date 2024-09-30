# Expected Traffic Estimation API

## Overview
This API estimates the expected traffic count based on given targeting criteria including countries, platforms, verticals, browsers, and total requests.

## Installation Instructions
1. **Clone the Repository**:
     ```sh
     git clone https://github.com/sahamsiddiqui/restAPI.git

     ```

3. **Navigate to the Project Directory**:
   - Open a terminal or command prompt and navigate to the project directory.

4. **Create and Activate a Virtual Environment**:
   - Create a virtual environment:
     ```sh
     python -m venv venv
     ```
   - Activate the virtual environment:
     - On Windows:
       ```sh
       .\venv\Scripts\activate
       ```
     - On macOS and Linux:
       ```sh
       source venv/bin/activate
       ```

5. **Install the Required Packages**:
   - Run the following command to install the necessary dependencies:
     ```sh
     pip install -r requirements.txt
     ```

## Usage Instructions
1. **Run the Flask App**:
   - Execute the following command to start the Flask application:
     ```sh
     python app.py
     ```

2. **Access the API**:
   - You can access the API via your web browser using the following URL format:
     ```
     http://127.0.0.1:5000/calculate/<countries>/<platforms>/<verticals>/<browsers>/<total_requests>
     ```
   - Example:
     ```
     http://127.0.0.1:5000/calculate/us,ca/windows,mac/finance,entertainment/chrome,firefox/1000000
     ```

## Configuration
Ensure that the `data` directory within the project folder contains the following CSV files:
- `countries.csv`
- `platformname.csv`
- `vertical.csv`
- `browsername.csv`

These CSV files should have the columns `country`, `platform`, `vertical`, and `browser` respectively along with their average_opportunities column .


