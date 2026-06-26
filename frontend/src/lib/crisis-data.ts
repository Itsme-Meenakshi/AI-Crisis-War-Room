export type Perspective = "Business" | "PR" | "Legal" | "Operations";

export interface CrisisAction {
  time: string;
  title: string;
  owner: Perspective;
  priority: "P0" | "P1" | "P2";
}

export interface Stakeholder {
  name: string;
  impact: number; // 0-100
  sentiment: "negative" | "neutral" | "positive";
}

export interface RiskItem {
  category: string;
  likelihood: number; // 0-100
  impact: number; // 0-100
}

export interface PerspectiveInsight {
  perspective: Perspective;
  summary: string;
  recommendations: string[];
}

export interface CrisisAnalysis {
  id: string;
  title: string;
  description: string;
  createdAt: string;
  status: "active" | "monitoring" | "resolved";
  severity: number; // 0-100
  category: string;
  stakeholders: Stakeholder[];
  risks: RiskItem[];
  perspectives: PerspectiveInsight[];
  timeline: CrisisAction[];
  attachments: { name: string; size: number }[];
}

const STORAGE_KEY = "acwr.crises.v1";

export async function loadCrises(): Promise<CrisisAnalysis[]> {
  try {
    const response = await fetch("http://localhost:8000/api/crises");
    if (response.ok) {
      const data = await response.json();
      return data as CrisisAnalysis[];
    }
  } catch (err) {
    console.error("Failed to load crises from backend, falling back to localStorage:", err);
  }

  if (typeof window === "undefined") return seed;
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(seed));
      return seed;
    }
    return JSON.parse(raw) as CrisisAnalysis[];
  } catch {
    return seed;
  }
}

export function saveCrises(list: CrisisAnalysis[]) {
  if (typeof window === "undefined") return;
  localStorage.setItem(STORAGE_KEY, JSON.stringify(list));
}

export async function getCrisis(id: string): Promise<CrisisAnalysis | undefined> {
  try {
    const response = await fetch(`http://localhost:8000/api/crises/${id}`);
    if (response.ok) {
      const data = await response.json();
      return data as CrisisAnalysis;
    }
  } catch (err) {
    console.error(`Failed to fetch crisis ${id} from backend, falling back to localStorage:`, err);
  }

  const list = await loadCrises();
  return list.find((c) => c.id === id);
}

