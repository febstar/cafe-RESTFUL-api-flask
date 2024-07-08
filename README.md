# Cafe API

Welcome to the Cafe API project! This is a Flask-based web application that provides a simple and convenient way to manage a database of cafes. You can perform CRUD (Create, Read, Update, Delete) operations on cafes, search for cafes by location, and get random cafe recommendations.

## Features

- **Create**: Add a new cafe to the database with various attributes like name, location, amenities, and coffee price.
- **Read**: Retrieve details of all cafes, search for cafes by location, or get a random cafe recommendation.
- **Update**: Update the coffee price of a specific cafe by its ID.
- **Delete**: Delete a cafe from the database by its ID, with proper authorization.

## Endpoints

### Home
- `GET /`: Renders the homepage.

### Cafe Operations
- `GET /random`: Get a random cafe's details.
- `GET /all`: Retrieve details of all cafes.
- `GET /search?loc=<location>`: Search for cafes by location.
- `POST /add`: Add a new cafe.
- `PATCH /update-price/<int:id>`: Update the coffee price of a cafe by its ID.
- `DELETE /reported-closed/<int:id>?api-key=<api_key>`: Delete a cafe by its ID with proper authorization.

## Data Model

The cafe data model includes:
- `id`: Unique identifier for the cafe.
- `name`: Name of the cafe.
- `map_url`: URL to the cafe's location on the map.
- `img_url`: URL to an image of the cafe.
- `location`: Location of the cafe.
- `seats`: Number of seats available.
- `has_toilet`: Whether the cafe has a toilet (boolean).
- `has_wifi`: Whether the cafe has WiFi (boolean).
- `has_sockets`: Whether the cafe has power sockets (boolean).
- `can_take_calls`: Whether phone calls can be taken in the cafe (boolean).
- `coffee_price`: Price of coffee at the cafe.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/cafe-api.git
    cd cafe-api
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the database:
    ```bash
    flask db init
    flask db migrate
    flask db upgrade
    ```

5. Run the application:
    ```bash
    flask run
    ```

## Usage

You can interact with the API using tools like Postman or cURL. Below are some example requests:

- **Add a new cafe**:
    ```bash
    curl -X POST -F "name=Test Cafe" -F "map_url=http://map.url" -F "img_url=http://image.url" -F "loc=Test Location" -F "seats=20" -F "sockets=True" -F "toilet=True" -F "wifi=True" -F "calls=True" -F "coffee_price=$2.50" http://127.0.0.1:5000/add
    ```

- **Get all cafes**:
    ```bash
    curl http://127.0.0.1:5000/all
    ```

- **Search for cafes by location**:
    ```bash
    curl http://127.0.0.1:5000/search?loc=Test%20Location
    ```

- **Update a cafe's coffee price**:
    ```bash
    curl -X PATCH -d "new_price=$3.00" http://127.0.0.1:5000/update-price/1
    ```

- **Delete a cafe**:
    ```bash
    curl -X DELETE "http://127.0.0.1:5000/reported-closed/1?api-key=TopSecretAPIKey"
    ```

## Contributing

Feel free to fork the repository and submit pull requests. Any improvements or bug fixes are welcome.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
