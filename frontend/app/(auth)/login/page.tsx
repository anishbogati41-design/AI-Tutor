"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { z } from "zod";

import { AuthCard } from "@/components/auth-card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ApiError, apiRequest } from "@/lib/api";
import type { User } from "@/types/user";

const schema = z.object({
  email: z.email("Enter a valid email address"),
  password: z.string().min(1, "Enter your password").max(128),
});

type LoginValues = z.infer<typeof schema>;

export default function LoginPage() {
  const router = useRouter();
  const queryClient = useQueryClient();
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginValues>({ resolver: zodResolver(schema) });

  const login = useMutation({
    mutationFn: (values: LoginValues) =>
      apiRequest<User>("/auth/login", {
        method: "POST",
        body: JSON.stringify(values),
      }),
    onSuccess: (user) => {
      queryClient.setQueryData(["current-user"], user);
      router.replace("/dashboard");
      router.refresh();
    },
  });

  return (
    <AuthCard
      title="Welcome back"
      description="Sign in to continue your learning."
      alternateHref="/register"
      alternateLabel="Need an account? Register"
    >
      <form
        className="space-y-5"
        onSubmit={handleSubmit((values) => login.mutate(values))}
      >
        <div>
          <label htmlFor="email" className="mb-2 block text-sm font-semibold">
            Email
          </label>
          <Input
            id="email"
            type="email"
            autoComplete="email"
            aria-invalid={Boolean(errors.email)}
            {...register("email")}
          />
          {errors.email && (
            <p className="mt-1 text-sm text-red-700">{errors.email.message}</p>
          )}
        </div>
        <div>
          <label htmlFor="password" className="mb-2 block text-sm font-semibold">
            Password
          </label>
          <Input
            id="password"
            type="password"
            autoComplete="current-password"
            aria-invalid={Boolean(errors.password)}
            {...register("password")}
          />
          {errors.password && (
            <p className="mt-1 text-sm text-red-700">
              {errors.password.message}
            </p>
          )}
        </div>
        {login.error && (
          <p role="alert" className="rounded-lg bg-red-50 p-3 text-sm text-red-800">
            {login.error instanceof ApiError
              ? login.error.message
              : "Unable to sign in"}
          </p>
        )}
        <Button type="submit" className="w-full" disabled={login.isPending}>
          {login.isPending ? "Signing in…" : "Sign in"}
        </Button>
      </form>
      <Link href="/admin-login" className="mt-5 block text-center text-sm font-semibold text-slate-600 hover:text-blue-800">Administrator sign in</Link>
    </AuthCard>
  );
}
