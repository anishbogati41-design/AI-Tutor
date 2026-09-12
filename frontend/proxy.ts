import { NextRequest, NextResponse } from "next/server";

const SESSION_COOKIE =
  process.env.SESSION_COOKIE_NAME ?? "adaptive_session";

export function proxy(request: NextRequest) {
  const hasSession = request.cookies.has(SESSION_COOKIE);
  const isAuthRoute =
    request.nextUrl.pathname === "/login" ||
    request.nextUrl.pathname === "/admin-login" ||
    request.nextUrl.pathname === "/register";

  const isProtectedRoute =
    request.nextUrl.pathname.startsWith("/profile") ||
    request.nextUrl.pathname.startsWith("/dashboard") ||
    request.nextUrl.pathname.startsWith("/lessons") ||
    request.nextUrl.pathname.startsWith("/practice") ||
    request.nextUrl.pathname.startsWith("/chat") ||
    request.nextUrl.pathname.startsWith("/study-plan") ||
    (request.nextUrl.pathname.startsWith("/admin") && !isAuthRoute);

  if (isProtectedRoute && !hasSession) {
    return NextResponse.redirect(new URL("/login", request.url));
  }
  return NextResponse.next();
}

export const config = {
  matcher: [
    "/login",
    "/admin-login",
    "/register",
    "/profile/:path*",
    "/lessons/:path*",
    "/dashboard/:path*",
    "/practice/:path*",
    "/chat/:path*",
    "/study-plan/:path*",
    "/admin/:path*",
  ],
};
