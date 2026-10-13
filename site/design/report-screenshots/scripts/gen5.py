import json,copy
base=json.load(open('site/data/report.json'))['results']
tmpl={r['result_id']:r for r in base}
E={
 'revenue_1997':dict(t=tmpl['extract1'],title='Revenue in 1997',cat='sales'),
 'order_total_1995':dict(t=tmpl['loc1'],title='Order total in 1995',cat='sales',prompt='What was the total price of all the orders placed in 1995?',exp='35055813985.22',src=['orders','lineitem'],db=None,sc=None),
 'top_segment':dict(t=tmpl['contains1'],title='Market segment with the most customers',cat='customers'),
 'top_nations_last_year':dict(t=tmpl['judge1'],title='Top 5 nations by orders last year',cat='customers',prompt='Which 5 nations placed the most orders last year?',exp='Germany, France, Brazil, Japan and Canada placed the most orders.',src=['orders','customer','nation'],db=None,sc=None),
}
# scores per model per run: (acc,prov) per eval, in eval order above
S='claude-sonnet-4-5';H='claude-haiku-4-5';G='gpt-5.4-mini'
runs=[ # date, model, scores
 ('2026-10-01',S,[(1,1),(1,1),(1,1),(.9,1)]),
 ('2026-10-02',S,[(1,1),(1,1),(1,1),(1,1)]),
 ('2026-10-03',S,[(1,1),(1,1),(1,1),(.9,1)]),
 ('2026-10-03',H,[(1,.5),(.6,1),(1,1),(.5,.67)]),
 ('2026-10-04',S,[(1,1),(1,1),(1,1),(1,1)]),
 ('2026-10-04',G,[(1,1),(1,.5),(1,1),(.8,1)]),
 ('2026-10-05',S,[(1,1),(1,.5),(1,1),(1,1)]),
 ('2026-10-06',S,[(1,1),(1,.5),(1,1),(.9,1)]),
 ('2026-10-06',H,[(0,.5),(.6,.5),(1,1),(.5,.67)]),
 ('2026-10-07',S,[(.6,.5),(1,.5),(1,1),(1,1)]),
 ('2026-10-08',S,[(0,.5),(1,.5),(1,1),(1,1)]),
 ('2026-10-08',G,[(1,1),(1,.5),(1,1),(.9,1)]),
 ('2026-10-09',S,[(0,.5),(1,.5),(1,1),(.9,1)]),
 ('2026-10-10',S,[(0,.5),(1,.5),(1,1),(1,1)]),
]
out=[];n=0
for i,(d,m,sc) in enumerate(runs):
  hh='08' if m==S else ('09' if m==H else '10')
  ts=f'{d} {hh}:02:11'; rid=f'run{i}'
  for (eid,e),(a,p) in zip(E.items(),sc):
    r=copy.deepcopy(e['t']); n+=1
    r.update(run_id=rid,run_timestamp=ts,model_name=m,eval_id=eid,eval_title=e['title'],category=e['cat'],accuracy_score=a,provenance_score=p,result_id=f'r{n}',grading_model=None if r['accuracy_method']=='contains' else S,agent_backend='openai' if m==G else 'anthropic')
    if 'prompt' in e: r['prompt']=e['prompt']; r['expected_answer']=e['exp']; r['expected_sources']=e['src']; r['expected_database']=e['db']; r['expected_schema']=e['sc']
    srcs=r['expected_sources']
    if p<1:
      k=max(1,round(p*len(srcs))); q=srcs[:k]
    else: q=srcs
    r['queried_sources']=[{'database':(s.split('.')[0] if s.count('.')==2 else None),'schema':(s.split('.')[1] if s.count('.')==2 else None),'name':s.split('.')[-1]} for s in q]
    if eid=='revenue_1997':
      if a==1: r['extracted_answer']='307992639.49'; r['agent_answer']='Our revenue in 1997, net of discounts and before tax, was **$307,992,639.49**.'
      elif a==0: r['extracted_answer']='310330373.70'; r['agent_answer']=tmpl['extract1']['agent_answer']
      else: r['extracted_answer']='309112054.10'; r['agent_answer']='Revenue in 1997 was about **$309.1M**, net of discounts.'
    if eid=='order_total_1995':
      r['accuracy_tolerance_percent']=None; r['accuracy_tolerance']=0.01
      r['extracted_answer']='35055813985.22' if a==1 else '35211493012.80'
      r['agent_answer']=f"The orders placed in 1995 totalled **${float(r['extracted_answer']):,.2f}**."
    if eid=='top_nations_last_year':
      r['accuracy_rationale']='All five nations are right.' if a==1 else ('Four of the five nations are right; Canada is missing and India is listed instead.' if a>=.8 else 'Only two of the five nations match the expected list.')
      r['agent_answer']='Germany, France, Brazil, Japan and Canada placed the most orders last year.' if a==1 else 'Germany, France, Brazil, Japan and India placed the most orders last year.'
    out.append(r)
