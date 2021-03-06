import uvicorn
from fastapi import FastAPI, Request
from models import register as user_models
from database import engine
from routers import user, send_mail, authentication, oauth2
import logging
import time
import string
import random

user_models.Base.metadata.create_all(engine)

app = FastAPI()
app.include_router(authentication.router)
app.include_router(oauth2.router)
app.include_router(user.router)
app.include_router(send_mail.router)


# setup loggers
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

# get root logger
logger = logging.getLogger(__name__)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}")

    return response

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)