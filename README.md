# Location-Based Restaurant and Museum Finder API

This project provides a Flask-based API to help users find the nearest restaurants and museums based on their geographical location and the current time. The API uses the Haversine formula to calculate distances and includes endpoints to retrieve restaurant menus and museum information.

## Project Overview

The API serves two main functionalities:
1. **Finding the Nearest Restaurant**: Users can obtain the nearest restaurant's menu based on their location and the time of day.
2. **Finding the Nearest Museum**: Users can find the nearest museum, its opening status, and additional information based on their location and the time of day.

### API Endpoints

1. **Get Menu Based on Location and Time**
   - **Endpoint**: `/qrapi/get_menu`
   - **Method**: `GET`
   - **Parameters**:
     - `latitude` (float): Latitude of the user's location.
     - `longitude` (float): Longitude of the user's location.
     - `time` (string): Current time in the format "HH:MM".
   - **Response**: Returns the nearest restaurant's name, location, menu type, and corresponding menu items.
   - **Example Request**:
     ```
     GET /qrapi/get_menu?latitude=12.9716&longitude=77.5946&time=13:00
     ```

2. **Get Nearest Museum Information**
   - **Endpoint**: `/qrapi/nearest_museum`
   - **Method**: `GET`
   - **Parameters**:
     - `latitude` (float): Latitude of the user's location.
     - `longitude` (float): Longitude of the user's location.
     - `time` (string): Current time in the format "HH:MM".
   - **Response**: Returns the nearest museum's name, address, description, opening status, opening and closing times, and entrance fee.
   - **Example Request**:
     ```
     GET /qrapi/nearest_museum?latitude=12.9716&longitude=77.5946&time=13:00
     ```

### Project Files

- **museums.json**: Contains data about various museums, including their location, opening times, and entrance fees.
- **restaurants.json**: Contains data about various restaurants, including their menus and locations.

### Installation and Usage

To set up and run the project locally, follow these steps:

1. **Clone the repository** (or download the project files).
2. **Install required dependencies**:
   ```bash
   pip install Flask flask-cors
   ```

3. **Run the Flask application**:
   ```bash
   python app.py
   ```

4. **Access the API**: Open your web browser or API testing tool (like Postman) to interact with the API endpoints:
   - For restaurant menu: `http://127.0.0.1:5000/qrapi/get_menu?latitude=<lat>&longitude=<lon>&time=<time>`
   - For nearest museum: `http://127.0.0.1:5000/qrapi/nearest_museum?latitude=<lat>&longitude=<lon>&time=<time>`

### Technologies Used

- **Flask**: Web framework for building the API.
- **Flask-CORS**: For handling Cross-Origin Resource Sharing.
- **Python**: Programming language used for the API development.
- **JSON**: Data format for storing restaurant and museum information.

## Acknowledgments

- Special thanks to the creators of the datasets used in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
