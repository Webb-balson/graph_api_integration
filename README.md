<!-- 
This README file provides an overview and instructions for the `graph_api_integration` project. 
It is intended to guide users on how to set up, configure, and use the integration with the Graph API.
-->
# graph_api_integration

## Setup Instructions

### Installing Dependencies
1. Clone the repository
    ```bash
    git clone git@github.com:Webb-balson/graph_api_integration.git
    ```
2. Navigate to the project directory:
    ```bash
    cd graph_api_integration
    ```
3. Ensure you have Python 3.8 or higher installed.
4. Create a virtual environment by running:
    ```bash
    python3 -m venv venv
    ```
5. Activate the virtual environment:
        ```bash
        source venv/bin/activate
        ```
6. Install the required dependencies by running:
    ```bash
    pip3 install -r requirements.txt
    ```

### Setting Up Environment Variables
1. Create a `.env` file in the project root directory.
2. Add the following variables to the `.env` file:
    ```env
    CLIENT_ID=<your-client-id>
    CLIENT_SECRET=<your-client-secret>
    TENANT_ID=<your-tenant-id>
    USER_EMAIL=<your-mail-id>
    ```

### Running the Service
1. Navigate to the project directory:
    ```bash
    cd app
    ```
2. Start the service by executing:
    ```bash
    python3 app.py
    ```
3. Access the service at `http://localhost:8000` (or the configured host and port).
4. Access the swagger UI at `http://localhost:8000/docs`.

## Approach to Scheduling
The project uses a scheduling mechanism to handle tasks like fetching emails at specific interval. This is achieved using Python's `APSchedule` library . The scheduler runs in the background and periodically checks for emails and also persists then in MongoDB.

## API Structure
The API is designed with a RESTful architecture, making it intuitive and easy to use. Key endpoints include:
- **GET /**: Root endpoint, can also be used to healthcheck of the service.
- **POST /send-email**: Allows users to send an email immediately by providing the necessary details (e.g., recipient, subject, body).
- **GET /fetch-emails**: Lists all emails arrived in last 24 hours.

The API is documented using Swagger, which provides an interactive UI for testing and understanding the endpoints.

## Testing Email Functionality
To test the email-sending and retrieval features:
1. Start the application and access the Swagger UI at `http://localhost:8000/docs`.
2. Use the **POST /send-email** endpoint to send a test email. Provide the required fields (e.g., recipient email, subject, and body) in the request payload.
3. Use the **GET /fetch-emails** endpoint to retrieve a list of all emails.

By following these steps, you can ensure that the email functionality works as expected and handles both immediate and scheduled email tasks effectively.

## How I Used AI Coding Tools

In this project, I utilized AI coding tools like ChatGPT and GitHub Copilot to streamline development and improve productivity. These tools assisted in various aspects of the project, including:

- **Code Generation**: AI tools helped generate boilerplate code for setting up the API endpoints and integrating with the Graph API.
- **Debugging**: By providing detailed explanations and suggestions, the tools assisted in identifying and resolving issues in the codebase.
- **Test Creation**: AI tools were instrumental in drafting unit tests and integration tests to ensure the reliability of the application.
- **Documentation**: The README file and other documentation were enhanced with the help of AI tools, ensuring clarity and completeness for end-users.

These tools significantly reduced development time and allowed me to focus on implementing core features effectively.

P.S - I used Github Copilot to generate the complete README file :)
