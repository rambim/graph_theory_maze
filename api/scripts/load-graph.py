from redis import Redis
from redisgraph import Node, Edge, Graph
import sys, os

class MazeLoader:

  def __init__ (self,
    GTM_REDIS_HOST: str = os.getenv ('GTM_REDIS_HOST', 'localhost'),
    GTM_REDIS_PORT: int = int (os.getenv ('GTM_REDIS_PORT', 6379))
  ):

    self.redis_cliente = Redis (
      host = GTM_REDIS_HOST,
      port = GTM_REDIS_PORT
    )


  def load_maze (self, maze_id: str, maze_file_path: str):
    graph = Graph (
      maze_id,
      self.redis_cliente
    )

    with open (maze_file_path, 'r') as file:
      for line in file:
        n1, n2, p = '', '', ''
        node01: Node = None
        node02: Node = None
        edge: Edge = None

        try:
          n1, n2 = line.split (':')
        except:
          n1, n2, p = line.split (':')
        
        node01 = Node (
          node_id = int (n1.strip ()),
          label = 'node',
          properties = {
          'is_end': False,
          'is_start': False,
          'node_id': int (n1.strip ())
          }
        )

        node02 = Node (
          node_id = int (n2.strip ()),
          label = 'node',
          properties = {
            'is_end': p.strip () == 'end',
            'is_start': p.strip () == 'start',
            'node_id': int (n2.strip ())
          }
        )

        graph.add_node (node01)
        graph.add_node (node02)

        edge = Edge (
          src_node = node01,
          relation = 'connects',
          dest_node = node02
        )

        graph.add_edge (edge = edge)

    graph.commit ()


if __name__ == '__main__':
  maze_id = None
  maze_file_path = None
  ml: MazeLoader = None

  if len (sys.argv) == 5:
    redis_host = sys.argv [1]
    redis_port = sys.argv [2]
    maze_id = sys.argv [3]
    maze_file_path = sys.argv [4]

    ml = MazeLoader (
      GTM_REDIS_HOST = redis_host,
      GTM_REDIS_PORT = redis_port
    )

  elif len (sys.argv) == 3:
    maze_id = sys.argv [1]
    maze_file_path = sys.argv [2]
    ml = MazeLoader ()

  else:
    raise Exception ('Incorrect number of arguments. Use `python load-graph.py <redis_host> <redis_port> <maze_id> <maze_file_path>` ou `python load-graph.py <maze_id> <maze_file_path>`')

  try:
    ml.load_maze (
      maze_id = maze_id,
      maze_file_path = maze_file_path
    )

    print (f'{maze_file_path} carregado com sucesso!')
  except Exception as e:
    print (f'Algo deu errado!')
    raise e
