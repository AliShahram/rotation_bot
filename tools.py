"""
Description:
This file contains the functionalities/objects for the interface between
the database and the front end.


Functionalities include:
    - Create/update list
    - Delete list
    - Read list
    - Pop current item
"""

from models import db, Teams, Tasks


class TaskManager:
    def __init__(self):
        pass


    def processInput(self, teams_id, name):
        """This method takes teams_id and name as input,
        looks up if the team exists, and if there is a task with the given name.
        If either don't exist, it returns the appropriate error
        else it return the team and task objects
        """
        team = Teams.query.filter_by(teams_id=teams_id).first()
        if not team:
            return {'status': 401,
                    'message': 'Team does not exist'}

        task = Tasks.query.filter_by(teams_id=team.id, name=name).first()
        if not task:
            return {'status': 401,
                    'message': 'Task does not exist'}
        return team, task


    def createTask(self, data):
        """inputs:
            @string task name
            @string task members
        """
        team = Teams.query.filter_by(teams_id=data['teams_id']).first()
        if not team:
            return {'status': 401,
                    'message': 'Team does not exist'}

        existing = Tasks.query.filter_by(teams_id=team.id).filter_by(name=data['name']).first()
        if not existing:
            new_task = Tasks(teams_id=team.id, name=data['name'], items=data['items'])
            db.session.add(new_task)
            message = 'New Task created'
            val = new_task.items
        else:
            existing.items = data['items']
            message = 'Existing task updated'
            val = existing.items

        db.session.commit()
        return {'status': 201,
                'message': message,
                'val': val}


    def deleteTask(self, teams_id, name):
        team, task = self.processInput(teams_id, name)
        db.session.delete(task)
        db.session.commit()
        return {'status': 200,
                'message': 'Successfuly deleted item'}


    def getTask(self, teams_id, name):
        team, task = self.processInput(teams_id, name)
        return {'status': 200,
                'message': 'Successfuly retrieved item',
                'val': task.items}



    def popItem(self, teams_id, name):
        team, task = self.processInput(teams_id, name)
        items = task.items.split(',')

        popped_item = items.pop(0)
        items.append(popped_item)

        task.items = ','.join(items)
        db.session.commit()

        return {'status': 200,
                'message': 'Successfuly rotated items',
                'val': popped_item}
