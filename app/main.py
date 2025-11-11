import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routes import users, banners, categories, products
from app.core.logger import setup_logger


setup_logger()
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.APP_NAME, version=settings.APP_VERSION, debug=settings.DEBUG
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制为小程序域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(users.router, prefix="/api/users", tags=["用户"])
app.include_router(banners.router, prefix="/api/banners", tags=["首页轮播"])
app.include_router(categories.router, prefix="/api/categories", tags=["品类"])
app.include_router(products.router, prefix="/api/products", tags=["产品"])


@app.get("/")
async def root():
    return {"message": "后端服务运行中"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/headers")
async def headers_info(req: Request):
    return req.headers


## TODO: 添加验证中间件 allowedSources x-wx-source

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)
