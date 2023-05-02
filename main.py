import csv
import sys
import os

from utils.Node import Node
from utils.Fila import FilasAdjacentes

nome = {}

# Mapa de pessoas (name, birth, filmes)
pessoas = {}

# Mapa de filmes (title, year, stars)
filmes = {}


def load_data():
    with open(f"./dataset/pessoas.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            pessoas[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "filmes": set()
            }
            if row["name"].lower() not in nome:
                nome[row["name"].lower()] = {row["id"]}
            else:
                nome[row["name"].lower()].add(row["id"])

    with open(f"./dataset/filmes.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            filmes[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }
    with open(f"./dataset/estrelas.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                pessoas[row["person_id"]]["filmes"].add(row["movie_id"])
                filmes[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():

    print("Carregando dados...")
    load_data()
    print("Dados carregados.")

    source = busca_nome_usuario(input("Nome do ator: "))
    if source is None:
        sys.exit("Pessoa nao encontrada.")
    target = busca_nome_usuario(input("Nome do ator: "))
    if target is None:
        sys.exit("Pessoa nao encontrada.")
    os.system('clear')
    path = shortest_path(source, target)

    if path is None:
        print("Nao encontrou conexao.")
    else:
        degrees = len(path)
        print(f"{degrees} graus de separacao.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = pessoas[path[i][1]]["name"]
            person2 = pessoas[path[i + 1][1]]["name"]
            movie = filmes[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} e {person2} estrelaram no filme:\n\t** {movie} **")


def shortest_path(source, target):
    start = Node(source, None, None)
    vizinhos = FilasAdjacentes()
    vizinhos.add(start)

    explored = set()

    while True:

      if len(explored) % 100 == 0:
        print('Atores explorados para achar a solucao: ', len(explored))
        print('Nós restantes para expandir aos nos adjacentes: ', len(vizinhos.vizinhos))

      if vizinhos.empty():
        print('vizinhos esta vazio, nao existe conexao entre os atores!')
        print('Atores explorados, solucao nao encontrada: ', len(explored))
        return None

      curr_node = vizinhos.remove()
      explored.add(curr_node.state)

      for action, state in neighbors_for_person(curr_node.state):

        # If state (actor) is the target actor then solution has been found, return path:
        if state == target:
          print('** Solucao encontrada! **')
          print('Atores explorados para achar a solucao:', len(explored))
          path = []
          path.append((action, state))

          while curr_node.parent != None:
            path.append((curr_node.action, curr_node.state))
            curr_node = curr_node.parent

          path.reverse()

          return path

        if not vizinhos.contains_state(state) and state not in explored:
          new_node = Node(state, curr_node, action)
          vizinhos.add(new_node)


def busca_nome_usuario(name):
    person_ids = list(nome.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Qual '{name}' abaixo?")
        for person_id in person_ids:
            person = pessoas[person_id]
            name = person["name"]
            birth = person["birth"]
            print('==============================================')
            print(f"\tID: {person_id}\n\tNome: {name},\n\tAno nascimento: {birth}")
            print('==============================================')
        try:
            person_id = input("Insira ID desejado: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    movie_ids = pessoas[person_id]["filmes"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in filmes[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
