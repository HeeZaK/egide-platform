import { NextRequest, NextResponse } from "next/server";

export const dynamic = "force-dynamic";

const backendBase = () =>
  (process.env.EGIDE_API_URL ?? "http://127.0.0.1:8000").replace(/\/$/, "");

async function proxy(req: NextRequest, pathParts: string[]) {
  const suffix = pathParts.join("/");
  const target = `${backendBase()}/api/${suffix}${req.nextUrl.search}`;

  const token = req.cookies.get("egide_token")?.value;
  const headers = new Headers();
  const contentType = req.headers.get("content-type");
  if (contentType) {
    headers.set("content-type", contentType);
  }
  if (token) {
    headers.set("authorization", `Bearer ${token}`);
  }

  const hasBody = !["GET", "HEAD"].includes(req.method);
  const init: RequestInit = {
    method: req.method,
    headers,
    body: hasBody ? await req.text() : undefined,
  };

  const res = await fetch(target, init);
  const out = new NextResponse(await res.arrayBuffer(), { status: res.status });
  const outCt = res.headers.get("content-type");
  if (outCt) {
    out.headers.set("content-type", outCt);
  }
  return out;
}

type Ctx = { params: { path: string[] } };

export async function GET(req: NextRequest, ctx: Ctx) {
  return proxy(req, ctx.params.path);
}

export async function POST(req: NextRequest, ctx: Ctx) {
  return proxy(req, ctx.params.path);
}

export async function PUT(req: NextRequest, ctx: Ctx) {
  return proxy(req, ctx.params.path);
}

export async function PATCH(req: NextRequest, ctx: Ctx) {
  return proxy(req, ctx.params.path);
}

export async function DELETE(req: NextRequest, ctx: Ctx) {
  return proxy(req, ctx.params.path);
}