json.dump({'generated_at':'2026-10-10T08:05:00Z','results':out,'agent_logs':[],'tool_calls':[]},open('site2/data/report.json','w'))
print(len(out)); print([r['result_id'] for r in out if r['run_id']=='run13'])
# trace + sql for the latest revenue_1997 result (r53)
q1="select table_name from information_schema.tables where table_schema = 'main' order by table_name"
q2="select sum(l_extendedprice * (1 - l_discount)) as revenue\nfrom lineitem\nwhere year(l_shipdate) = 1997"
msgs=[{'role':'user','content':[{'type':'text','text':'What was our revenue in 1997, net of discounts and before tax?'}]},
 {'role':'assistant','content':[{'type':'text','text':'I will check which tables are available first.'},{'type':'tool_use','id':'tu_1','name':'query_warehouse','input':{'sql':q1}}]},
 {'role':'user','content':[{'type':'tool_result','tool_use_id':'tu_1','content':[{'type':'text','text':'table_name\ncustomer\nlineitem\nnation\norders\npart\npartsupp\nregion\nsupplier'}]}]},
 {'role':'assistant','content':[{'type':'text','text':'Revenue net of discounts comes from line items. I will sum them for 1997.'},{'type':'tool_use','id':'tu_2','name':'query_warehouse','input':{'sql':q2}}]},
 {'role':'user','content':[{'type':'tool_result','tool_use_id':'tu_2','content':[{'type':'text','text':'revenue\n310330373.70'}]}]},
 {'role':'assistant','content':[{'type':'text','text':out[-4]['agent_answer']}]}]
det={'steps':[{'input_tokens':1650,'output_tokens':62,'duration_ms':1900,'stop_reason':'tool_use'},{'input_tokens':1720,'output_tokens':118,'duration_ms':2600,'stop_reason':'tool_use'},{'input_tokens':1830,'output_tokens':130,'duration_ms':2100,'stop_reason':'end_turn'}],'tool_ms':{'tu_1':180,'tu_2':640}}
rid=out[-4]['result_id']
logs=[{'result_id':rid,'run_id':'run13','eval_id':'revenue_1997','agent_trace':json.dumps(msgs),'step_details':json.dumps(det)}]
tc=[dict(result_id=rid,run_id='run13',eval_id='revenue_1997',call_index=0,tool_name='query_warehouse',type='sql',payload=json.dumps({'sql':q1}),is_error=False,generated=False,step=1,error=None,result_column=None,result_value=None),
    dict(result_id=rid,run_id='run13',eval_id='revenue_1997',call_index=1,tool_name='query_warehouse',type='sql',payload=json.dumps({'sql':q2}),is_error=False,generated=False,step=2,error=None,result_column='revenue',result_value='310330373.70')]
json.dump({'generated_at':'2026-10-10T08:05:00Z','results':out,'agent_logs':logs,'tool_calls':tc},open('site2/data/report.json','w'))
print('rid',rid)
