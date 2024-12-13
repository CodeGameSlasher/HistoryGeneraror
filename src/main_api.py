from __init__ import WordList, HistoryGenerator
from fastapi import FastAPI

words = WordList.from_file('src/words.txt')
generator = HistoryGenerator(words)

print(f'{len(words)} words')

stories = []
app = FastAPI()

@app.get('/generate')
@app.get('/generate{seed}')
@app.get('/generate/{word_count}')
@app.get('/generate{seed}/{word_count}')
def generate_story(word_count: int | None = None, seed: str | int | None = None):
    if seed is not None:
        generator.set_seed(seed)
    return (generator.generate() if word_count is None else generator.generate(word_count))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000)