from lib.parsing.LearningTrack import LearningTrack
from lib.parsing.Step import Step, Branch
class LearningTrackGraph:
    
    def __init__(self, lt: LearningTrack) -> None:
        self.lt = lt
        self.steps = lt.steps
        self.step_dict = {}
        self.adjacency_list = {} # maps step id to list of branches to children of that step

        self._init_step_dict()
        self._init_adjacency_list()
        self._build_graph()
        pass
    def _init_step_dict(self) -> None:
        for step in self.steps:
            self.step_dict[step.id] = step
    
    def _init_adjacency_list(self) -> None:
        for step in self.steps:
            self.adjacency_list[step.id] = []

    def _build_graph(self) -> None:
        """Builds the graph by adding branches of each step to the adjacency list"""
        for step in self.steps:
            for branch in step.children:
                if branch.childStepId is None:
                    continue
                self.adjacency_list[step.id].append(branch)
        # Add start and end node
        self.step_dict['start'] = Step('start', 'start', [Branch(0, self.get_root_node().id)], [])
        self.adjacency_list['start'] = self.step_dict['start'].children
        self.step_dict['end'] = Step('end', 'end', [], [])
        self.adjacency_list['end'] = []
        # [Branch(0, step.id) for step in self.steps if len(self.get_child_branches(step.id)) == 0]
        for step in self.steps:
            if len(self.get_child_branches(step.id)) == 0:
                self.adjacency_list[step.id].append(Branch(0, 'end'))
                step.children.append(Branch(0, 'end'))

    def get_child_branches(self, step_id: str) -> list[Branch]:
        """Returns a list of step objects that are children of the step with the given id"""
        branches = []
        for branch in self.adjacency_list[step_id]:
            branches.append(branch)
        return branches
    
    def get_step_by_id(self, step_id):
        return self.step_dict[step_id]
    
    def get_root_node(self) -> Step:
        #root is node with no incoming edges, use adjacency list with list of branches that contain child step id
        for step_id in self.adjacency_list:
            no_incoming_edges = True
            for branches in self.adjacency_list.values():
                if any(branch.childStepId == step_id for branch in branches):
                    no_incoming_edges = False
                    break
            if no_incoming_edges:
                return self.step_dict[step_id]

