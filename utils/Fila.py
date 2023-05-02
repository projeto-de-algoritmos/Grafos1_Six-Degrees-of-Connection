class FilasAdjacentes():
  def __init__(self):
    self.vizinhos = []

  def add(self, node):
    self.vizinhos.append(node)

  def contains_state(self, state):
    return any(node.state == state for node in self.vizinhos)

  def empty(self):
    return len(self.vizinhos) == 0

  def remove(self):
    if self.empty():
      raise Exception("vazio")
    else:
      node = self.vizinhos[0]
      self.vizinhos = self.vizinhos[1:]
      return node
