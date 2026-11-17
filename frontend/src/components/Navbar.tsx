import React from 'react';
import { Sparkles, Cpu, Layers, BookOpen, AlertCircle, CheckCircle2 } from 'lucide-react';

interface NavbarProps {
  apiStatus: {
    configured: boolean;
    model: string;
    faqsCount: number;
  };
  activePageTitle: string;
}

export const Navbar: React.FC<NavbarProps> = ({ apiStatus, activePageTitle }) => {
  return (
    <header className="h-16 border-b border-slate-800/80 bg-slate-950/80 backdrop-blur-md px-6 flex items-center justify-between sticky top-0 z-30">
      <div className="flex items-center gap-3">
        <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-cyan-600 via-indigo-600 to-violet-600 p-[1px] flex items-center justify-center shadow-lg shadow-cyan-950/50">
          <div className="w-full h-full bg-slate-950 rounded-[11px] flex items-center justify-center">
            <Cpu className="w-5 h-5 text-cyan-400" />
          </div>
        </div>
        <div>
          <div className="flex items-center gap-2">
            <h1 className="font-bold tracking-tight text-white text-base">ARCHITECTURE LAB</h1>
            <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-cyan-950/80 text-cyan-400 border border-cyan-800/50 font-semibold">
              AI FOUNDATIONS
            </span>
          </div>
          <p className="text-[11px] text-slate-400 font-medium">
            Comparative Chatbot Study: Rules vs Retrieval vs LLM RAG
          </p>
        </div>
      </div>

      <div className="flex items-center gap-4">
        {/* Knowledge Base Counter */}
        <div className="hidden sm:flex items-center gap-1.5 text-xs text-slate-300 bg-slate-900/90 border border-slate-800 px-3 py-1.5 rounded-lg">
          <BookOpen className="w-3.5 h-3.5 text-cyan-400" />
          <span>Demo Knowledge Base:</span>
          <span className="font-mono font-semibold text-cyan-300">{apiStatus.faqsCount} FAQs</span>
        </div>

        {/* Gemini API Status Badge */}
        <div className={`flex items-center gap-2 text-xs px-3 py-1.5 rounded-lg border ${
          apiStatus.configured 
            ? 'bg-emerald-950/40 text-emerald-300 border-emerald-800/50' 
            : 'bg-amber-950/40 text-amber-300 border-amber-800/50'
        }`}>
          <div className={`w-2 h-2 rounded-full ${apiStatus.configured ? 'bg-emerald-400 animate-pulse' : 'bg-amber-400'}`} />
          <span className="font-medium">
            {apiStatus.configured ? `Gemini API: Live (${apiStatus.model})` : 'Gemini API: Not Configured'}
          </span>
          {apiStatus.configured ? (
            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
          ) : (
            <AlertCircle className="w-3.5 h-3.5 text-amber-400" />
          )}
        </div>
      </div>
    </header>
  );
};
