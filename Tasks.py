from enum import Enum

from Strassen import prepare_p_instructions, compute_leaf

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
			output.append(TopDownTask(self.current_id, instruction_id, instruction['matrix_a'], instruction['matrix_b'], instruction['tam']))
		return output
	
	def make_leaf_responce(self):
		output_matrix = compute_leaf(self.matrix_a, self.matrix_b)
		return [TaskResponse(self.master_task_id, self.current_id, output_matrix, self.master_hostname)]
	
	
		
	
class DownTopTask:
	task_type = TaskType.DOWN_TOP
	master_hostname = None
	p_matrices = {}
	master_task_id = None
	current_id = None
	
class TaskResponse:
	
	def __init__(self, task_id, p_id, matrix, target_hostname=None):
		super().__init__()
		self.task_id = task_id
		self.p_id = p_id
		self.matrix = matrix
		self.target_hostname = target_hostname
	