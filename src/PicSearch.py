from fastapi import APIRouter
from src import vectorSearch
from pydantic import BaseModel
import requests
import json

cfg = json.load(open('./src/config.json'))

pools = cfg['pools']
host = cfg['host']
port = cfg['port']

router_PicSearch = APIRouter()


class ItemPic(BaseModel):
    vector: list

    pool: list
    limit: int


class ItemId(BaseModel):
    id_vector: int
    id_pool: int

    limit: int


@router_PicSearch.post('/')
async def post_PicSearch(item: ItemPic):
    v = vectorSearch.search(vector=item.vector, pool_id=item.pool, limit=item.limit)
    return v


@router_PicSearch.post('/by_id')
async def post_PicSearch_by_id(item: ItemId):
    url = f'http://{host}:{port}/collections/{pools[item.id_pool]}/points/{item.id_vector}'
    # url = f'http://{host}:{port}/collections/{pools[item.id_pool]}/points/{item.id_vector}'
    resp = requests.get(
        url).json()['result']['vector']

    v = vectorSearch.search(vector=resp, pool_id=[item.id_pool], limit=item.limit)
    return v
