import asyncio
from flask import Flask, render_template, flash,request
from forms import AddAccountForm, SwitchAccountForm, SendMessageForm
from manager import AccountManager, get_active_manager, load_managers_from_config

app = Flask(__name__)
app.secret_key = "your-secret-key"

config_file = "config.json"
managers = load_managers_from_config(config_file)




@app.route('/', methods=['GET', 'POST'])
def index():
    add_account_form = AddAccountForm(request.form)
    switch_account_form = SwitchAccountForm()
    send_message_form = SendMessageForm()
    if request.method == 'POST' and add_account_form.validate():
        try:
            manager = AccountManager(add_account_form.phone_number.data, add_account_form.api_id.data, add_account_form.api_hash.data)
            managers.append(manager)
            flash("Account added successfully", "success")
        except Exception as e:
            raise e
            flash(f'Error: {str(e)}', 'danger')



    if switch_account_form.validate_on_submit():
        account_id = switch_account_form.account_id.data
        if 0 < account_id <= len(managers):
            AccountManager.set_active_manager(managers[account_id - 1])
            flash(f"Switched to account {account_id}", "success")
        else:
            flash("Invalid account ID", "danger")

    if send_message_form.validate_on_submit():
        active_manager = get_active_manager()
        if active_manager:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(
                active_manager.execute_task(
                    "send_message",
                    telegram_id=send_message_form.telegram_id.data,
                    message=send_message_form.message.data,
                )
            )
            flash("Message sent successfully", "success")
        else:
            flash("Please select an account before sending messages", "danger")

    return render_template("index.html", add_account_form=add_account_form, switch_account_form=switch_account_form, send_message_form=send_message_form)

if __name__ == "__main__":
    app.run(debug=True)
