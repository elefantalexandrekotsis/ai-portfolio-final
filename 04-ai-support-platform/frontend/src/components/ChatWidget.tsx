"use client";
import { useState, useRef, useEffect } from "react";
interface Msg { id: string; role: "user"|"assistant"; content: string; }
export function ChatWidget() {
  const [msgs, setMsgs] = useState<Msg[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [convId, setConvId] = useState<string|null>(null);
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => { ref.current?.scrollIntoView({behavior:"smooth"}); }, [msgs]);
  const send = async () => {
    if (!input.trim()||loading) return;
    setMsgs(p => [...p, {id:crypto.randomUUID(),role:"user",content:input}]);
    setInput(""); setLoading(true);
    try {
      const r = await fetch(process.env.NEXT_PUBLIC_API_URL+"/api/v1/chat/message",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({message:input,conversation_id:convId,user_id:"demo"})});
      const d = await r.json();
      if(!convId) setConvId(d.conversation_id);
      setMsgs(p => [...p, {id:crypto.randomUUID(),role:"assistant",content:d.response}]);
    } catch { setMsgs(p => [...p, {id:crypto.randomUUID(),role:"assistant",content:"Error occurred."}]); }
    finally { setLoading(false); }
  };
  return (
    <div className="flex flex-col h-[600px] w-full max-w-2xl mx-auto border rounded-2xl shadow-lg bg-white">
      <div className="bg-blue-600 px-6 py-4"><h2 className="text-white font-semibold">AI Support</h2></div>
      <div className="flex-1 overflow-y-auto p-4 space-y-3 bg-gray-50">
        {msgs.map(m=><div key={m.id} className={"flex "+(m.role==="user"?"justify-end":"justify-start")}><div className={"max-w-[80%] rounded-2xl px-4 py-2 text-sm "+(m.role==="user"?"bg-blue-600 text-white":"bg-white border shadow-sm")}>{m.content}</div></div>)}
        {loading&&<p className="text-gray-400 text-sm">Thinking...</p>}
        <div ref={ref}/>
      </div>
      <div className="border-t p-4 flex gap-3">
        <input value={input} onChange={e=>setInput(e.target.value)} onKeyDown={e=>e.key==="Enter"&&send()} placeholder="Type message..." className="flex-1 px-4 py-3 border rounded-xl text-sm"/>
        <button onClick={send} disabled={loading||!input.trim()} className="px-6 py-3 bg-blue-600 text-white rounded-xl disabled:opacity-50 text-sm font-medium">Send</button>
      </div>
    </div>);
}
