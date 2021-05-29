class Deadline:
    def __init__(self, title, date) -> None:
        self.deadline_title = title
        self.date = date
    def __str__(self) -> str:
        return '{}: {}'.format(self.deadline_title, self.date)
    def __repr__(self) -> str:
        return '{}: {}'.format(self.deadline_title, self.date)