"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { z } from "zod";

import { AuthCard } from "@/components/auth-card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ApiError, apiRequest } from "@/lib/api";
import type { User } from "@/types/user";

const schema = z.object({
  email: z.email("Enter a valid administrator email"),
  password: z.string().min(1, "Enter your password").max(128),
  pin: z.string().min(4, "Enter the administrator PIN").max(64),
});

type AdminLoginValues = z.infer<typeof schema>;

export default function AdminLoginPage() {
  const router = useRouter();
  const queryClient = useQueryClient();
  const { register, handleSubmit, formState: { errors } } = useForm<AdminLoginValues>({ resolver: zodResolver(schema) });
  const login = useMutation({
    mutationFn: (values: AdminLoginValues) => apiRequest<User>("/auth/admin-login", { method: "POST", body: JSON.stringify(values) }),
    onSuccess: (user) => {
      queryClient.setQueryData(["current-user"], user);
      router.replace("/admin/students");
      router.refresh();
    },
  });
  return <AuthCard title="Administrator sign in" description="Enter your administrator account and private PIN." alternateHref="/login" alternateLabel="Return to student sign in"><form className="space-y-5" onSubmit={handleSubmit((values) => login.mutate(values))}><div><label htmlFor="admin-email" className="mb-2 block text-sm font-semibold">Email</label><Input id="admin-email" type="email" autoComplete="username" {...register("email")} />{errors.email && <p className="mt-1 text-sm text-red-700">{errors.email.message}</p>}</div><div><label htmlFor="admin-password" className="mb-2 block text-sm font-semibold">Password</label><Input id="admin-password" type="password" autoComplete="current-password" {...register("password")} />{errors.password && <p className="mt-1 text-sm text-red-700">{errors.password.message}</p>}</div><div><label htmlFor="admin-pin" className="mb-2 block text-sm font-semibold">Private PIN</label><Input id="admin-pin" type="password" inputMode="numeric" autoComplete="off" {...register("pin")} />{errors.pin && <p className="mt-1 text-sm text-red-700">{errors.pin.message}</p>}</div>{login.error && <p role="alert" className="rounded-lg bg-red-50 p-3 text-sm text-red-800">{login.error instanceof ApiError ? login.error.message : "Unable to sign in"}</p>}<Button type="submit" className="w-full" disabled={login.isPending}>{login.isPending ? "Signing in…" : "Sign in as administrator"}</Button></form></AuthCard>;
}
