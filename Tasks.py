from enum import Enum

from MatrixFiles import readMatrixB, readMatrixA, saveMatrix
from Strassen import prepare_p_instructions, compute_leaf, continueStrassen, adapt_odd_matrices, restore_size

LEAFSIZE = 128


class TaskType(Enum):
    INTRO = -1
    TOPDOWN = 0
    DOWNTOP = 1

class EntryTask:
    task_type = TaskType.INTRO

    def __init__(self):
        super().__init__()
        self.matrix_a = readMatrixA()
        self.matrix_b = readMatrixB()
        self.original_tam = self.matrix_a.shape[0]

    def compute(self):
        adapted_matrices = adapt_odd_matrices(self.matrix_a, self.matrix_b)
        task = TopDownTask(None, 0, adapted_matrices[0], adapted_matrices[1])
        output = task.compute()
        if type(output) == list:
            return output
        else:
            restored_matrix = restore_size(output.matrix, self.original_tam)
            saveMatrix(restored_matrix)
            return restored_matrix




class TopDownTask:
    task_type = TaskType.TOP_DOWN

    def __init__(self, master_task_id, current_id, matrix_a, matrix_b):
        super().__init__()
        self.master_task_id = master_task_id
        self.current_id = current_id
        self.matrix_a = matrix_a
        self.matrix_b = matrix_b
        self.master_host = None
        self.master_port = None

    def compute(self):
        if self.matrix_a.shape[0] > LEAFSIZE:
            return self.make_next_topdown_tasks()
        else:
            return self.make_leaf_responce()

    def make_next_topdown_tasks(self):
        output = []
        p_instructions = prepare_p_instructions(self.matrix_a, self.matrix_b)
        for instruction_id, instruction in iter(p_instructions):
            output.append(TopDownTask(self.master_task_id + self.current_id,
                                      instruction_id,
                                      instruction['matrix_a'],
                                      instruction['matrix_b']))
        return output

    def make_leaf_responce(self):
        output_matrix = compute_leaf(self.matrix_a, self.matrix_b)
        return TaskResponse(self.master_task_id, self.current_id, output_matrix, self.master_host, self.master_port)


class DownTopTask:
    task_type = TaskType.DOWN_TOP

    def __init__(self, master_host, master_port, master_task_id, current_id, original_tam=None):
        super().__init__()
        self.master_host = master_host
        self.master_port = master_port
        self.current_id = current_id
        self.master_task_id = master_task_id
        self.p_matrices = {}
        self.original_tam = original_tam

    def compute(self):
        output_matrix = continueStrassen(self.p_matrices['1'], self.p_matrices['2'], self.p_matrices['3'],
                                         self.p_matrices['4'], self.p_matrices['5'], self.p_matrices['6'],
                                         self.p_matrices['7'])
        response = TaskResponse(self.master_task_id, self.current_id, output_matrix, self.master_host, self.master_port)
        return response

    def is_complete(self):
        for i in range(1, 7):
            if str(i) not in self.p_matrices:
                return False
        return True


class TaskResponse:

    def __init__(self, task_id, p_id, matrix, target_host=None, target_port=None):
        super().__init__()
        self.task_id = task_id
        self.p_id = p_id
        self.matrix = matrix
        self.target_host = target_host
        self.target_port = target_port
