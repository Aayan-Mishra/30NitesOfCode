from exa_py import Exa
# You can obtain a free Exa API key at https://exa.ai/
exa = Exa('YOUR_EXA_API_KEY')

query = input("What would you like to search for?: ")

response = exa.search(
    query,
    num_results=5,
    type='keyword',
)

for result in response.results:
    print(f'Title: {result.title}')
    print(f'URL: {result.url}')
    print()
