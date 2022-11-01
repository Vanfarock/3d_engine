from engine import Engine

engine = Engine(
    max_fps=120,
    fov=90,
    near=0.1,
    far=1_000
)
engine.run()
