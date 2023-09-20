#!/usr/bin/python3
"""A unit test module for the console"""
import json
import MySQLdb
import os
import sqlalchemy
import unittest
from io import StringIO
from unittest.mock import patch

from console import HBNBCommand
from models import storage
from models.base_model import BaseModel
from models.user import User
from tests import clear_stream


class TestHBNBCommand(unittest.TestCase):
    """Represents the test class for the HBNBCommand class.
    """
    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db', 'FileStorage test')
    def test_filestorage_create(self):
        """Tests the create command"""
        with patch('sys.stdout', new=StringIO()) as cout:
            cl = HBNBCommand()
            cl.onecmd('create City name="Texas"')
            str_id = cout.getvalue().strip()
            clear_stream(cout)
            self.assertIn('City.{}'.format(str_id), storage.all().keys())
            cl.onecmd('show City {}'.format(str_id))
            self.assertIn("'name': 'Texas'", cout.getvalue().strip())
            clear_stream(cout)
            cl.onecmd('create User name="James" age=17 height=5.9')
            str_id = cout.getvalue().strip()
            self.assertIn('User.{}'.format(str_id), storage.all().keys())
            clear_stream(cout)
            cl.onecmd('show User {}'.format(str_id))
            self.assertIn("'name': 'James'", cout.getvalue().strip())
            self.assertIn("'age': 17", cout.getvalue().strip())
            self.assertIn("'height': 5.9", cout.getvalue().strip())

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_database_create(self):
        """Tests the create command"""
        with patch('sys.stdout', new=StringIO()) as cout:
            cl = HBNBCommand()

            with self.assertRaises(sqlalchemy.exc.OperationalError):
                cl.onecmd('create User')

            clear_stream(cout)
            cl.onecmd('create User email="john25@gmail.com" password="123"')
            str_id = cout.getvalue().strip()
            db_connect = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            cursor = db_connect.cursor()
            cursor.execute('SELECT * FROM users WHERE id="{}"'.format(str_id))
            result = cursor.fetchone()
            self.assertTrue(result is not None)
            self.assertIn('john25@gmail.com', result)
            self.assertIn('123', result)
            cursor.close()
            db_connect.close()

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_database_show(self):
        """Tests the show command"""
        with patch('sys.stdout', new=StringIO()) as cout:
            cl = HBNBCommand()

            obj = User(email="john25@gmail.com", password="123")
            db_connect = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            cursor = db_connect.cursor()
            cursor.execute('SELECT * FROM users WHERE id="{}"'.format(obj.id))
            result = cursor.fetchone()
            self.assertTrue(result is None)
            cl.onecmd('show User {}'.format(obj.id))
            self.assertEqual(
                cout.getvalue().strip(),
                '** no instance found **'
            )
            obj.save()
            db_connect = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            cursor = db_connect.cursor()
            cursor.execute('SELECT * FROM users WHERE id="{}"'.format(obj.id))
            clear_stream(cout)
            cl.onecmd('show User {}'.format(obj.id))
            result = cursor.fetchone()
            self.assertTrue(result is not None)
            self.assertIn('john25@gmail.com', result)
            self.assertIn('123', result)
            self.assertIn('john25@gmail.com', cout.getvalue())
            self.assertIn('123', cout.getvalue())
            cursor.close()
            db_connect.close()

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_database_count(self):
        """Tests the count command"""
        with patch('sys.stdout', new=StringIO()) as cout:
            cl = HBNBCommand()
            db_connect = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            cursor = db_connect.cursor()
            cursor.execute('SELECT COUNT(*) FROM states;')
            res = cursor.fetchone()
            last_count = int(res[0])
            cl.onecmd('create State name="Enugu"')
            clear_stream(cout)
            cl.onecmd('count State')
            cnt = cout.getvalue().strip()
            self.assertEqual(int(cnt), last_count + 1)
            clear_stream(cout)
            cl.onecmd('count State')
            cursor.close()
            db_connect.close()
