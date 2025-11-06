from concurrent.futures import ThreadPoolExecutor, as_completed
from .models import Patient
from .db import db

def average_age(batch_size: int = 100) -> float:
    # Stream patients in batches so it scales
    total_age = 0
    total_count = 0

    def chunk(query, size):
        offset = 0
        while True:
            rows = query.limit(size).offset(offset).all()
            if not rows:
                break
            yield rows
            offset += size

    with ThreadPoolExecutor(max_workers=4) as ex:
        futures = [ex.submit(lambda rows=rows: sum(p.age for p in rows), rows)
                   for rows in chunk(Patient.query, batch_size)]
        counts = []
        for rows in chunk(Patient.query, batch_size):
            counts.append(len(rows))
        for i, fut in enumerate(as_completed(futures)):
            total_age += fut.result()
        total_count = sum(counts)
    return (total_age / total_count) if total_count else 0.0
