from wtforms import Form, StringField, PasswordField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, Regexp, ValidationError, length
from models.comments import Comments

class PcommentsForm(Form):
    """用户的第一评论"""
    username = SubmitField(label="username", validators=[DataRequired()])
    message = TextAreaField(label="comments", validators=[DataRequired(message="记录下你的观影感受吧~~"), length(min=1,max=200)])
    email = StringField(label="email", validators=[DataRequired(), Email()])
    # is_appear = BooleanField(label="私密评论")
    submit = SubmitField(label="提交")