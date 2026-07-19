import { useState, useEffect, useRef } from "react";
import { Mic, Send, RefreshCcw, Volume2 } from "lucide-react";
import api from '@/lib/api'

export function CopilotChat() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [messages, setMessages] = useState<{ role: 'user' | 'assistant'; text: string }[]>([]);
  const [lastUserMessage, setLastUserMessage] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [listening, setListening] = useState(false);
  const [voiceError, setVoiceError] = useState<string | null>(null);
  const [backendError, setBackendError] = useState<string | null>(null);
  const [speaking, setSpeaking] = useState(false);
  const [ttsError, setTtsError] = useState<string | null>(null);
  const recognitionRef = useRef<any>(null);
  const utteranceRef = useRef<SpeechSynthesisUtterance | null>(null);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.onresult = null;
        recognitionRef.current.onend = null;
        recognitionRef.current.onerror = null;
        recognitionRef.current.stop();
      }
      if (window.speechSynthesis) {
        window.speechSynthesis.cancel();
      }
    };
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }, [messages, loading]);

  const [suggestions, setSuggestions] = useState<string[]>([
    "How many employees are currently active?",
    "Show me this month's sales performance.",
    "What is the current inventory value?",
    "Give me a summary of open opportunities."
  ]);
  const [newSuggestion, setNewSuggestion] = useState("");

  const askAI = async (prompt?: string, clearInputImmediately = true) => {
    const message = prompt?.trim() ?? question.trim();
    if (!message || loading) return;

    setLastUserMessage(message);
    setBackendError(null);
    setTtsError(null);
    setVoiceError(null);
    setLoading(true);
    setMessages((current) => [...current, { role: 'user', text: message }]);
    setAnswer("");

    if (clearInputImmediately) {
      setQuestion("");
    }

    try {
      const response = await api.post('/copilot/chat', { message });
      const reply = response.data.reply?.content || "No response received.";
      setAnswer(reply);
      setMessages((current) => [...current, { role: 'assistant', text: reply }]);
    } catch (err) {
      const errorMessage = "Unable to connect to AI backend.";
      setBackendError(errorMessage);
      setAnswer(errorMessage);
      setMessages((current) => [...current, { role: 'assistant', text: errorMessage }]);
    } finally {
      if (!clearInputImmediately) {
        setQuestion("");
      }
      setLoading(false);
    }
  };

  const handleSuggestionClick = (suggestion: string) => {
    askAI(suggestion);
  };

  const handleAddSuggestion = () => {
    const trimmed = newSuggestion.trim();
    if (!trimmed) return;

    setSuggestions((current) => [trimmed, ...current]);
    setNewSuggestion("");
  };

  const speakAnswer = () => {
    if (!answer.trim()) return;
    if (!("speechSynthesis" in window)) {
      setTtsError("Text-to-speech is not supported in this browser.");
      return;
    }

    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(answer);
    utterance.onend = () => {
      setSpeaking(false);
      utteranceRef.current = null;
    };
    utterance.onerror = () => {
      setTtsError("Unable to speak the response.");
      setSpeaking(false);
      utteranceRef.current = null;
    };

    utteranceRef.current = utterance;
    setTtsError(null);
    setSpeaking(true);
    window.speechSynthesis.speak(utterance);
  };

  const stopSpeaking = () => {
    if (window.speechSynthesis) {
      window.speechSynthesis.cancel();
    }
    setSpeaking(false);
    utteranceRef.current = null;
  };

  const stopListening = () => {
    recognitionRef.current?.stop();
    setListening(false);
  };

  const startVoiceCommand = () => {
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SpeechRecognition) {
      setVoiceError("Voice recognition is not supported in this browser.");
      return;
    }

    setVoiceError(null);
    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onresult = (event: any) => {
      const transcript = event.results?.[0]?.[0]?.transcript?.trim();
      if (transcript) {
        setQuestion(transcript);
        askAI(transcript, false);
      }
      setListening(false);
      recognitionRef.current = null;
    };

    recognition.onerror = (event: any) => {
      setVoiceError(event?.error || "Speech recognition failed.");
      setListening(false);
      recognitionRef.current = null;
    };

    recognition.onend = () => {
      setListening(false);
      recognitionRef.current = null;
    };

    recognitionRef.current = recognition;
    recognition.start();
    setListening(true);
  };

  return (
    <div className="min-h-screen pb-10">
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
        <div className="card mb-6 overflow-hidden rounded-[2rem] border border-slate-200/80 bg-slate-950/95 px-6 py-8 text-white shadow-2xl shadow-slate-950/20">
          <div className="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
            <div className="space-y-3">
              <p className="text-xs uppercase tracking-[0.3em] text-indigo-300">ERP Copilot</p>
              <h1 className="text-4xl font-semibold tracking-tight">ERP GPT Copilot</h1>
              <p className="max-w-2xl text-sm text-slate-300">Chat with your ERP assistant for faster decisions, summaries, insights, and workflow guidance.</p>
            </div>
            <button
              onClick={() => {
                setMessages([])
                setLastUserMessage(null)
                setAnswer("")
                setBackendError(null)
                setVoiceError(null)
                setTtsError(null)
              }}
              className="inline-flex items-center justify-center rounded-2xl bg-white/95 px-5 py-3 text-sm font-semibold text-slate-950 shadow-sm shadow-slate-950/10 transition hover:bg-white"
            >
              Clear chat
            </button>
          </div>
        </div>

        <div className="grid gap-6 xl:grid-cols-[1.5fr_0.9fr]">
          <div className="card rounded-[2rem] border border-slate-200/80 bg-white/95 p-6 shadow-xl">
            <div className="mb-5 rounded-[1.75rem] border border-slate-200 bg-slate-950/95 p-5 text-slate-100 shadow-inner shadow-slate-950/10">
              <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                <div>
                  <p className="text-sm font-semibold uppercase tracking-[0.25em] text-indigo-300">Live chat</p>
                  <p className="mt-2 text-sm text-slate-400">Ask the model anything about your ERP data and processes.</p>
                </div>
                <div className="text-right text-xs text-slate-500">{messages.length} messages</div>
              </div>
            </div>

            <div className="max-h-[55vh] space-y-3 overflow-y-auto pr-1">
              {messages.length === 0 ? (
                <div className="flex min-h-[220px] items-center justify-center rounded-[1.75rem] border border-dashed border-slate-200 bg-slate-50">
                  <p className="text-sm text-slate-500">Start by typing a question, tapping a suggestion, or using voice input.</p>
                </div>
              ) : (
                messages.map((message, index) => (
                  <div
                    key={`${message.role}-${index}`}
                    className={`mb-3 flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div className={`max-w-[88%] rounded-[1.75rem] px-5 py-4 shadow-sm ${message.role === 'user' ? 'bg-indigo-600 text-white' : 'bg-slate-100 text-slate-950 border border-slate-200'}`}>
                      <p className="text-sm leading-6 whitespace-pre-wrap">{message.text}</p>
                    </div>
                  </div>
                ))
              )}
              <div ref={messagesEndRef} />
            </div>

            <form
              onSubmit={(event) => {
                event.preventDefault()
                askAI()
              }}
              className="mt-4 rounded-[1.75rem] border border-slate-200 bg-slate-100 px-3 py-3 shadow-sm"
            >
              <div className="flex flex-wrap items-center gap-3">
                <textarea
                  className="min-h-[110px] flex-1 resize-none rounded-[1.5rem] border border-slate-300 bg-white px-4 py-3 text-sm text-slate-900 shadow-sm outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200"
                  rows={2}
                  placeholder="Type your question or press the mic to speak..."
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                />

                <div className="flex flex-wrap items-center gap-2">
                  <button
                    type="submit"
                    disabled={!question.trim() || loading}
                    className="rounded-full border border-slate-300 bg-indigo-600 px-4 py-3 text-white transition hover:bg-indigo-700 disabled:bg-slate-400 disabled:cursor-not-allowed"
                    aria-label={loading ? 'Thinking' : 'Send message'}
                  >
                    {loading ? (
                      <span className="text-sm">…</span>
                    ) : (
                      <Send className="w-5 h-5" />
                    )}
                  </button>
                  <button
                    type="button"
                    onClick={() => lastUserMessage && askAI(lastUserMessage)}
                    disabled={!lastUserMessage || loading}
                    className="rounded-full border border-slate-300 bg-slate-100 px-4 py-3 text-slate-900 transition hover:bg-slate-200 disabled:bg-slate-200 disabled:cursor-not-allowed"
                    aria-label="Regenerate response"
                  >
                    <RefreshCcw className="w-5 h-5" />
                  </button>
                  <button
                    type="button"
                    onClick={() => {
                      if (listening) {
                        stopListening()
                        return
                      }
                      startVoiceCommand()
                    }}
                    className={`rounded-full border border-slate-300 bg-slate-950 px-4 py-3 text-white transition ${listening ? 'bg-emerald-600' : 'hover:bg-slate-800'}`}
                    aria-label={listening ? 'Stop listening' : 'Voice command'}
                  >
                    <Mic className="w-5 h-5" />
                  </button>
                  <button
                    type="button"
                    onClick={speaking ? stopSpeaking : speakAnswer}
                    disabled={!answer.trim() && !speaking}
                    className={`rounded-full border border-slate-300 bg-indigo-600 px-4 py-3 text-white transition ${speaking ? 'bg-slate-700' : 'hover:bg-indigo-700'} disabled:bg-slate-400 disabled:cursor-not-allowed`}
                    aria-label={speaking ? 'Stop speaking' : 'Speak response'}
                  >
                    <Volume2 className="w-5 h-5" />
                  </button>
                </div>
              </div>
            </form>
          </div>

          <aside className="card rounded-[2rem] border border-slate-200/80 bg-slate-50 p-6 shadow-xl">
            <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <h2 className="text-lg font-semibold text-slate-950">Suggested questions</h2>
                <p className="mt-1 text-sm text-slate-500">Tap a prompt or add one to keep the conversation moving.</p>
              </div>
              <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-end">
                <input
                  type="text"
                  value={newSuggestion}
                  onChange={(e) => setNewSuggestion(e.target.value)}
                  placeholder="Add a new suggestion"
                  className="input w-full sm:w-72"
                />
                <button
                  onClick={handleAddSuggestion}
                  className="btn-primary w-full sm:w-auto"
                >
                  Add
                </button>
              </div>
            </div>

            <div className="mt-5 space-y-3">
              {suggestions.map((suggestion) => (
                <button
                  key={suggestion}
                  onClick={() => handleSuggestionClick(suggestion)}
                  className="w-full rounded-full border border-slate-300 bg-white px-4 py-3 text-left text-sm font-medium text-slate-950 transition hover:border-indigo-500 hover:bg-indigo-50"
                >
                  {suggestion}
                </button>
              ))}
            </div>

            <div className="mt-6 rounded-[1.5rem] bg-slate-100 p-4 text-sm text-slate-700">
              <p className="font-semibold text-slate-900">Quick tips</p>
              <ul className="mt-3 list-disc list-inside space-y-2">
                <li>Use short queries for faster answers.</li>
                <li>Follow up directly after a response.</li>
                <li>Tap regenerate for alternate summaries.</li>
              </ul>
            </div>
          </aside>
        </div>

        <div className="mt-6 space-y-3 text-sm text-slate-700">
          {voiceError ? (
            <div className="rounded-2xl border border-rose-200 bg-rose-50 p-4 text-rose-700">
              <p className="font-semibold">{voiceError}</p>
              <ul className="mt-2 list-disc list-inside space-y-1">
                <li>Allow microphone access in browser settings.</li>
                <li>Speak clearly and wait for input to finish.</li>
                <li>Try typing if voice recognition fails.</li>
              </ul>
            </div>
          ) : listening ? (
            <div className="rounded-2xl bg-slate-900/5 p-4 text-slate-700">Listening... speak now.</div>
          ) : null}

          {ttsError ? (
            <div className="rounded-2xl border border-rose-200 bg-rose-50 p-4 text-rose-700">
              <p className="font-semibold">{ttsError}</p>
              <p>Try a different browser or refresh the page.</p>
            </div>
          ) : speaking ? (
            <div className="rounded-2xl bg-slate-900/5 p-4 text-slate-700">Speaking response...</div>
          ) : null}

          {backendError ? (
            <div className="rounded-2xl border border-rose-200 bg-rose-50 p-4 text-rose-700">
              <p className="font-semibold">{backendError}</p>
              <ul className="mt-2 list-disc list-inside space-y-1">
                <li>Check that the AI backend is running.</li>
                <li>Verify your internet connection.</li>
                <li>Try again in a few seconds.</li>
              </ul>
            </div>
          ) : null}
        </div>
      </div>
    </div>
  )
}
