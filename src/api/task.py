from datetime import datetime
class Task:
    def __init__(self,id, title, description, due_date, priority='Normal', tags=None, completed=False, created_at=datetime.now(), recurrence = "once"):
        if tags is None:
            tags = []
        self.id = id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.tags = tags
        if type(self.tags) is not list:
            self.tags = [self.tags]
        self.completed = completed
        self.created_at = created_at
        self.recurrence = recurrence  # Options: "daily", "weekly", "monthly", "yearly", "once"

    def mark_as_completed(self):
        self.completed = True

    def __str__(self):
        return (f"Task(title={self.title}, description={self.description}, due_date={self.due_date}, "
                f"priority={self.priority}, tags={self.tags}, completed={self.completed})")