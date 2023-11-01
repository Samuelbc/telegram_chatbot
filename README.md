# README for Telegram Chatbot
### Introduction
This project is a Telegram chatbot designed to provide a seamless interaction for users. The bot uses the GPT-4 model to generate responses, and the user data is stored in a MySQL database.

Project Structure

```
telegram_chatbot/
|-- bot/
|   |-- __init__.py
|   |-- main.py
|   |-- handlers/
|   |   |-- __init__.py
|   |   |-- command.py
|   |   |-- gptconnection.py
|   |   |-- message.py
|-- db/
|   |-- __init__.py
|   |-- database.py
|-- .env
|-- .gitignore
|-- Pipfile
|-- Pipfile.lock
```
### Prerequisites
* Python 3.8 or higher
* MySQL Server
* pipenv (for dependency management)
  
### Setup & Installation
* Clone the repository from GitHub.
* Navigate to the root directory of the project.

#### Install the necessary dependencies using pipenv:
* bash
* Copy code
* pipenv install
* Set up your MySQL server and create a database.
### Update the .env file with the required database configurations:
```
DB_HOST=<your_database_host>
DB_USER=<your_database_user>
DB_PASS=<your_database_password>
DB_NAME=<your_database_name>
BOT_USERNAME=<your_telegram_bot_username>
GPT_API_KEY=<your_gpt_api_key>
```
Ensure your MySQL server is running.
### Running the Bot
To execute the bot locally, run the following command from the root directory:
* pipenv run python -m bot.main
  
### Contributing
If you would like to contribute to this project, please fork the repository, make your changes, and create a pull request. Ensure that your code is well-documented.

License
This project is licensed under the MIT License. See the LICENSE file for details.
