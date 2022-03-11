from .models import Board


def gen_master(apps, schema_editor):
    boards = [('notice', 'Notice')]
    for board in boards:
        Board(name=board[0], title=board[1]).save()
