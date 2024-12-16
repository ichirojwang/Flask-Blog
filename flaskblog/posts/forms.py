from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField, TextAreaField

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField()

    def __init__(self, submit_label="Post", *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.submit.label.text = submit_label
        