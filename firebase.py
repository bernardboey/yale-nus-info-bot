import datetime
import os
from typing import Optional

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Code referenced from https://firebase.google.com/docs/firestore/quickstart#python

# Use a service account
cred = credentials.Certificate(os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))
firebase_admin.initialize_app(cred)

db = firestore.client()
menus_ref = db.collection('menus')


def insert_menu(menu_dict: dict):
    doc_ref = menus_ref.document(menu_dict["date"].date().isoformat())
    doc_ref.set(menu_dict)


def get_menu(date: datetime.date) -> Optional[dict]:
    """

    Args:
        date:

    Returns:
        A dictionary containing the menu for the requested date OR None if it was not found.
    """
    doc_id = date.isoformat()
    doc = menus_ref.document(doc_id).get()
    return doc.to_dict()
