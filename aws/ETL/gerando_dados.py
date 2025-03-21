import pandas as pd
from faker import Faker

# Inicializando o Faker
fake = Faker()
Faker.seed(42)

# Gerar 5000 registros fictícios
data = {
    "id": [i for i in range(1, 5001)],
    "name": [fake.name() for _ in range(5000)],
    "email": [fake.email() for _ in range(5000)],
    "address": [fake.address() for _ in range(5000)],
    "phone_number": [fake.phone_number() for _ in range(5000)],
    "date_of_birth": [fake.date_of_birth(minimum_age=18, maximum_age=75) for _ in range(5000)],
    "created_at": [fake.date_time_this_year() for _ in range(5000)],
}

# Criar o DataFrame
df = pd.DataFrame(data)

# Salvar em um arquivo CSV
df.to_csv("fake_dataset.csv", index=False)
print("Dataset gerado e salvo como 'fake_dataset.csv'")
