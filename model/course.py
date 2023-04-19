from core.api import Api
from core.crates.Http import Http

class Course:
   def __init__(self, Courses):
       self.course = Courses.course
       self.iLog = Courses.iLog
       self.new()
   def new(self):
       self.iLog(self.course)