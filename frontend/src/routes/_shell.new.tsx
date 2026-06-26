import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { useState } from "react";
import { Upload, X, Siren, FileText, Image as ImageIcon, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { analyzeCrisis, loadCrises, saveCrises } from "@/lib/crisis-data";

export const Route = createFileRoute("/_shell/new")({
  head: () => ({
    meta: [
      { title: "Declare crisis — AI Crisis War Room" },
      { name: "description", content: "Describe a crisis and let AI generate severity, risks, and a response plan." },
    ],
  }),
  component: NewCrisis,
});

function NewCrisis() {
  const navigate = useNavigate();
  const [title, setTitle] = useState("");
  const [desc, setDesc] = useState("");
  const [scope, setScope] = useState("Regional");
  const [files, setFiles] = useState<File[]>([]);
  const [submitting, setSubmitting] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  function onFiles(list: FileList | null) {
    if (!list) return;
    setFiles((f) => [...f, ...Array.from(list)].slice(0, 8));
  }

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setSubmitting(true);
    setErrorMsg(null);
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 3 * 60 * 1000); // 3-min timeout
      const response = await fetch("http://localhost:8000/api/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title,
          description: desc,
          files: files.map((f) => ({ name: f.name, size: f.size })),
        }),
        signal: controller.signal,
      });
      clearTimeout(timeoutId);

      if (!response.ok) {
        const errData = await response.json().catch(() => ({}));
        const detail = errData?.detail ?? response.statusText;
        throw new Error(detail);
      }

      const analysis = await response.json();
      // loadCrises is async — must await it
      const all = await loadCrises();
      saveCrises([analysis, ...all]);
      navigate({ to: "/analysis/$id", params: { id: analysis.id } });
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : String(err);
      console.error("Failed to run AI analysis:", msg);

      // Only fall back to simulation for network/connection errors
      const isNetworkErr = msg.toLowerCase().includes("failed to fetch") ||
        msg.toLowerCase().includes("network") ||
        msg.toLowerCase().includes("timeout");

      if (isNetworkErr) {
        const analysis = analyzeCrisis({
          title,
          description: desc,
          files: files.map((f) => ({ name: f.name, size: f.size })),
        });
        const all = await loadCrises();
        saveCrises([analysis, ...all]);
        navigate({ to: "/analysis/$id", params: { id: analysis.id } });
      } else {
        // Surface backend errors directly so user can see what's wrong
        setErrorMsg(msg);
        setSubmitting(false);
        return;
      }
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="mx-auto max-w-4xl space-y-8 p-6 lg:p-8">
      <div>
        <div className="text-[10px] uppercase tracking-[0.2em] text-accent">Intake</div>
        <h1 className="mt-1.5 text-3xl font-semibold tracking-tight">Declare a new crisis</h1>
        <p className="mt-1.5 text-sm text-muted-foreground">
          Describe what's happening. The faster and more specific your input, the sharper the analysis.
        </p>
      </div>

      <form onSubmit={submit} className="space-y-6">
        <div className="panel p-6 space-y-5">
          <div className="space-y-1.5">
            <Label htmlFor="title" className="text-xs uppercase tracking-wider text-muted-foreground">
              Incident title
            </Label>
            <Input
              id="title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="e.g. Customer data exposure via vendor"
              required
              className="h-11 bg-secondary/40 text-base"
            />
          </div>

          <div className="space-y-1.5">
            <Label htmlFor="desc" className="text-xs uppercase tracking-wider text-muted-foreground">
              What's happening?
            </Label>
            <Textarea
              id="desc"
              value={desc}
              onChange={(e) => setDesc(e.target.value)}
              placeholder="Describe the situation, what's known and unknown, who's affected, and any actions already taken. Include keywords like 'breach', 'recall', 'lawsuit' for better classification."
              required
              rows={7}
              className="bg-secondary/40 resize-none"
            />
            <div className="flex justify-between text-[11px] text-muted-foreground">
              <span>Confidential — encrypted at rest</span>
              <span className="tabular-nums">{desc.length} chars</span>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-1.5">
              <Label className="text-xs uppercase tracking-wider text-muted-foreground">Scope</Label>
              <div className="flex gap-1.5">
                {["Local", "Regional", "Global"].map((s) => (
                  <button
                    type="button" key={s} onClick={() => setScope(s)}
                    className={`flex-1 rounded-md border px-3 py-2 text-xs font-medium transition ${
                      scope === s ? "border-accent bg-accent/10 text-foreground" : "border-border text-muted-foreground hover:bg-secondary"
                    }`}
                  >{s}</button>
                ))}
              </div>
            </div>
            <div className="space-y-1.5">
              <Label className="text-xs uppercase tracking-wider text-muted-foreground">Declared</Label>
              <div className="flex h-[38px] items-center rounded-md border border-border bg-secondary/40 px-3 text-sm tabular-nums">
                {new Date().toLocaleString()}
              </div>
            </div>
          </div>
        </div>

        {/* Uploads */}
        <div className="panel p-6">
          <div className="mb-3">
            <Label className="text-xs uppercase tracking-wider text-muted-foreground">Evidence (optional)</Label>
            <p className="mt-1 text-xs text-muted-foreground">Photos, screenshots, PDFs, logs. Max 8 files.</p>
          </div>

          <label className="flex cursor-pointer flex-col items-center justify-center gap-2 rounded-md border border-dashed border-border bg-secondary/20 py-10 text-sm text-muted-foreground hover:bg-secondary/40">
            <Upload className="h-5 w-5" />
            <span><span className="text-foreground">Click to upload</span> or drag and drop</span>
            <span className="text-[11px]">PNG, JPG, PDF, LOG up to 25MB each</span>
            <input type="file" multiple className="hidden" onChange={(e) => onFiles(e.target.files)} />
          </label>

          {files.length > 0 && (
            <div className="mt-4 grid grid-cols-1 gap-2 sm:grid-cols-2">
              {files.map((f, i) => {
                const isImg = f.type.startsWith("image/");
                return (
                  <div key={i} className="flex items-center gap-3 rounded-md border border-border bg-card/40 p-2.5">
                    <div className="grid h-9 w-9 place-items-center rounded-md bg-secondary">
                      {isImg ? <ImageIcon className="h-4 w-4 text-accent" /> : <FileText className="h-4 w-4 text-accent" />}
                    </div>
                    <div className="min-w-0 flex-1">
                      <div className="truncate text-xs font-medium">{f.name}</div>
                      <div className="text-[10px] text-muted-foreground">{(f.size / 1024).toFixed(1)} KB</div>
                    </div>
                    <button
                      type="button"
                      onClick={() => setFiles(files.filter((_, idx) => idx !== i))}
                      className="rounded p-1 text-muted-foreground hover:bg-secondary hover:text-foreground"
                    ><X className="h-3.5 w-3.5" /></button>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {errorMsg && (
          <div className="rounded-md border border-destructive/40 bg-destructive/10 px-4 py-3 text-sm text-destructive">
            <span className="font-semibold">Analysis failed: </span>{errorMsg}
          </div>
        )}

        <div className="flex items-center justify-end gap-2">
          <Button type="button" variant="ghost" onClick={() => navigate({ to: "/dashboard" })}>
            Cancel
          </Button>
          <Button
            type="submit"
            disabled={submitting || !title || !desc}
            className="bg-accent text-accent-foreground hover:bg-accent/90"
          >
            {submitting ? (
              <><Loader2 className="mr-2 h-4 w-4 animate-spin" /> Analyzing situation…</>
            ) : (
              <><Siren className="mr-2 h-4 w-4" /> Run AI analysis</>
            )}
          </Button>

        </div>
      </form>
    </div>
  );
}
