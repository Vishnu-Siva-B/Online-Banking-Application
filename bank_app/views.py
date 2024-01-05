# Importing necessary libraries
import re
import sqlite3
from .models import *
from datetime import datetime
from flask import Blueprint, render_template, redirect, request, url_for, session, flash

# Creating a Blueprint for views
views = Blueprint(
    "views", __name__, static_folder="static", template_folder="templates"
)

# Creating user table and transaction table if they don't exist
create_user_table()
create_transaction_table()


@views.route("/")
def home():
    """
    Renders the home page.

    Returns:
    - HTML template for the home page
    """
    return render_template("1_home.html")


@views.route("/signIn", methods=["GET", "POST"])
def signIn():
    """
    Handles user sign-in.

    Returns:
    - If successful, redirects to userHome.
    - If unsuccessful, shows the sign-in form.
    """
    if request.method == "POST":
        accNo = request.form.get("accNo")
        password = request.form.get("password")

        # Check if the account number and password match
        if verify_credentials(accNo, password):
            session["accNo"] = accNo
            flash("You have logged in successfully", "success")
            return redirect(url_for("views.userHome"))
        else:
            flash("Invalid account number or password", "danger")

    # If not a POST request or login fails, show the sign-in form
    if "accNo" in session:
        flash("You already logged in", "success")
        return redirect(url_for("views.userHome"))
    else:
        return render_template("2_signIn.html")


@views.route("/signUp", methods=["GET", "POST"])
def signUp():
    """
    Handles user sign-up.

    Returns:
    - If successful, redirects to signIn.
    - If unsuccessful, shows the sign-up form with appropriate error messages.
    """
    if "accNo" in session:
        an = session["accNo"]
    if request.method == "POST":
        session["firstName"] = request.form.get("firstName").strip()
        session["lastName"] = request.form.get("lastName").strip()
        session["accNo"] = request.form.get("accNo").strip()
        session["email"] = request.form.get("email").strip()
        session["city"] = request.form.get("city").strip()
        session["state"] = request.form.get("state").strip()
        session["country"] = request.form.get("country").strip()
        session["password"] = request.form.get("password").strip()
        session["conPassword"] = request.form.get("conPassword").strip()

        re_accNo = r"^[0-9]{10}$"
        re_email = r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"

        er = 0
        errors = []

        if not re.match(re_accNo, session["accNo"]):
            errors.append(
                "Invalid Account Number !! \n Account Number should be of 10 digits"
            )
            session.pop("accNo", None)

        if not re.match(re_email, session["email"]):
            errors.append("Invalid Email")
            session.pop("email", None)

        if not (session["password"] == session["conPassword"]):
            errors.append("Passwords don't match")
            er = 1

        if len(session["password"]) < 8 or len(session["conPassword"]) < 8:
            errors.append("Password length should be >= 8")
            er = 2

        if er in [1, 2]:
            session.pop("password", None)
            session.pop("conPassword", None)

        if errors:
            for error in errors:
                flash(error, "danger")
            return render_template("3_signUp.html")

        # Check if the account number already exists
        if not is_account_exists(session["accNo"]):
            # Insert the new user into the database
            insert_user(
                session["accNo"],
                session["password"],
                session["firstName"],
                session["lastName"],
                session["email"],
                session["city"],
                session["state"],
                session["country"],
            )
            an = session["accNo"]
            session.clear()
            session["accNo"] = an
            flash("Registration successful! You can now sign in.", "success")
            return redirect(url_for("views.signIn"))
        else:
            flash(
                "Account number already exists. Choose a different account number.",
                "danger",
            )
            return render_template("3_signUp.html")

    session.clear()
    return render_template("3_signUp.html")


@views.route("/userHome")
def userHome():
    """
    Renders the user home page.

    Returns:
    - If logged in, HTML template for the user home page.
    - If not logged in, redirects to signIn with an error message.
    """
    if "accNo" in session:
        user_details = get_user_details(session["accNo"])
        session.clear()
        session.update(user_details)
        if user_details:
            return render_template("4_userHome.html", user_details=user_details)
        else:
            flash("Error retrieving user details", "danger")
            return redirect(url_for("views.signIn"))
    else:
        flash("You are not logged in", "danger")
        return redirect(url_for("views.signIn"))


@views.route("/signOut")
def signOut():
    """
    Handles user sign-out.

    Returns:
    - Redirects to home page after logging out.
    """
    session.pop("accNo", None)
    flash("You have logged out successfully", "success")
    return redirect(url_for("views.home"))


@views.route("/transactionHistory")
def transactionHistory():
    """
    Renders the transaction history page.

    Returns:
    - If logged in, HTML template for the transaction history page.
    - If not logged in, redirects to signIn with an error message.
    """
    if "accNo" in session:
        user_details = get_user_details(session["accNo"])

        if user_details:
            transactions = get_transaction_history(session["accNo"])
            return render_template(
                "transactionHistory.html",
                user_details=user_details,
                transactions=transactions,
            )
        else:
            flash("Error retrieving user details", "danger")
            return redirect(url_for("views.signIn"))
    else:
        flash("You are not logged in", "danger")
        return redirect(url_for("views.signIn"))


@views.route("/deposit", methods=["GET", "POST"])
def deposit():
    """
    Handles user deposit.

    Returns:
    - If logged in, HTML template for the deposit page.
    - If not logged in, redirects to signIn with an error message.
    """
    if "accNo" in session:
        if request.method == "POST":
            amount = int(request.form.get("amt"))
            password = request.form.get("password")

            # Verify password before processing the deposit
            if verify_credentials(session["accNo"], password):
                # Update the user's balance in the user table
                update_balance(session["accNo"], amount)

                # Record the deposit in the transactions table
                record_transaction(session["accNo"], "deposit", amount)

                flash(f"Deposit of ₹{amount} successful", "success")
                return redirect(url_for("views.deposit"))

            flash("Invalid password", "danger")

        user_details = get_user_details(session["accNo"])
        if user_details:
            return render_template("deposit.html", user_details=user_details)
        else:
            flash("Error retrieving user details", "danger")
            return redirect(url_for("views.signIn"))
    else:
        flash("You are not logged in", "danger")
        return redirect(url_for("views.signIn"))


@views.route("/withdrawal", methods=["GET", "POST"])
def withdrawal():
    """
    Handles user withdrawal.

    Returns:
    - If logged in, HTML template for the withdrawal page.
    - If not logged in, redirects to signIn with an error message.
    """
    err = []
    if "accNo" in session:
        if request.method == "POST":
            amount = int(request.form.get("amt"))
            password = request.form.get("password")

            # Verify password before processing the withdrawal
            if verify_credentials(session["accNo"], password):
                # Check if the user has sufficient balance
                user_details = get_user_details(session["accNo"])
                if user_details["balance"] >= amount:
                    # Update the user's balance in the user table
                    update_balance(session["accNo"], -amount)

                    # Record the withdrawal in the transactions table
                    record_transaction(session["accNo"], "withdrawal", amount)

                    flash(f"Withdrawal of ₹{amount} successful", "success")
                    return redirect(url_for("views.withdrawal"))
                else:
                    err.append("Insufficient balance")
            else:
                err.append("Invalid password")

            if err:
                for error in err:
                    flash(error, "danger")

        user_details = get_user_details(session["accNo"])
        if user_details:
            return render_template("withdrawal.html", user_details=user_details)
        else:
            flash("Error retrieving user details", "danger")
            return redirect(url_for("views.signIn"))
    else:
        flash("You are not logged in", "danger")
        return redirect(url_for("views.signIn"))
