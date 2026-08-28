import json
import csv
import random
from faker import Faker

fake = Faker('pt_BR')

# ---------- JSON lines de vendas de livros ----------
titulos = [
    "O Senhor dos Anéis", "Dom Casmurro", "1984", "A Revolução dos Bichos",
    "Harry Potter e a Pedra Filosofal", "Grande Sertão: Veredas", "O Hobbit",
    "Memórias Póstumas de Brás Cubas", "A Moreninha", "Capitães da Areia"
]
autores = [
    "J.R.R. Tolkien", "Machado de Assis", "George Orwell", "J.K. Rowling",
    "Guimarães Rosa", "José de Alencar", "Jorge Amado"
]
generos = ["Fantasia", "Romance", "Ficção Científica", "Drama", "Aventura"]

with open("livros.json", "w", encoding="utf-8") as f:
    for i in range(1, 501):
        livro = {
            "id": i,
            "titulo": random.choice(titulos),
            "autor": random.choice(autores),
            "genero": random.choice(generos),
            "preco": round(random.uniform(20, 120), 2),
            "quantidade": random.randint(1, 5),
            "data_venda": fake.date_this_year().isoformat(),
            "endereco": {
                "rua": fake.street_name(),
                "numero": random.randint(1, 9999),
                "bairro": fake.bairro(),
                "cidade": fake.city(),
                "estado": fake.estado_sigla(),
                "cep": fake.postcode()
            }
        }
        f.write(json.dumps(livro, ensure_ascii=False) + "\n")

# ---------- CSV de endereços brasileiros ----------
with open("enderecos.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "rua", "numero", "bairro", "cidade", "estado", "cep"])
    for i in range(1, 1001):
        writer.writerow([
            i,
            fake.street_name(),
            random.randint(1, 9999),
            fake.bairro(),
            fake.city(),
            fake.estado_sigla(),
            fake.postcode()
        ])

print("Arquivos gerados: livros.json (500 registros em JSON lines) e enderecos.csv (1000 linhas)")
