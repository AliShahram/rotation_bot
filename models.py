"""
Description:
This file contains the database objects
"""

from extensions import db

class Teams(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teams_id = db.Column(db.String(124), unique=True, nullable=False)
    team_domain = db.Column(db.String(124), unique=False, nullable=True)

    def __repr__(self):
        return '<Team %r>' % self.team_domain


class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teams_id = db.Column(db.ForeignKey("teams.id"), nullable=False)
    team = db.relationship("Teams",
                            foreign_keys=[teams_id],
                            backref=db.backref("Tasks"))
    name = db.Column(db.String(124), unique=False, nullable=False)
    items = db.Column(db.String(512), unique=False, nullable=True)

    def __repr__(self):
        return '<Task %r>' % self.name
