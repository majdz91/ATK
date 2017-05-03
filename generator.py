#funcion to generate chunks of 8 digits strings to verify input 
from conf import config
import random,string
# usage generator.get_ran_str()
def get_ran_str(size=8, chars=string.ascii_uppercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))
  
def generate():
    hashs = ['start',]
    for i in range (int(config.STU_NUM)) :
        hashs.append(get_ran_str())
    
    hashs.append('end')    
    return hashs
        
        