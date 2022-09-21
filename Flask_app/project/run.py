from app import create_app,db
from flask_migrate import Migrate, MigrateCommand, upgrade
#from flask_script import Manager

app = create_app()
#manager = Manager(app)
#migrate = Migrate(app, db)
#manager.add_command('db', MigrateCommand)


#@manager.command
def recreate_db():
    with app.app_context():
        #db.drop_all()
        db.create_all()
        db.session.commit()
        print('ok')

if __name__ =='__main__':
    app.run(debug=True)