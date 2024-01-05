# Online Banking App

#### Video Demo: [https://youtu.be/9gXuXxRZmAA]

#### Description

The Online Banking App stands as a sophisticated and robust Flask-based web application, meticulously designed to seamlessly manage an extensive array of user-related functionalities, encompassing everything from intricate account management to precise transaction handling and an array of account-related activities. This advanced platform is not just a tool; it's an empowerment mechanism that enables users to effortlessly navigate through a spectrum of financial actions. From the initial steps of signing up and logging in to the more nuanced processes of perusing intricate account details, conducting seamless deposits and withdrawals, and meticulously reviewing transaction history, every facet of the user experience is carefully considered and intuitively implemented.

At its core, the application is a testament to meticulous craftsmanship, with Python serving as the foundational programming language. This choice not only speaks to the language's versatility but also to its efficiency in delivering a seamless and responsive user experience. Behind the scenes, a potent SQLite backend takes center stage, ensuring not only the efficiency but also the security and integrity of the underlying database management. This robust combination of technologies creates a synergy that allows the Online Banking App to handle user data with precision and safeguard sensitive information with the utmost reliability.

As users engage with the platform, the intuitive interface guides them through a journey that seamlessly blends functionality and accessibility. The application's responsiveness ensures a consistent and enjoyable experience across devices, while its sophisticated features, such as real-time updates on account balances and comprehensive transaction histories, provide users with a comprehensive view of their financial landscape.

Looking ahead, the Online Banking App is not just a static solution; it's a dynamic entity poised for continuous evolution. With a commitment to ongoing enhancements and the integration of advanced features, the application sets its sights on not just meeting but exceeding user expectations. Its role extends beyond a mere tool for financial transactions; it emerges as a trusted companion in users' financial journeys, providing a secure, efficient, and feature-rich environment for all their banking needs.

## Files

- `app.py`: Main script containing the Flask application setup.
- `models.py`: Script containing database models and functions for user and transaction handling.
- `views.py`: Script containing Flask routes and views for the web application.
- `requirements.txt`: The file which contains the list of required libraries to be installed before running the script.
- `templates/`: Folder containing HTML templates for the web application.
- `static/`: Folder containing static files like CSS and images for the web application.
- `README.md`: The file that explains the project.

## Project Requirements

- The project is implemented using Flask (Python web framework) and SQLite for database management.
- The Flask library should be installed before running the code.
- The project has a modular structure with separate files for application setup (`app.py`), database models (`models.py`), and routes/views (`views.py`).
- Key functionalities include user authentication, account management, transactions, and a simple user interface using HTML templates.
- The code follows the Flask naming convention for routes and views.
- Additional libraries or tools, such as Flask-WTF for form handling, can be added as needed.

## Usage

1. Navigate to the project directory.
2. Install the required dependencies using pip: `pip install -r requirements.txt`
3. Run the Flask application by executing `app.py` in the terminal: `python app.py`
4. Access the application in a web browser at `http://127.0.0.1:5000/`.
5. Follow the prompts to interact with the Online Banking App.


## Acknowledgments

- Flask: [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)
- SQLite: [https://www.sqlite.org/index.html](https://www.sqlite.org/index.html)
