from src import DB as db
from werkzeug.security import generate_password_hash, check_password_hash

# Schema:
# +--------+----------+----------------+
# | UserID | Username | Email          |
# +--------+----------+----------------+
# | 1      | JohnDoe  | john@example.com |
# | 2      | JaneDoe  | jane@example.com |
# +--------+----------+----------------+

# Ads Table
# +-------+--------+-------------------+
# | AdID  | UserID | AdContent         |
# +-------+--------+-------------------+
# | 101   | 1      | Ad content here... |
# | 102   | 1      | More ad content... |
# | 103   | 2      | Another ad content |
# +-------+--------+-------------------+

# Typically, table names are plural.
USER_TABLE_NAME = 'users'
ADS_TABLE_NAME = 'ads'

class User(db.Model):
    """Represents a user registered on the website.

    - id: The ID of the user (used as primary key)
    - username: The user's username.
    - email: The user's email registered to the account.
    - password_hash: The hashed password for the user's account.
    
    Note: for initial stages, there will only be one user: the developer(s).
    As of 5/19 we aren't implementing logins. This is only there if we decide
    to scale.
    """
    __tablename__ = USER_TABLE_NAME
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), nullable = False)
    lastname = db.Column(db.String(80), nullable = False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    # Creates a link between the `Ad` model and user id. Note: this is done by
    # setting `db.ForeignKey(<tablename>.<attribute>)` and will only consider that
    # foreign key. Here, it's linking the `id` since it's the primary.
    # From ChatGPT: "The backref='owner' in User.ads adds an owner attribute to each Ad instance, which refers back to the associated User."
    ads = db.relationship('Ad', backref='owner', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Ad(db.Model):
    """A model for a specific ad, including the following:
        - ad_id: The ID of the ad
        - user_id: The ID of the owner of the ad, linked to user.id as foreign key.
        - title: The title of the ad to display (bolded section typically)
        - text: Any information that goes into the ad (shown)
        - image_url: The path to the image
        - cta_text: What CTA to show the user
        - cta_link: The link to the advertised item/service.
    """
    __tablename__ = ADS_TABLE_NAME
    ad_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(f'{USER_TABLE_NAME}.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    cta_text = db.Column(db.String(255), nullable=False)
    cta_link = db.Column(db.String(255), nullable=False)
