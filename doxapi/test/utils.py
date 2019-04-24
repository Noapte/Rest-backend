from doxapi.app import db


def commit(db_item):
    db.session.add(db_item)
    db.session.commit()
    return db_item
