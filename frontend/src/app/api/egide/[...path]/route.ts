import { cookies } from "next/headers";
import { NextRequest, NextResponse } from "next/server";

const UPSTREAM =
  process.env.EGIDE_API_INTERNAL_URL ||
  process.env.NEXT_PUBLIC_API_URL ||
  "http://localhost:8000/api/v1";
const TOKEN_COOKIE = "egide_token";

function buildUpstreamUrl(path: string[], request: NextRequest) {
  const upstream = new URL(`${UPSTREAM.replace(/\/$/, "")}/${path.join("/")}`);
  request.nextUrl.searchParams.forEach((value, key) => {
    upstream.searchParams.append(key, value);
  });
  return upstream;
}

async function proxy(request: NextRequest, ctx: { params: { path: string[] } }) {
  const upstream = buildUpstreamUrl(ctx.params.path ?? [], request);
  const cookieStore = cookies();
  const token = cookieStore.get(TOKEN_COOKIE)?.value;

  const headers = new Headers();
  const contentType = request.headers.get("content-type");
  if (contentType) headers.set("content-type", contentType);
  const accept = request.headers.get("accept");
  if (accept) headers.set("accept", accept);
  if (token) headers.set("authorization", `Bearer ${token}`);

  const init: RequestInit = {
    method: request.method,
    headers,
    cache: "no-store",
    redirect: "follow",
  };

  if (!["GET", "HEAD"].includes(request.method)) {
    init.body = await request.text();
  }

  const upstreamResponse = await fetch(upstream, init);
  const responseHeaders = new Headers();
  const responseContentType = upstreamResponse.headers.get("content-type");
  if (responseContentType) {
    responseHeaders.set("content-type", responseContentType);
  }

  return new NextResponse(upstreamResponse.body, {
    status: upstreamResponse.status,
    statusText: upstreamResponse.statusText,
    headers: responseHeaders,
  });
}

export async function GET(request: NextRequest, ctx: { params: { path: string[] } }) {
  return proxy(request, ctx);
}

export async function POST(request: NextRequest, ctx: { params: { path: string[] } }) {
  return proxy(request, ctx);
}

export async function PUT(request: NextRequest, ctx: { params: { path: string[] } }) {
  return proxy(request, ctx);
}

export async function PATCH(request: NextRequest, ctx: { params: { path: string[] } }) {
  return proxy(request, ctx);
}

export async function DELETE(request: NextRequest, ctx: { params: { path: string[] } }) {
  return proxy(request, ctx);
}
