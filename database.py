import datetime
import os
from typing import Optional

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from menu import Menu

# Code referenced from https://firebase.google.com/docs/firestore/quickstart#python

# Use a service account
cred = credentials.Certificate(os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))
firebase_admin.initialize_app(cred)

db = firestore.client()
menus_ref = db.collection('menus')


def insert_menu(menu: Menu):
    doc_ref = menus_ref.document(menu.datetime.date().isoformat())
    doc_ref.set(menu.to_dict())


def get_menu(date: datetime.date):
    """

    Args:
        date:

    Returns:
        A Menu object for the requested date OR None if it was not found.
    """
    doc_id = date.isoformat()
    doc = menus_ref.document(doc_id).get()
    return Menu.parse_from_dict(doc.to_dict()) if doc.to_dict() else None
