from flask import flash


class Flash():
    @staticmethod
    def error(message):
        flash(message, category='error')

    @staticmethod
    def info(message):
        flash(message, category='info')

    @staticmethod
    def success(message):
        flash(message, category='success')
