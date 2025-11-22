# minor change for next commit
# test commit

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expense_tracker.db'
db = SQLAlchemy(app)

# ----------------- MODELS -----------------
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

class Category(db.Model):
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(50))
    description = db.Column(db.String(100))

class Account(db.Model):
    account_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    account_name = db.Column(db.String(50))
    balance = db.Column(db.Float)
    type = db.Column(db.String(50))

class Transaction(db.Model):
    transaction_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    account_id = db.Column(db.Integer, db.ForeignKey('account.account_id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'))
    amount = db.Column(db.Float)
    type = db.Column(db.String(10))
    date = db.Column(db.String(20))
    note = db.Column(db.String(100))

class Budget(db.Model):
    budget_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'))
    limit_amount = db.Column(db.Float)
    start_date = db.Column(db.String(20))
    end_date = db.Column(db.String(20))

# ----------------- ROUTES -----------------
@app.route('/')
def index():
    transactions = Transaction.query.all()

    # --- Chart and summary data ---
    total_income = sum(t.amount for t in transactions if t.type.lower() == 'income')
    total_expense = sum(t.amount for t in transactions if t.type.lower() == 'expense')
    balance = total_income - total_expense

    chart_data = {
        'labels': ['Income', 'Expense'],
        'values': [total_income, total_expense]
    }

    # Create separate lists for bar chart data
    dates = [t.date for t in transactions]
    amounts = [float(t.amount or 0) for t in transactions]

    return render_template(
        'index.html',
        transactions=transactions,
        chart_data=chart_data,
        total_income=total_income,
        total_expense=total_expense,
        balance=balance,
dates=dates,
        amounts=amounts
    )


@app.route('/add_transaction', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        new_t = Transaction(
            user_id=1,  # test user
            account_id=None,
            category_id=None,
            amount=request.form['amount'],
            type=request.form['type'],
            date=request.form['date'],
            note=request.form['note']
        )
        db.session.add(new_t)
        db.session.commit()
        return redirect('/')
    return render_template('add_transaction.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

