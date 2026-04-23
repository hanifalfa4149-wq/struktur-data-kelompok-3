"""FastAPI entrypoint for the logistics backend."""

from api.routes import courier, graph, inventory, queue, stack, tree
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Logistics API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tree.router)
app.include_router(inventory.router)
app.include_router(queue.router)
app.include_router(stack.router)
app.include_router(courier.router)
app.include_router(graph.router)


@app.get("/")
def root() -> dict[str, str]:
    """Return API health status."""
    return {"status": "Logistics API running"}
