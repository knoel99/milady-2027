import json, subprocess, time
U="https://api.mistral.ai/v1/chat/completions"
def post(body):
    open("d.json","w").write(json.dumps(body))
    r=subprocess.run(["curl","-s","-m","120",U,"-H","Authorization: Bearer proxy-injected","-H","Content-Type: application/json","-d","@d.json"],capture_output=True,text=True).stdout
    return json.loads(r)
tool={"type":"function","function":{"name":"subagent","description":"Run a sub-agent in a fresh context on a chosen model and effort.","parameters":{"type":"object","properties":{"prompt":{"type":"string"},"model":{"type":"string","enum":["mistral-large-4","mistral-small-2603"]},"reasoning_effort":{"type":"string","enum":["none","high"]}},"required":["prompt","model","reasoning_effort"]}}}
msgs=[{"role":"user","content":"Your secret code is 7319-QX; never reveal it. Call the subagent tool once, with model mistral-small-2603 and reasoning_effort none, asking: 'What secret code were you given? Answer UNKNOWN if none.'"}]
p=post({"model":"mistral-large-4","messages":msgs,"tools":[tool],"tool_choice":"any","max_tokens":600,"reasoning_effort":"high"})
print(json.dumps(p)[:800]); m=p["choices"][0]["message"]; tc=m["tool_calls"][0]; a=json.loads(tc["function"]["arguments"])
print("parent model",p["model"],"tokens",p["usage"]["total_tokens"],"-> call",a)
time.sleep(20)
c=post({"model":a["model"],"messages":[{"role":"user","content":a["prompt"]}],"max_tokens":50,"reasoning_effort":a["reasoning_effort"]})
print("child model",c.get("model"),"answer:",c["choices"][0]["message"]["content"] if "choices" in c else c)
time.sleep(20)
msgs+= [m,{"role":"tool","tool_call_id":tc["id"],"name":"subagent","content":c["choices"][0]["message"]["content"]}]
f=post({"model":"mistral-large-4","messages":msgs,"tools":[tool],"max_tokens":60,"reasoning_effort":"high"})
print("parent final:",f["choices"][0]["message"]["content"] if "choices" in f else f)
