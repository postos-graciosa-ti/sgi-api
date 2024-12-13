from models.turn import Turn
from repository.functions import find_all, create, update, delete
from datetime import datetime

def parse_form_data(formData: Turn):
  formData.start_time = datetime.strptime(formData.start_time, "%H:%M").time()
  
  formData.start_interval_time = datetime.strptime(formData.start_interval_time, "%H:%M").time()
  
  formData.end_time = datetime.strptime(formData.end_time, "%H:%M").time()
  
  formData.end_interval_time = datetime.strptime(formData.end_interval_time, "%H:%M").time()
  
  return formData

def handle_get_turns():
  turns = find_all(Turn)

  return turns

def handle_post_turns(formData: Turn):
  formData.start_time = datetime.strptime(formData.start_time, "%H:%M").time()
  
  formData.start_interval_time = datetime.strptime(formData.start_interval_time, "%H:%M").time()
  
  formData.end_time = datetime.strptime(formData.end_time, "%H:%M").time()
  
  formData.end_interval_time = datetime.strptime(formData.end_interval_time, "%H:%M").time()
  
  turns = create(formData)

  return turns

def handle_put_turns(id: int, formData: Turn):
  formData.start_time = datetime.strptime(formData.start_time, "%H:%M").time()
  
  formData.start_interval_time = datetime.strptime(formData.start_interval_time, "%H:%M").time()
  
  formData.end_time = datetime.strptime(formData.end_time, "%H:%M").time()
  
  formData.end_interval_time = datetime.strptime(formData.end_interval_time, "%H:%M").time()
  
  return update(id, Turn, formData)

def handle_delete_turn(id: int):
  return delete(id, Turn)