// Deterministic mock "AI" analyzer from description text
export function analyzeCrisis(input: {
  title: string;
  description: string;
  files: { name: string; size: number }[];
}): CrisisAnalysis {
  const text = (input.title + " " + input.description).toLowerCase();
  const hash = [...text].reduce((a, c) => (a * 31 + c.charCodeAt(0)) | 0, 7);
  const r = (n: number) => Math.abs((hash >> n) % 100);

  const keywords: Record<string, number> = {
    breach: 30, leak: 25, lawsuit: 20, fire: 25, recall: 22,
    outage: 18, fraud: 28, death: 35, injury: 22, hack: 30,
    layoff: 15, strike: 18, regulator: 20, viral: 15, scandal: 25,
  };
  let bonus = 0;
  for (const k in keywords) if (text.includes(k)) bonus += keywords[k];
  const severity = Math.min(98, 35 + (r(2) % 25) + bonus);

  const category =
    text.includes("cyber") || text.includes("hack") || text.includes("breach")
      ? "Cybersecurity"
      : text.includes("recall") || text.includes("product")
      ? "Product Safety"
      : text.includes("legal") || text.includes("lawsuit")
      ? "Legal & Regulatory"
      : text.includes("pr") || text.includes("media") || text.includes("social")
      ? "Reputation"
      : "Operational";

  return {
    id: "c_" + Math.random().toString(36).slice(2, 9),
    title: input.title || "Untitled Crisis",
    description: input.description,
    createdAt: new Date().toISOString(),
    status: "active",
    severity,
    category,
    attachments: input.files,
    stakeholders: [
      { name: "Customers", impact: 60 + (r(3) % 35), sentiment: "negative" },
      { name: "Employees", impact: 40 + (r(5) % 40), sentiment: "neutral" },
      { name: "Investors", impact: 50 + (r(7) % 45), sentiment: "negative" },
      { name: "Regulators", impact: 30 + (r(9) % 50), sentiment: "neutral" },
      { name: "Media / Press", impact: 55 + (r(11) % 40), sentiment: "negative" },
      { name: "Partners", impact: 25 + (r(13) % 40), sentiment: "neutral" },
    ],
    risks: [
      { category: "Financial", likelihood: 60 + (r(2) % 35), impact: 55 + (r(4) % 40) },
      { category: "Reputation", likelihood: 70 + (r(6) % 25), impact: 65 + (r(8) % 30) },
      { category: "Legal", likelihood: 40 + (r(10) % 45), impact: 60 + (r(12) % 35) },
      { category: "Operational", likelihood: 50 + (r(14) % 40), impact: 50 + (r(16) % 40) },
      { category: "Compliance", likelihood: 35 + (r(18) % 50), impact: 55 + (r(20) % 40) },
    ],
    perspectives: [
      {
        perspective: "Business",
        summary:
          "Short-term revenue exposure is moderate. Prioritize customer retention messaging and protect top-100 accounts.",
        recommendations: [
          "Brief executive team within 1 hour",
          "Freeze non-critical marketing campaigns",
          "Activate retention task force for tier-1 accounts",
        ],
      },
      {
        perspective: "PR",
        summary:
          "Public sentiment is trending negative. A factual, empathetic statement within the next 2 hours is critical to control narrative.",
        recommendations: [
          "Publish holding statement on owned channels",
          "Brief key journalists with verified facts",
          "Monitor sentiment hourly across X, LinkedIn, news",
        ],
      },
      {
        perspective: "Legal",
        summary:
          "Disclosure obligations may apply. Preserve evidence, restrict internal commentary, and prepare regulator notifications.",
        recommendations: [
          "Issue litigation hold to all involved teams",
          "Engage outside counsel on disclosure timing",
          "Draft regulator notification template",
        ],
      },
      {
        perspective: "Operations",
        summary:
          "Containment is the priority. Isolate affected systems / sites and stand up an incident command with 30-min checkpoints.",
        recommendations: [
          "Activate incident command structure",
          "Isolate affected systems / facilities",
          "Establish 30-min status cadence",
        ],
      },
    ],
    timeline: [
      { time: "0–1h", title: "Activate war room & assign incident commander", owner: "Operations", priority: "P0" },
      { time: "0–2h", title: "Publish holding statement to customers & media", owner: "PR", priority: "P0" },
      { time: "1–3h", title: "Issue litigation hold & assess disclosure duties", owner: "Legal", priority: "P0" },
      { time: "2–6h", title: "Brief board and top-100 customers", owner: "Business", priority: "P1" },
      { time: "6–24h", title: "Root-cause investigation & containment report", owner: "Operations", priority: "P1" },
      { time: "24–72h", title: "Public update with corrective actions", owner: "PR", priority: "P2" },
    ],
  };
}

const seed: CrisisAnalysis[] = [
  {
    id: "c_demo1",
    title: "Customer data exposure — analytics vendor",
    description: "Third-party analytics vendor reported unauthorized access affecting an estimated 18k customer records.",
    createdAt: new Date(Date.now() - 1000 * 60 * 60 * 6).toISOString(),
    status: "active",
    severity: 82,
    category: "Cybersecurity",
    attachments: [],
    stakeholders: [
      { name: "Customers", impact: 88, sentiment: "negative" },
      { name: "Regulators", impact: 76, sentiment: "neutral" },
      { name: "Investors", impact: 64, sentiment: "negative" },
      { name: "Employees", impact: 42, sentiment: "neutral" },
      { name: "Media / Press", impact: 71, sentiment: "negative" },
      { name: "Partners", impact: 38, sentiment: "neutral" },
    ],
    risks: [
      { category: "Financial", likelihood: 72, impact: 78 },
      { category: "Reputation", likelihood: 86, impact: 82 },
      { category: "Legal", likelihood: 80, impact: 84 },
      { category: "Operational", likelihood: 55, impact: 60 },
      { category: "Compliance", likelihood: 78, impact: 80 },
    ],
    perspectives: [],
    timeline: [],
  },
  {
    id: "c_demo2",
    title: "Manufacturing line halt — Plant 4",
    description: "Unplanned shutdown of Line B affecting shipment SLAs for the Northeast region.",
    createdAt: new Date(Date.now() - 1000 * 60 * 60 * 26).toISOString(),
    status: "monitoring",
    severity: 58,
    category: "Operational",
    attachments: [],
    stakeholders: [], risks: [], perspectives: [], timeline: [],
  },
  {
    id: "c_demo3",
    title: "Executive social media controversy",
    description: "Public statement by SVP gaining negative traction; trending in two markets.",
    createdAt: new Date(Date.now() - 1000 * 60 * 60 * 70).toISOString(),
    status: "resolved",
    severity: 44,
    category: "Reputation",
    attachments: [],
    stakeholders: [], risks: [], perspectives: [], timeline: [],
  },
];
