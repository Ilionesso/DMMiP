from enum import Enum

from Strassen import prepare_p_instructions, compute_leaf, continueStrassen

LEAFSIZE = 128


class TaskType(Enum):
    TOPDOWN = 0
    DOWNTOP = 1


class TopDownTask:
    task_type = TaskType.TOP_DOWN

    def __init__(self, master_task_id, current_id, matrix_a, matrix_b, tam):
        super().__init__()
        self.master_task_id = master_task_id
        self.current_id = current_id
        self.matrix_a = matrix_a
        self.matrix_b = matrix_b
        self.tam = tam
        self.master_hostname = None

    def compute(self):
        if self.tam > LEAFSIZE:
            return self.make_next_topdown_tasks()
        else:
            return self.make_leaf_responce()

    def make_next_topdown_tasks(self):
        output = []
        p_instructions = prepare_p_instructions(self.matrix_a, self.matrix_b, self.tam)
        for instruction_id, instruction in iter(p_instructions):
            output.append(TopDownTask(self.master_task_id + self.current_id,
                                      instruction_id,
                                      instruction['matrix_a'],
                                      instruction['matrix_b'],
                                      instruction['tam']))
        return output

    def make_leaf_responce(self):
        output_matrix = compute_leaf(self.matrix_a, self.matrix_b)
        return [TaskResponse(self.master_task_id, self.current_id, output_matrix, self.master_hostname)]


class DownTopTask:
    task_type = TaskType.DOWN_TOP

    def __init__(self, master_hostname, master_task_id, current_id, tam):
        super().__init__()
        self.master_hostname = master_hostname
        self.current_id = current_id
        self.master_task_id = master_task_id
        self.tam = tam
        self.p_matrices = {}

    def compute(self):
        output_matrix = continueStrassen(self.p_matrices['1'], self.p_matrices['2'], self.p_matrices['3'],
                                         self.p_matrices['4'], self.p_matrices['5'], self.p_matrices['6'],
                                         self.p_matrices['7'], self.tam)
        response = TaskResponse(self.master_task_id, self.current_id, output_matrix, self.master_hostname)
        return response

    def is_complete(self):
        for i in range(1, 7):
            if str(i) not in self.p_matrices:
                return False
        return True


class TaskResponse:

    def __init__(self, task_id, p_id, matrix, target_hostname=None):
        super().__init__()
        self.task_id = task_id
        self.p_id = p_id
        self.matrix = matrix
        self.target_hostname = target_hostname
