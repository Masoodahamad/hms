"""
Batch Calculation for Patient Data
"""
import logging
from .db import db
from .models import Patient
from .config import Config

log = logging.getLogger(__name__)

def calculate_average_age() -> float:
    """
    Calculates the average age of all patients by processing them in batches.
    
    This method is memory-efficient as it does not load all patients
    into memory at once.
    
    Returns:
        float: The average age, or 0.0 if no patients exist.
    """
    
    # Get the batch size from our config file
    batch_size = Config.DEFAULT_BATCH_SIZE
    offset = 0
    
    total_age = 0
    total_count = 0
    
    log.info(f"Starting average age calculation with batch size {batch_size}...")
    
    # We will use modern SQLAlchemy 2.0 select syntax
    # We only select the 'age' column, which is more efficient
    base_query = db.select(Patient.age)

    while True:
        # 1. Create a query for the next batch
        batch_query = base_query.offset(offset).limit(batch_size)
        
        # 2. Execute the query and get the ages
        # .scalars() gets just the age values (e.g., [25, 42, 61])
        ages_in_batch = db.session.execute(batch_query).scalars().all()

        # 3. Check if the batch is empty
        if not ages_in_batch:
            log.info("No more patients found. Finishing calculation.")
            break # Exit the loop if we've processed all patients

        # 4. Process the batch
        total_age += sum(ages_in_batch)
        total_count += len(ages_in_batch)
        
        log.debug(f"Processed batch. Offset: {offset}, Count: {len(ages_in_batch)}")

        # 5. Move to the next batch
        offset += batch_size

    # --- Calculation Complete ---
    
    if total_count == 0:
        log.warning("calculate_average_age: No patients found in database.")
        return 0.0

    average = total_age / total_count
    log.info(f"Calculation complete. Total Patients: {total_count}, Average Age: {average:.2f}")
    
    return average
