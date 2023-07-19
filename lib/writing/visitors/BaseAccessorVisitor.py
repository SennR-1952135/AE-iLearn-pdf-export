from lib.writing.files.FileWriterFactory import FileWriterFactory

class BaseAccessorVisitor:
    
    def __init__(self, file_type: str, filename: str) -> None:
        self.file_type = file_type
        self.filename = filename
        self.file_writer = FileWriterFactory.create_writer(file_type, filename)

        # Possible to capture more information within the visitor class                           

    def _process_data(self, data: dict) -> None:
        # Implement in subclass
        # capture data from the visited writer object and write it to the file using file_writer
        pass
        
    def visit_learning_track(self, learning_track_accessor):#: LearningTrackWriter) -> None:
        data = learning_track_accessor.get_accessor_data()
        self._process_data(data)

    def visit_step(self, step_accessor):#: StepWriter) -> None:
        data = step_accessor.get_accessor_data()
        self._process_data(data)
    
    def visit_branch(self, branch_accessor):#: BranchWriter) -> None:
        data = branch_accessor.get_accessor_data()
        self._process_data(data)
    
    def visit_objective(self, objective_accessor):#: ObjectiveWriter) -> None:
        data = objective_accessor.get_accessor_data()
        self._process_data(data)
    
    def visit_question(self, question_accessor):#: QuestionWriter) -> None:
        data = question_accessor.get_accessor_data()
        self._process_data(data)
    
    def visit_answer_option(self, answerOption_accessor):#: AnswerOptionWriter) -> None:
        data = answerOption_accessor.get_accessor_data()
        self._process_data(data)
    
    def visit_score_range(self, scoreRange_accessor):#: ScoreRangeWriter) -> None:
        data = scoreRange_accessor.get_accessor_data()
        self._process_data(data)
          
    