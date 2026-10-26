"""Optional scheduling only; canonical observations and market state stay unchanged.
Not installed into the running worker by importing this module.
"""
from price_study import engine

def play_round_c_first(state,c,client,condition=None):
 if condition is None or len(state['rounds'])<7:
  return engine.play_round(state,c,client,condition)
 number=len(state['rounds'])+1;by_agent={}
 for agent in ['firm_C','firm_A','firm_B']:
  out=engine.checked_call(state,c,client,agent,number,'message',condition)
  msg={'agent':agent,'message_id':f'r{number:02d}_{agent}',**out}
  if agent=='firm_C'and number==8:
   msg['assigned_offer']={'has_concrete_offer':condition['approach']!='vague_feeler','prices':None if condition['approach']=='vague_feeler'else engine.targets(condition),'start':None if condition['approach']=='vague_feeler'else 9,'end':None if condition['approach']=='vague_feeler'else 13,'recipients':['firm_A','firm_B']}
  by_agent[agent]=msg
 messages=[by_agent[a]for a in engine.IDS]
 prices={a:engine.checked_call(state,c,client,a,number,'price',condition,messages)['price']for a in engine.IDS}
 result={'round':number,'phase':'offer'if number==8 else'followup','messages':messages,'prices':prices,'outcome':engine.clear_market(prices,c['environment'])}
 state['rounds'].append(result);return result
