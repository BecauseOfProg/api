import time

from pony.orm import *
from werkzeug.exceptions import NotFound
from app.controllers.users import UsersController
from app.models.arduino import ArduinoProject


class ArduinoController:
    @staticmethod
    def fill_informations(project: ArduinoProject):
        p = project.to_dict()
        p['author'] = UsersController.get_one(p['author'])
        return p

    @staticmethod
    @db_session
    def get_all():
        projects = list(ArduinoProject.select().order_by(desc(ArduinoProject.timestamp)))
        for project in projects:
            projects[projects.index(project)] = ArduinoController.fill_informations(project)
        return projects

    @staticmethod
    @db_session
    def get_last():
        projects = list(ArduinoProject.select().order_by(desc(ArduinoProject.timestamp)))
        return ArduinoController.fill_informations(projects[0])

    @staticmethod
    @db_session
    def get_featured():
        projects = list(ArduinoProject.select(lambda p: p.is_featured == True).order_by(desc(ArduinoProject.timestamp)))
        for project in projects:
            projects[projects.index(project)] = ArduinoController.fill_informations(project)
        return projects

    @staticmethod
    @db_session
    def get_from_staff():
        projects = list(ArduinoProject.select(lambda p: p.is_from_staff == True).order_by(desc(ArduinoProject.timestamp)))
        for project in projects:
            projects[projects.index(project)] = ArduinoController.fill_informations(project)
        return projects

    @staticmethod
    @db_session
    def get_one(url):
        try:
            return ArduinoController.fill_informations(ArduinoProject[url])
        except core.ObjectNotFound:
            raise NotFound

    @staticmethod
    @db_session
    def create_one(params, optional_data):
        timestamp = int(time.time())

        # Required fields
        project = ArduinoProject(name=params['name'],
                                 url=params['url'],
                                 summary=params['summary'],
                                 thumbs_up=0,
                                 is_from_staff=params['from_staff'],
                                 is_featured=False,
                                 timestamp=timestamp,
                                 author=params['author_username'])
        # Optional fields
        for field in optional_data:
            if field in params['optional']:
                setattr(project, field, params['optional'][field])
        commit()
        return True

    @staticmethod
    @db_session
    def update_one(url, params, optional_data):
        try:
            project = ArduinoProject[url]
            for field in optional_data:
                if field in params:
                    setattr(project, field, params[field])
            commit()
        except core.ObjectNotFound:
            raise NotFound

    @staticmethod
    @db_session
    def delete_one(url):
        try:
            ArduinoProject[url].delete()
            return True
        except core.ObjectNotFound:
            raise NotFound
