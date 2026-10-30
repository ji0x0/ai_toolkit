from contextlib import asynccontextmanager
from pathlib import Path
from typing import Literal
import os

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field
from ai.rag import answer
from data.analysis import profile
from .database import Database


class ItemInput(BaseModel):
    model_config = ConfigDict(extra='forbid', allow_inf_nan=False, str_strip_whitespace=True)
    title: str = Field(min_length=1, max_length=150)
    category: str = Field(default='일반', min_length=1, max_length=60)
    value: float = 0
    status: Literal['new', 'active', 'done'] = 'new'


class DocumentInput(BaseModel):
    model_config = ConfigDict(extra='forbid', str_strip_whitespace=True)
    name: str = Field(min_length=1, max_length=150)
    text: str = Field(min_length=1, max_length=100_000)


class Question(BaseModel):
    model_config = ConfigDict(extra='forbid', str_strip_whitespace=True)
    question: str = Field(min_length=1, max_length=2000)
    k: int = Field(default=3, ge=1, le=10)


class DataInput(BaseModel):
    model_config = ConfigDict(extra='forbid')
    csv_text: str = Field(min_length=1, max_length=5_000_000)
    group_by: str | None = None
    value_column: str | None = None


def create_app(database_path=None, static_dir=None, generator=None):
    db_path = Path(database_path) if database_path else Path(os.getenv('DATA_DIR', '.local/app')) / 'app.sqlite3'
    database = Database(db_path)

    @asynccontextmanager
    async def lifespan(application):
        database.initialize()
        yield

    app = FastAPI(title='Workspace API', version='1.0.0', lifespan=lifespan)
    app.state.database = database

    @app.get('/api/health')
    def health():
        return {'status': 'ok', 'storage': 'sqlite', 'rag_mode': 'extractive' if generator is None else 'provided-generator'}

    @app.get('/api/items')
    def list_items(limit: int = Query(100, ge=1, le=1000), offset: int = Query(0, ge=0)):
        return database.items(limit, offset)

    @app.post('/api/items', status_code=201)
    def create_item(item: ItemInput):
        return database.create_item(item.model_dump())

    @app.put('/api/items/{identifier}')
    def update_item(identifier: str, item: ItemInput):
        result = database.update_item(identifier, item.model_dump())
        if result is None:
            raise HTTPException(404, 'item not found')
        return result

    @app.delete('/api/items/{identifier}', status_code=204)
    def delete_item(identifier: str):
        if not database.delete('items', identifier):
            raise HTTPException(404, 'item not found')
        return Response(status_code=204)

    @app.post('/api/data/profile')
    def analyze(data: DataInput):
        try:
            return profile(data.csv_text, data.group_by, data.value_column)
        except ValueError as error:
            raise HTTPException(422, str(error)) from error

    @app.get('/api/documents')
    def list_documents():
        return database.documents()

    @app.post('/api/documents', status_code=201)
    def add_document(document: DocumentInput):
        try:
            return database.add_document(document.name, document.text)
        except ValueError as error:
            raise HTTPException(409, str(error)) from error

    @app.delete('/api/documents/{identifier}', status_code=204)
    def delete_document(identifier: str):
        if not database.delete('documents', identifier):
            raise HTTPException(404, 'document not found')
        return Response(status_code=204)

    @app.post('/api/rag/answer')
    def question(question: Question):
        documents = database.documents(include_text=True)
        try:
            return answer(question.question, [(d['name'], d['text']) for d in documents], question.k, generator)
        except ValueError as error:
            raise HTTPException(422, str(error)) from error
        except Exception as error:
            raise HTTPException(503, 'answer generation failed') from error

    static = Path(static_dir or os.getenv('STATIC_DIR', 'frontend/dist'))
    if static.is_dir():
        app.mount('/', StaticFiles(directory=static, html=True), name='frontend')
    return app


app = create_app()
