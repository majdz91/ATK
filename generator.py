#funcion to generate chunks of 8 digits strings to verify input 

import random,string
# usage generator.get_ran_str()
def get_ran_str(size=8, chars=string.ascii_uppercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))
