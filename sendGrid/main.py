
from train.sendGrid.template.template import MyTemplate
from train.sendGrid.sendGrid import MySendGrid

if __name__ == "__main__":

    fake_data = {
        "name": "Hamza",
        "cta_link": "https://www.youtube.com/",
        "social_media_username": "cristiano"
    }

    # Template file name inside Designs/
    MyTemplate.preview_template("new_user_sign_up.html", fake_data)

    MySendGrid.send_email(recipient="hamza.jj.jbk@gmail.com")
