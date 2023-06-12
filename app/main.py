import uvicorn

from fastapi import FastAPI, Request, UploadFile, File, Form, Body

from app.services import compare_styles, get_styles_from_file


app = FastAPI()


ALLOWED_LANGS = ('en', 'de', 'es', 'fr')


async def check_lang(lang: str) -> dict:
    if lang not in ALLOWED_LANGS:
        return {'message': 'This language is not supported'}


@app.get('/')
async def main() -> dict:
    return {'Success': True}


@app.post('/get_style/')
async def get_style(data=Body()) -> dict[str, bool]:
    lang = data.get('lang')
    phrase = data.get('phrase')
    result = await check_lang(lang)
    if not result:
        style = compare_styles(phrase, lang)
        result = {phrase: style}
    return result


@app.get('/get_my_style/')
async def get_my_style(lang: str = 'en', phrase: str = 'Hi dude') -> dict[str, bool]:
    result = await check_lang(lang)
    if not result:
        style = compare_styles(phrase, lang)
        result = {phrase: style}
    return result


@app.post('/get_file_styles/')
async def get_styles(file: UploadFile = File(...), lang: str = Form(...)) -> list[tuple[str, bool]]:
    result = await check_lang(lang)
    if not result:
        result = get_styles_from_file(file, lang)
    return result


# if __name__ == '__main__':
#     app.debug = True
#     uvicorn.run(app, host='127.0.0.1', port=8000)
