class Config:
    SECRET_KEY = 'f69bab14e88d577f730e04b72a480acbad15d5ebdb038ad7'
    # 'mysql+pymysql://root:password@localhost/CommonBlock'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost/CommonBlock'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'app/furniture_images'