from bank_app import create_app

# Create an instance of the Flask application using the create_app function
app = create_app()

if __name__ == "__main__":
    # Run the application in debug mode
    app.run(debug=True)
