import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { useState } from "react";
import { Shield, ArrowRight, Activity, Eye, Scale } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export const Route = createFileRoute("/")({
  component: SignIn,
});

function SignIn() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [pw, setPw] = useState("");

  function submit(e: React.FormEvent) {
    e.preventDefault();
    navigate({ to: "/dashboard" });
  }

  return (
    <div className="grid min-h-screen grid-cols-1 bg-background lg:grid-cols-2">
      {/* Left — brand panel */}
      <div className="relative hidden flex-col justify-between overflow-hidden border-r border-border bg-sidebar p-10 lg:flex">
        <div className="grid-bg pointer-events-none absolute inset-0 opacity-30" />
        <div className="absolute -left-32 top-1/3 h-96 w-96 rounded-full bg-accent/10 blur-3xl" />

        <div className="relative flex items-center gap-3">
          <div className="grid h-10 w-10 place-items-center rounded-md border border-border bg-secondary">
            <Shield className="h-5 w-5 text-accent" />
          </div>
          <div className="leading-tight">
            <div className="text-sm font-semibold">AI Crisis War Room</div>
            <div className="text-[10px] uppercase tracking-[0.2em] text-muted-foreground">Crisis Management OS</div>
          </div>
        </div>

        <div className="relative space-y-8">
          <div>
            <div className="text-[10px] uppercase tracking-[0.25em] text-accent">AI-Powered</div>
            <h1 className="mt-3 max-w-md text-4xl font-semibold leading-[1.05] tracking-tight text-grad">
              Command center for crisis response.
            </h1>
            <p className="mt-4 max-w-md text-sm leading-relaxed text-muted-foreground">
              Describe the crisis. Get severity scoring, stakeholder impact, risk
              modeling, and a prioritized response plan — across business, PR, legal, and ops.
              Powered by Multi-Agent AI and RAG.
            </p>
          </div>

          <div className="grid max-w-md grid-cols-3 gap-3">
            {[
              { icon: Activity, label: "Severity scoring" },
              { icon: Eye, label: "Stakeholder map" },
              { icon: Scale, label: "Multi-lens advice" },
            ].map((f) => (
              <div key={f.label} className="rounded-md border border-border bg-card/60 p-3">
                <f.icon className="h-4 w-4 text-accent" />
                <div className="mt-2 text-[11px] leading-tight text-muted-foreground">{f.label}</div>
              </div>
            ))}
          </div>
        </div>

        <div className="relative text-[11px] text-muted-foreground">
          Multi-Agent AI · RAG-powered · LangGraph Workflow
        </div>
      </div>

      {/* Right — form */}
      <div className="flex items-center justify-center p-6 sm:p-10">
        <div className="w-full max-w-sm">
          <div className="mb-8 lg:hidden">
            <div className="flex items-center gap-2.5">
              <div className="grid h-9 w-9 place-items-center rounded-md border border-border bg-secondary">
                <Shield className="h-4 w-4 text-accent" />
              </div>
              <div className="text-sm font-semibold">AI Crisis War Room</div>
            </div>
          </div>

          <div className="text-[10px] uppercase tracking-[0.2em] text-muted-foreground">
            Secure access
          </div>
          <h2 className="mt-2 text-2xl font-semibold tracking-tight">Sign in to War Room</h2>
          <p className="mt-1.5 text-sm text-muted-foreground">
            Enter your credentials to access the crisis dashboard.
          </p>

          <form onSubmit={submit} className="mt-8 space-y-4">
            <div className="space-y-1.5">
              <Label htmlFor="email" className="text-xs">Email</Label>
              <Input
                id="email"
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@example.com"
                className="h-10 bg-secondary/40"
              />
            </div>
            <div className="space-y-1.5">
              <div className="flex items-center justify-between">
                <Label htmlFor="pw" className="text-xs">Password</Label>
                <a className="text-[11px] text-muted-foreground hover:text-foreground" href="#">Forgot?</a>
              </div>
              <Input
                id="pw"
                type="password"
                required
                value={pw}
                onChange={(e) => setPw(e.target.value)}
                placeholder="••••••••"
                className="h-10 bg-secondary/40"
              />
            </div>

            <Button type="submit" className="group h-10 w-full bg-accent text-accent-foreground hover:bg-accent/90">
              Enter War Room
              <ArrowRight className="ml-1 h-4 w-4 transition-transform group-hover:translate-x-0.5" />
            </Button>
          </form>

          <div className="mt-6 flex items-center gap-3">
            <div className="h-px flex-1 bg-border" />
            <span className="text-[10px] uppercase tracking-[0.2em] text-muted-foreground">or</span>
            <div className="h-px flex-1 bg-border" />
          </div>

          <button
            onClick={() => navigate({ to: "/dashboard" })}
            className="mt-6 w-full rounded-md border border-border bg-secondary/40 px-4 py-2.5 text-sm font-medium hover:bg-secondary"
          >
            Continue with Google
          </button>

          <p className="mt-8 text-center text-[11px] text-muted-foreground">
            No account?{" "}
            <Link to="/dashboard" className="text-foreground underline-offset-4 hover:underline">
              Request access
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}